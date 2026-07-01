import takodachi_bot.configs as Configs
import os
from datetime import datetime
from logging import FileHandler


class DynamicFileHandler(FileHandler):
    # 🌟 使用 *args 和 **kwargs 來接收 fileConfig 丟過來的所有未知參數，徹底防禦 TypeError
    def __init__(
        self, log_folder_name="", mode="a", encoding=None, delay=True, *args, **kwargs
    ):

        # 安全防禦：清洗掉設定檔可能殘留的引號
        log_folder_name = log_folder_name.strip("'\"")

        # 組合出正確的檔案絕對路徑
        filename = os.path.join(
            Configs.LOG_DIRECTORY, log_folder_name, self.get_current_date() + ".log"
        )

        # 🌟 呼叫父類別時，我們只精準傳遞 FileHandler 所需的 4 個核心參數，其餘沒用的直接丟掉
        super().__init__(filename, mode, encoding, delay)

    def _open(self):
        """覆寫底層開檔邏輯：真正要寫 Log 時才建立資料夾"""
        os.makedirs(os.path.dirname(self.baseFilename), exist_ok=True)
        return super()._open()

    def get_current_date(self):
        return datetime.now().strftime("%Y-%m-%d")
