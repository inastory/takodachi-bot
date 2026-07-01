import os
import sys
import asyncio
import psutil
from logging.config import fileConfig
import logging.handlers

import takodachi_bot.configs as configs
from takodachi_bot.modules import ServicesManager
from takodachi_bot.utils.datetime_utils import (
    format_datetime_by_timestamp,
    count_difference_by_timestamp,
)


def get_bot_pid_list():
    bot_pid_list = []
    if getattr(sys, "frozen", False):
        target_name = "takodachi.exe"
    else:
        target_name = "takodachi"

    for process in psutil.process_iter(["pid", "cmdline", "exe", "name"]):
        try:
            if getattr(sys, "frozen", False):
                # 1. 打包環境：比對執行檔名稱
                p_name = process.info.get("name", "") or ""
                if p_name.lower() == target_name.lower():
                    if process.info["pid"] == os.getpid():
                        continue
                    bot_pid_list.append(process.info["pid"])
            else:
                # 2. 開發環境 (uv run)
                command_line = process.info.get("cmdline", [])
                exe_path = process.info.get("exe", "") or ""

                if not command_line:
                    continue

                full_cmd_str = " ".join(command_line).lower()
                exe_path_lower = exe_path.lower()

                # 核心防線 1：命令列必須包含關鍵字
                if target_name.lower() in full_cmd_str:

                    # 核心防線 2：排除 VS Code 編輯器本身
                    if (
                        "microsoft vs code" in exe_path_lower
                        or "code.exe" in full_cmd_str
                    ):
                        continue

                    # 核心防線 3：排除 .venv\scripts 底下的導航殼（bot.exe）
                    if ".venv\\scripts" in exe_path_lower:
                        continue

                    # 核心防線 4：排除自己 (當前正在查 STATUS 的這個進程)
                    if process.info["pid"] == os.getpid():
                        continue

                    bot_pid_list.append(process.info["pid"])

        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    return bot_pid_list, target_name


def print_english_details(target_name, process):
    print(f"{target_name}")
    print("=" * 30)
    print(f"Status: {process.status()}")
    print()
    print(f"Command Line: {' '.join(process.cmdline())}")
    print()
    print(f"Create Time: {format_datetime_by_timestamp(process.create_time())}")
    print(f"Running Time: {count_difference_by_timestamp(process.create_time())}")
    print()
    print(f"CPU Usage (%): {process.cpu_percent()}%")
    print(f"Memory Usage (%): {process.memory_percent()}%")
    print()
    print(f"Number of Threads: {process.num_threads()}")
    print(f"Number of Handles: {process.num_handles()}")
    # print(f"Name: {process.name()}")
    # print(f"PID: {process.pid}")
    # print(f"Parent PID: {process.ppid()}")
    # print(f"Executable: {process.exe()}")
    print("=" * 30)
    print("")


def show_app_status():
    bot_pid_list, target_name = get_bot_pid_list()
    if not bot_pid_list:
        print(f"No running processes found with the name {target_name}.")
        return
    for pid in bot_pid_list:
        try:
            process = psutil.Process(pid)
            print_english_details(target_name, process)
        except psutil.NoSuchProcess:
            print(f"No process found with PID {pid}")
        except psutil.AccessDenied:
            print(f"Access denied for PID {pid}")


class App:
    def __init__(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.services_manager = ServicesManager(loop=self.loop, exit_callback=self.exit)
        self.init_logger()

    def init_logger(self):
        # 1. 確保實體的 logs 資料夾存在
        os.makedirs(configs.LOG_DIRECTORY, exist_ok=True)

        # 2. 註冊自訂 Handler 到 logging 模組，防範 .exe 環境解不出來
        from takodachi_bot.library.dynamic_file_handler import DynamicFileHandler

        setattr(logging, "DynamicFileHandler", DynamicFileHandler)

        # 3. 直接載入唯一的融合版 logger.conf
        fileConfig(
            configs.LOGGER_CONFIGS_PATH,
            disable_existing_loggers=False,
            encoding="utf-8",
        )

        # 4. 絕對路徑導航保險：當有人把 conf 切換成 rotating 模式時，幫內建類別強制校正家目錄
        root_logger = logging.getLogger()
        all_loggers = [root_logger] + [
            logging.getLogger(name) for name in logging.Logger.manager.loggerDict
        ]

        for logger in all_loggers:
            if not hasattr(logger, "handlers"):
                continue
            for handler in logger.handlers:
                if isinstance(handler, logging.handlers.RotatingFileHandler):
                    base_filename = os.path.basename(handler.baseFilename)
                    target_path = os.path.abspath(
                        os.path.join(configs.LOG_DIRECTORY, base_filename)
                    )
                    if handler.baseFilename != target_path:
                        handler.close()
                        handler.baseFilename = target_path

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
    # 🔥 第一關：攔截命令列參數。如果是 STATUS，直接跑完立刻結束，完全不建立 App 實例！
    if len(sys.argv) >= 2:
        request_type = sys.argv[1].upper()
        if request_type == "STATUS":
            show_app_status()
            sys.exit(0)  # 優雅退出
        else:
            print(f"Request type not found: {request_type}. Exiting.")
            sys.exit(1)

    # 🔥 第二關：正常點擊執行（無參數），啟動完整的系統服務與 GUI 圖示
    app = App()
    app.run()


if __name__ == "__main__":
    main()
