import datetime
import os
import json


class DataBase:
    def __init__(self):
        self.semester_start = datetime.datetime(2021, 9, 1)

        time_shift = {
            1: ["08:00", "09:35"],
            2: ["09:50", "11:25"],
            3: ["11:40", "13:15"],
            4: ["13:30", "15:05"]
        }

        timetable = {
            0: [
                [1, "Укр", 1, "лекция", "233гук"],
                [2, "Вышмат", None, "лекция", "201ф"],
                [3, "ООП", None, "лекция", "909ф"],
                [4, "Веб", None, "лекция", "203ф"]
            ],
            1: [
                [1, "Базы данных", None, "лаба", "607ф"],
                [2, "Конфликт", 0, None, "вставка"],
                [3, "Вышмат", None, "практика", "311ф"],
                [4, "Физ-ра", None, None, None]
            ],
            2: [
                [1, "Конфликт", 1, None, "вставка"],
                [2, "Экология", None, "лекция", "214гук"],
                [3, "Алгоритмы", None, "лекция", "707ф"],
                [4, "Базы данных", None, "лекция", "707ф"]
            ],
            3: [
                [2, "Веб", 1, "лаба", "909ф"],
                [3, "Укр", None, "практика", "201ф"]
            ],
            4: [
                [1, "ООП", None, "лаба", "909ф"],
                [2, "Экология", 1, "практика", "02а"],
                [2, "Алгоритмы", 0, "лаба", "109а"],
                [3, "Физ-ра", None, None, None]
            ]
        }

        russian_timetable = {
            0: "Понедельник",
            1: "Вторник",
            2: "Среда",
            3: "Четверг",
            4: "Пятница"
        }

        data = {
            "TIMETABLE": timetable,
            "TIME_SHIFT": time_shift,
            "RUSSIAN_TABLE": russian_timetable
        }

        self.token_path = "TOKEN"
        self.timetable_path = "TIMETABLE.json"
        self.logfile_path = "bot.log"

        # with open(self.timetable_path, 'w+', encoding='utf-8') as f:
        #     json.dump(data, f, indent=4, ensure_ascii=False)

    def is_exists(self, path):
        return os.path.isfile(path)

    def open_token(self):
        assert self.is_exists(self.token_path), "TOKEN FILE IS NOT EXISTS"

        with open(self.token_path, "r") as f:
            try:
                token = f.readline()
                assert len(token) == 46, "TOKEN IS CORRUPTED"
                return token
            except IOError:
                print("TOKEN FILE READ ERROR")
            finally:
                f.close()

    def open_timetable(self):
        assert self.is_exists(self.timetable_path), "TIMETABLE FILE IS NOT EXISTS"

        with open(self.timetable_path, "r") as f:
            try:
                data = json.load(f)
            except IOError:
                print("TIMETABLE FILE READ ERROR")
            finally:
                f.close()

        assert "TIMETABLE" in data.keys(), "TIMETABLE NOT IN FILE"
        assert "TIME_SHIFT" in data.keys(), "TIME SHIFT NOT IN FILE"
        assert "RUSSIAN_TABLE" in data.keys(), "RUSSIAN TABLE NOT IN FILE"

        return data

    def write_log(self, message):
        with open(self.logfile_path, "a+", encoding="utf-8") as f:
            try:
                f.write(message)
            except:
                print("LOG FILE WRITE ERROR")
            finally:
                f.close()
