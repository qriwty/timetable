import datetime
import threading

from bot.timetable_bot import TimetableBot


def run_bot():
    TimetableBot().run_bot()


def reminder():
    print(f"[{datetime.datetime.now()}] Reminder started\n")


if __name__ == '__main__':
    t1 = threading.Thread(target=run_bot)
    t2 = threading.Thread(target=reminder)

    t1.start()
    t2.start()
