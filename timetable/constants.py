HELP_TEXT = """/setgroup [Код твоей группы] — таким образом я тебя запомню твою группу для дальнейшей нашей совместной жизни (если ты студент).
(Пример: /setgroup КВ72 или /setgroup kv-72)
/setteacher фамилия — а если ты преподаватель, то тебе стоит воспользоваться этой командой (писать на украинском языке)
(Пример: /setteacher Іва (если фамилия Иванов, Ивашин, Иваненко, т.д.))
/map — пришлю тебе карту КПИ. Правда, тебе прийдёт сжатая версия, так что если ты хочешь рассмотреть все детали - используй команду /fullmap
/now — напомню тебе, какая пара у тебя сейчас и сколько времени осталось до её конца.
/teacher фамилия - покажет тебе расписание преподавателя.
/time — просто выведу тебе время начала всех пар
/today — этой командой я покажу тебе расписание на сегодня.
/tomorrow — этой командой я смогу тебе показать расписание на завтра.
/tt — покажу полное расписание на все недели.
/week — помогу узнать, какая сейчас учебная неделя
/where — не дам тебе потеряться - скину карту с местоположением текущей аудитории
/who — напомню тебе, как зовут преподавателя, который стоит перед тобой.
А ещё к каждой из команд можно добавить __параметры__:
- Номер группы в виде КВ-72 или kv-72 чтобы отобразить расписание для любой конкретной группы
(Например, /today kv-52 покажет расписание на сегодня для группы КВ-52)
- Номер недели в ввиде w1 и w2 для вывода результата для первой или второй недели обучения соответственно
(Например, /tt w1 покажет полное расписание первой недели)
- Параметр w выведет расписание на текущую неделю.
(Например, если сейчас вторая неделя, то /tt w выведет расписание на всю вторую неделю)
- С помощью параметра t ты сможешь показать имена преподавателей. Этот параметр можно использовать почти с любой командой.
- Ты можешь посмотреть расписание на конкретный день используя, например, /tt mon или /tt пн.

А самое главное, что все эти параметры ты можешь комбинировать! Причем в любом порядке!
Несколько примеров:
- `/tt ia-25 w1`
- `/tt w2 mon IA-52`
- `/tt KM-21 w t`"""

TIME = """
1. 08:30 - 10:05
2. 10:25 - 12:00
3. 12:20 - 13:55
4. 14:15 - 15:50
5. 16:10 - 17:45
"""

EXCEPTION_MESSAGE = """
Из-за кривых рук моего разработчика случилась нередвиденная ошибка, но он уже об этом знает и скоро всё исправит.
Если ты хочешь пнуть его лично, то пиши @vladsydorenko
""".replace('\n', ' ')
