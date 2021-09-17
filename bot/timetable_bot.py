import datetime
import time
import math

import telebot
from telebot import types

from bot.database import DataBase
from bot.logger import Logger


class TimetableBot:
    def __init__(self):
        self.database = DataBase()
        self.logger = Logger()

        token = self.database.open_token()

        self.bot = telebot.TeleBot(token)

        @self.bot.message_handler(content_types=["text"])
        def msg(message):
            self.message_parse(message)

    def run_bot(self):
        self.logger.add_log("INIT SYSTEM CHECK", log_type="INFO", system_message=True)
        self.database.open_token()
        self.logger.add_log("TOKEN FOUNDED", log_type="INFO", system_message=True)
        self.database.open_timetable()
        self.logger.add_log("TIMETABLE FOUNDED", log_type="INFO", system_message=True)

        self.logger.add_log("SYSTEM CHECK SUCCESS", log_type="INFO", system_message=True)

        while True:
            self.logger.add_log("BOT STARTED", log_type="INFO", system_message=True)
            try:
                self.bot.polling(none_stop=True)
            except:
                self.logger.add_log("BOT FAILED \\ RESTARTING", log_type="ERROR", system_message=True)
                time.sleep(10)

    def start_up(self, message):
        # self.logger.logger(message)
        # user_id = message.chat.id
        # user_name = message.from_user.first_name
        return 0

    def timetable_controller(self, user_id, timespan, time_swing=0):
        data = self.database.open_timetable()
        timetable = data["TIMETABLE"]
        time_shift = data["TIME_SHIFT"]
        russian_days = data["RUSSIAN_TABLE"]

        start_date = self.database.semester_start
        today = datetime.datetime.now()

        current_date = today + datetime.timedelta(days=time_swing)
        week_start = current_date - datetime.timedelta(days=current_date.weekday())

        num_of_weeks = math.ceil((current_date - start_date).days / 7.0)

        is_even = num_of_weeks % 2

        msg = ""
        week_day = current_date.weekday()
        if timespan == "week":
            week_day = week_start
            for day in timetable:
                msg += f"\n{russian_days[day]} {datetime.datetime.strftime(week_day, '%d.%m')}\n"
                for subject in timetable[day]:
                    subject_start = time_shift[str(subject[0])][0]
                    subject_end = time_shift[str(subject[0])][1]
                    lesson_type = f"({subject[3]})" if subject[3] is not None else ""
                    cabinet = f"{subject[4]}" if subject[4] is not None else ""
                    if subject[2] == is_even or subject[2] is None:
                        msg += f"{subject_start} - {subject_end} -- {subject[1]} {lesson_type} {cabinet}\n"
                week_day += datetime.timedelta(days=1)

        else:
            if str(week_day) in timetable:
                msg += f"{russian_days[str(week_day)]} {datetime.datetime.strftime(current_date, '%d.%m')}\n"
                for subject in timetable[str(week_day)]:
                    subject_start = time_shift[str(subject[0])][0]
                    subject_end = time_shift[str(subject[0])][1]
                    lesson_type = f"({subject[3]})" if subject[3] is not None else ""
                    cabinet = f"{subject[4]}" if subject[4] is not None else ""
                    if subject[2] == is_even or subject[2] is None:
                        msg += f"{subject_start} - {subject_end} -- {subject[1]} {lesson_type} {cabinet}\n"
            else:
                msg += f"{datetime.datetime.strftime(current_date, '%d.%m')}\t"
                msg += "Выходной"

        self.bot.send_message(user_id, msg)

    def message_parse(self, message):
        self.logger.add_log(message, log_type="INFO")

        user_id = message.chat.id
        user_name = message.from_user.first_name
        command = message.text

        if command == "/start":
            self.start_up(message)
            self.bot.send_message(user_id, "Даров, {}".format(user_name))
            self.keyboard_menu(user_id)

        elif command == "/help":
            self.bot.send_message(user_id, "Сорян, {}, не помогу".format(user_name))

        elif command == "Расписание на неделю":
            self.timetable_controller(user_id, "week")

        elif command == "Расписание на следующую неделю":
            self.timetable_controller(user_id, "week", 7)

        elif command == "Расписание на завтра":
            self.timetable_controller(user_id, "day", 1)

        elif command == "Сегодняшнее расписание":
            self.timetable_controller(user_id, "day")

        else:
            self.bot.reply_to(message, "И что это значит?")

    def keyboard_menu(self, user_id):
        markup = types.ReplyKeyboardMarkup(row_width=1)

        btn1 = types.KeyboardButton('Расписание на неделю')
        btn2 = types.KeyboardButton('Расписание на следующую неделю')
        btn3 = types.KeyboardButton('Расписание на завтра')
        btn4 = types.KeyboardButton('Сегодняшнее расписание')

        markup.add(btn1, btn2, btn3, btn4)

        self.bot.send_message(user_id, "Чего желаешь?", reply_markup=markup)

