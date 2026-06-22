import asyncio

if __name__ == "__main__":
    import sys,os
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

from takodachi_bot.modules.base_service import BaseService
from takodachi_bot.modules.volume_control_module.volume_control import VolumeControl

class VolumeControlService(BaseService):
    def __init__(self):
        super().__init__()
        self._volume_control_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self._volume_control_loop)
        self.volume_control = VolumeControl()

    def start_service(self):
        if self.is_running():
            return
        super().start_service()

        # if not EnvironmentUtils.has_permission():
        #     raise PermissionError("This script requires administrative privileges to modify audio settings.")
        print("Volume monitoring started.")

        asyncio.run_coroutine_threadsafe(self.volume_control.volume_monitoring(), self._volume_control_loop)
        self._volume_control_loop.run_forever()

    def stop_service(self):
        if not self.is_running():
            return
        super().stop_service()

        self._volume_control_loop.stop()
        print("Volume monitoring stopped.")

if __name__ == "__main__":
    volume_control_service = VolumeControlService()
    try:
        volume_control_service.start_service()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"{e}")
    finally:
        volume_control_service.stop_service()
