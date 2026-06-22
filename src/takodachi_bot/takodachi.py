import os
import sys
import asyncio

from logging.config import fileConfig
import logging.handlers

import takodachi_bot.configs as configs
from takodachi_bot.modules import ServicesManager

class App():
    def __init__(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.services_manager = ServicesManager(loop=self.loop, exit_callback = self.exit)
        self.init_logger()


    def init_logger(self):
        # 1. 確保實體的 logs 資料夾存在於安全目錄 (configs.py 算出的 exe_dir)
        os.makedirs(configs.LOG_DIRECTORY, exist_ok=True)

        # 2. 精準根據「是否為打包環境」選擇設定檔
        if getattr(sys, 'frozen', False):
            logger_path = configs.LOGGER_CONFIGS_EXE_PATH
        else:
            logger_path = configs.LOGGER_CONFIGS_PATH

        # 3. 載入日誌設定結構
        fileConfig(logger_path, disable_existing_loggers=False,
                encoding="utf-8")

        # 4. 🔥 動態注入絕對路徑，防止 RotatingFileHandler 在 EXE 環境下亂跑
        # 對應你在 logger_exe.conf 中設定的 handler 名稱與想要的實際檔名
        loggers_mapping = {
            'fileHandler': 'app.log',
            'archiveFileHandler': 'archive.log',
            'remotePCFileHandler': 'remote_pc.log'
        }

        # 取得所有已登記的 loggers
        all_loggers = [logging.getLogger(), logging.getLogger(
            'archive'), logging.getLogger('remotePC')]

        for logger in all_loggers:
            for handler in logger.handlers:
                # 同時支援內建的 RotatingFileHandler 與你的 DynamicFileHandler
                if isinstance(handler, (logging.handlers.RotatingFileHandler, logging.FileHandler)):
                    handler_name = handler.name
                    if handler_name in loggers_mapping:
                        handler.close()  # 關閉預設開啟的相對路徑檔案

                        # 計算出絕對安全的絕對路徑 (例如: C:\...\takodachi-bot\logs\app.log)
                        target_path = os.path.join(
                            configs.LOG_DIRECTORY, loggers_mapping[handler_name])
                        handler.baseFilename = os.path.abspath(target_path)

    def run(self):
        self.services_manager.start_default_service()
        self.loop.run_forever()

        print("[Takodachi] Shutting down background thread pool...")
        self.services_manager.executor.shutdown(wait=False)

        print("[Takodachi] Program exited successfully. Goodbye!")
        os._exit(0)

    def exit(self):
        def _thread_safe_shutdown():
            print("[Takodachi] Stopping all background services...")
            self.services_manager.stop_all_services()
            self.loop.stop()
            print("[Takodachi] Event loop terminated.")
        self.loop.call_soon_threadsafe(_thread_safe_shutdown)

def main():
    app = App()
    app.run()

if __name__ == "__main__":
    main()