import takodachi_bot.configs as Configs
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler
from logging import FileHandler

class DynamicFileHandler(FileHandler):
    def __init__(self, log_folder_name="", mode='a', encoding=None, delay=False):
        filename = os.path.join(Configs.LOG_DIRECTORY, log_folder_name, self.get_current_date() + '.log')
        os.makedirs(os.path.join(Configs.LOG_DIRECTORY, log_folder_name), exist_ok=True)
        super().__init__(filename, mode, encoding, delay)

    def get_current_date(self):
        return datetime.now().strftime('%Y-%m-%d')