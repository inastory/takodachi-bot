from ..base_service import BaseService
from .app_icon import AppIcon

class AppIconService(BaseService):
    def __init__(self, services_manager, exit_callback):
        super().__init__()
        self.app_icon = AppIcon(services_manager, exit_callback)

    def start_service(self):
        if super().is_running():
            return
        super().start_service()
        self.app_icon.run()

    def stop_service(self):
        if not super().is_running():
            return
        super().stop_service()
        self.app_icon.visible = False
        self.app_icon.stop()
        print("App icon stopped")

    def notify(self, message):
        if super().is_running:
            self.app_icon.notify(message)