import re
from datetime import date, datetime, timedelta

from django.utils.translation import ugettext as _

from timetable.constants import GROUP_REGEXP, WEEK_DAYS_ABBREVIATIONS


class Parameters:
    """Class for parsing and validating bot command parameters.

    Transforms all parameters from string to corresponding class fields.
    Works as Django form: you need to create class instance and then call
    is_valid() method to start parsing and validation. If validation goes wrong,
    is_valid() method will return false and all errors will be in `errors`
    field.

    Possible parameters:
        kv-32, КВ32... - group code
        w1, w2 - week numbers
        w - current week number
        mon, tue, ..., fri - day number
        t - show teachers name
        123, 527 - teachers id (for /setteacher, /teacher commands)
        1, 2, ..., 7 - lesson number
        Иванов Иван - teachers name
    """

    def __init__(self, command: str, parameters: list):
        self.command = command
        self.parameters = parameters
        self.errors = []

    def is_valid(self) -> bool:
        self._parse_parameters(self.parameters)
        self._validate_parameters()
        self._customize_date()

        # If errors array is not empty, validation gone wrong, so return false.
        return not self.errors

    def _parse_parameters(self, parameters: list) -> None:
        """Transform string with command parameters to class fields"""
        for token in parameters:
            if re.match(GROUP_REGEXP, token):  # Group code
                self.group_name = self.transliterate(token)
                # To provide possability to enter group code without '-'
                # we need to check it and manually insert into string.
                if '-' not in token:
                    number_position = re.search("\d", token).start()
                    self.group_name = self.group_name[:number_position] + '-' +\
                        self.group_name[number_position:]
            elif re.match("w[1|2]", token):
                self.week = int(token[1])
            elif token == 'w':
                # Return current week number (1 or 2)
                self.week = 2 - date.today().isocalendar()[1] % 2
            elif token == 't':
                self.print_teacher = True
            elif self.get_week_day(token):
                self.day = self.get_week_day(token)
            elif token.isdigit():  # If token contains only numbers, it can be
                if self.command in ["/setteacher", "/teacher"]:  # teachers ID
                    self.teacher_id = int(token)
                else:
                    self.number = int(token)  # or lesson number
            elif re.match("[А-яіє]+", token):
                if not hasattr(self, "teachers_name"):
                    self.teachers_name = token
                else:
                    self.teachers_name += " " + token
            else:
                self.errors.append(_("Неправильный параметр"))

    def _customize_date(self) -> None:
        """For some commands, like '/today' or '/now' we need to manually set
        day number, week number and lesson number basing on current time.
        """
        if self.command in ["/today", "/tomorrow", "/now", "/next", "/where", "/who"]:
            current_date = date.today()
            if self.command == "/tomorrow":
                current_date += timedelta(days=1)

            self.week = 2 - current_date.isocalendar()[1] % 2
            self.day = current_date.weekday() + 1
            if self.command in ["/now", "/next", "/where", "/who"]:
                # TODO: Refactor
                now = datetime.now()
                pairs = [
                    datetime(now.year, now.month, now.day, 0, 1),
                    datetime(now.year, now.month, now.day, 8, 30),
                    datetime(now.year, now.month, now.day, 10, 5),
                    datetime(now.year, now.month, now.day, 12, 0),
                    datetime(now.year, now.month, now.day, 13, 55),
                    datetime(now.year, now.month, now.day, 15, 50),
                    datetime(now.year, now.month, now.day, 17, 45),
                    datetime(now.year, now.month, now.day, 23, 59)
                ]
                for i in range(len(pairs) - 1):
                    if now > pairs[i] and now < pairs[i + 1]:
                        self.lesson = i
                        break

                if self.command == "/next":
                    self.lesson += 1

    def _validate_parameters(self) -> None:
        """Some parameters are used only with certain commands, so we need to
        check, if we don't have unnecessary parameters or vice versa, if we
        don't have required parameter for command.
        """
        # Only `/tt` and `/teacher` commands can have week, day and lesson
        # number parameters
        if self.command == "/setgroup" and not hasattr(self, 'group_name'):
            self.errors.append(_("Код группы не задан."))
        if self.command in ["/setteacher", "/teacher"] and\
                (not hasattr(self, 'teachers_name') and
                 not hasattr(self, 'teacher_id')):
            self.errors.append(_("Имя или id преподавателя не заданы."))
        if self.command not in ["/tt", "/teacher"] and\
                (hasattr(self, 'day') or
                 hasattr(self, 'week') or
                 hasattr(self, 'number')):
            self.errors.append(_("Неправильный параметр для этой команды."))

    # Helper functions
    @staticmethod
    def transliterate(text: str):
        tr_en_ua = str.maketrans("abcdefghijklmnopqrstuvwxyz",
                                 "абцдефгхіжклмнопкрстуввхуз")
        return text.translate(tr_en_ua)

    @staticmethod
    def get_week_day(token: str):
        for day_number, day_names in WEEK_DAYS_ABBREVIATIONS.items():
            if token in day_names:
                return day_number
