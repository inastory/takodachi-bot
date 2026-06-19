import logging
from collections import OrderedDict
from concurrent.futures import ThreadPoolExecutor

from configs import (
    SERVICE_DISCORD_BOT as DISCORD_BOT_KEY,
    SERVICE_VOLUME_CONTROL as VOLUME_CONTROL_KEY,
    SERVICE_APP_ICON as APP_ICON_KEY
)

from modules import DiscordBotService
from modules import VolumeControlService
from modules import AppIconService

log = logging.getLogger('exception')

class ServicesManager():
    _services = OrderedDict()
    
    def __init__(self, loop, exit_callback):
        self.loop = loop
        self.executor = ThreadPoolExecutor(thread_name_prefix='We-are-here-')
        self.exit_callback = exit_callback
        self.init_services()

    def init_services(self):
        app_service = AppIconService(self, self.exit_callback)
        discord_service = DiscordBotService()
        volume_control_service = VolumeControlService()

        self.register_service(DISCORD_BOT_KEY, discord_service)
        self.register_service(VOLUME_CONTROL_KEY, volume_control_service)
        self.register_service(APP_ICON_KEY, app_service)

    def start_service(self, service_name):
        service = self.get_service(service_name)
        if service:
            try:
                self.loop.run_in_executor(self.executor, service.start_service)
            except Exception as exception:
                self.handle_exception(exception)

    def stop_service(self, service_name):
        service = self.get_service(service_name)
        if service:
            self.loop.run_in_executor(self.executor, service.stop_service)

    def start_default_service(self):
        self.start_service(DISCORD_BOT_KEY)
        self.start_service(APP_ICON_KEY)

    def stop_all_services(self):
        print("[ServicesManager] Shutting down services one by one...")
        for name, service in self._services.items():
            try:
                service.stop_service()
                print(
                    f"[ServicesManager] Service '{name}' stopped successfully.")
            except Exception as e:
                print(
                    f"[ServicesManager] Error occurred while stopping service '{name}': {e}")

    def get_service(self, service_name):
        return self._services.get(service_name, None)

    def is_service_running(self, service_name):
        service = self.get_service(service_name)
        if service:
            return service.is_running()

    def get_notify_methods(self, app_service, discord_service):
        return [app_service.notify, discord_service.notify]

    def handle_exception(self, exception):
        log.exception(f"Exception in {exception.name}: {exception.message}")
        self.get_service(APP_ICON_KEY).notify_exception(exception)
        self.get_service(DISCORD_BOT_KEY).notify_exception(exception)

    @classmethod
    def register_service(cls, service_name, service_instance):
        cls._services[service_name] = service_instance

    @classmethod
    def get_service(cls, service_name):
        return cls._services.get(service_name, None)
