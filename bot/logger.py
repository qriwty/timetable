import datetime

from bot.database import DataBase


class Logger:
    def __init__(self):
        self.database = DataBase()

    def add_log(self, message, log_type, system_message=False):
        msg = f"[{datetime.datetime.now()}]\t"
        msg += f"{log_type}:\t"
        if not system_message:
            user_id = message.chat.id
            user_name = message.from_user.first_name
            user_username = message.chat.username
            command = message.text

            msg += f"USER {user_id}\tNAME {user_name}\tUSERNAME {user_username}\tCOMMAND {command}"
        else:
            msg += f"{message}"

        print(msg)

        msg += "\n"
        self.database.write_log(msg)
