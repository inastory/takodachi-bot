class BaseService():
    def __init__(self) -> None:
        self._is_running = False

    def start_service(self) -> None:
        self._is_running = True

    def stop_service(self) -> None:
        self._is_running = False

    def is_running(self) -> bool:
        return self._is_running