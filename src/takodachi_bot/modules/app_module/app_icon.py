from pystray import Icon, Menu, MenuItem
from PIL import Image
import os
import sys
import subprocess
import takodachi_bot.configs as configs

from takodachi_bot.modules.archive_module.service import (
    archive_and_play_twitch_stream,
    archive_twitch_stream,
    archive_video,
    archive_youtube_stream,
)


class AppIcon(Icon):
    def __init__(self, services_manager, exit_callback):
        self.services_manager = services_manager
        self.exit_callback = exit_callback
        self.notify_title = "Takodachi says"
        super().__init__(
            name=configs.APP_NAME,
            title=configs.APP_TITLE,
            icon=Image.open(configs.APP_ICON_PATH),
            menu=self.init_menu(),
        )

    def init_menu(self):
        twitch_submenu = Menu(
            MenuItem("Archive And Play", archive_and_play_twitch_stream),
            MenuItem("Archive Only", archive_twitch_stream),
        )
        volume_submenu = Menu(
            MenuItem("Start Limit Volume", self.start_volume_control),
            MenuItem("Stop Limit Volume", self.stop_volume_control),
        )
        app_menu = Menu(
            MenuItem("Archive Youtube Stream", archive_youtube_stream, default=True),
            MenuItem("Archive Twitch Stream...", twitch_submenu),
            MenuItem("Archive Video", archive_video),
            Menu.SEPARATOR,
            MenuItem("App Logs", self.show_logs),
            MenuItem("App Status", self.show_app_status),
            MenuItem("Discord Status", self.show_discord_status),
            Menu.SEPARATOR,
            MenuItem("Volume Control", volume_submenu),
            Menu.SEPARATOR,
            MenuItem("Exit", action=self.exit),
        )
        return app_menu

    def show_logs(self):
        os.startfile("logs")

    def show_notify(self, notify_message):
        self.notify(title=self.notify_title, message=notify_message)

    def show_app_status(self):
        if getattr(sys, "frozen", False):
            # --- 打包後的 EXE 環境 ---
            # sys.executable 指向你的 takodachi.exe
            # 'cmd /k' 執行完會保持視窗開啟（等同於原本 .bat 的 pause 效果）
            subprocess.Popen(f'start cmd /k "{sys.executable}" STATUS', shell=True)
        else:
            # --- 開發環境 (uv run) ---
            # 透過 uv 虛擬環境直接去呼叫主程式進入點，並帶入 STATUS
            # 這裡用 'cmd /k' 也是為了讓你看完狀態後黑視窗不會秒退
            subprocess.Popen('start cmd /k "uv run bot STATUS"', shell=True)

    def show_discord_status(self):
        if self.services_manager.is_service_running(configs.SERVICE_DISCORD_BOT):
            return self.show_notify("Discord Bot is running!")
        return self.show_notify("Discord Bot is stopped!")

    def start_volume_control(self):
        self.services_manager.start_service(configs.SERVICE_VOLUME_CONTROL)

    def stop_volume_control(self):
        self.services_manager.stop_service(configs.SERVICE_VOLUME_CONTROL)

    def exit(self):
        self.exit_callback()
