import os
import asyncio

from logging.config import fileConfig

import configs

from modules import ServicesManager


class App():
    def __init__(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.services_manager = ServicesManager(
            loop=self.loop, exit_callback=self.exit)
        self.init_logger()

    def init_logger(self):
        if not os.path.exists(configs.LOG_DIRECTORY):
            os.makedirs(configs.LOG_DIRECTORY)

        logger_path = configs.LOGGER_CONFIGS_PATH
        if not os.path.exists(logger_path):
            logger_path = configs.LOGGER_CONFIGS_EXE_PATH
        fileConfig(logger_path, disable_existing_loggers=False,
                   encoding="utf-8")

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


if __name__ == "__main__":
    app = App()
    app.run()
