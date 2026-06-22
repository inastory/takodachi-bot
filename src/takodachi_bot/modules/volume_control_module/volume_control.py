import asyncio
from typing import Any
import comtypes
from comtypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

if __name__ == "__main__":
    import sys
    import os
    sys.path.append(os.path.abspath(
        os.path.join(os.path.dirname(__file__), '../'*3)))


class VolumeControl():
    def __init__(self):
        self._minimum_volume_limit: float = 0.3
        self._maximum_volume_limit: float = 0.5

        # Initialize COM at the beginning of your script
        comtypes.CoInitialize()

        # Get the audio output (speakers) device
        self._devices = AudioUtilities.GetSpeakers()

        # Activate the interface to control audio volume
        self._interface = self._devices.Activate(
            IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        self._volume: Any = cast(self._interface, POINTER(IAudioEndpointVolume))

    @property
    def minimum_volume_limit(self):
        return self._minimum_volume_limit

    @minimum_volume_limit.setter
    def minimum_volume_limit(self, value):
        if isinstance(value, (int, float)):
            self._minimum_volume_limit = value

    @property
    def maximum_volume_limit(self):
        return self._maximum_volume_limit

    @maximum_volume_limit.setter
    def maximum_volume_limit(self, value):
        if isinstance(value, (int, float)):
            self._maximum_volume_limit = value

    async def volume_monitoring(self):
        while True:
            # Get the current volume level as a scalar (0.0 to 1.0)
            self.current_volume = self._volume.GetMasterVolumeLevelScalar()
            # print("Current: " + str(self.current_volume))

            if abs(round(self.current_volume - self._minimum_volume_limit, 2)) > 0.01:
                # Check if the current volume exceeds the minimum limit
                if self.current_volume < self._minimum_volume_limit:
                    # If it does, set the volume to the minimum limit
                    self._volume.SetMasterVolumeLevelScalar(
                        self._minimum_volume_limit, None)
                    # print("Mini limit start: " + str(self._minimum_volume_limit))

                # Check if the current volume exceeds the maximum limit
                if self.current_volume > self._maximum_volume_limit:
                    # If it does, set the volume to the maximum limit
                    self._volume.SetMasterVolumeLevelScalar(
                        self._maximum_volume_limit, None)
                    # print("Max limit start: " + str(self._maximum_volume_limit))

            # Wait for a period (1 second) before checking again
            await asyncio.sleep(1)  # Adjust volume every second


if __name__ == "__main__":
    volume_control_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(volume_control_loop)

    volume_control = VolumeControl()
    try:
        volume_control_loop.create_task(volume_control.volume_monitoring())
        print("Volume monitoring started. Press Ctrl+C to stop.")
        volume_control_loop.run_forever()
    except KeyboardInterrupt:
        pass
    except PermissionError as e:
        print(f"{e}")
    finally:
        volume_control_loop.stop()
        print("Volume monitoring stopped.")
