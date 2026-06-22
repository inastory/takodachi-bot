from ctypes import windll

class EnvironmentUtils():
    @classmethod
    def has_permission(self):
        try:
            return windll.shell32.IsUserAnAdmin()
        except Exception:
            return False