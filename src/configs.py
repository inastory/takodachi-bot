import os
import os, sys
from dotenv import load_dotenv
from urllib.parse import quote_plus

src_dir = os.path.dirname(os.path.abspath(__file__))

project_root = os.path.abspath(os.path.join(src_dir, ".."))

# env setup
env_file_path = os.path.join(project_root, '.env')
if getattr(sys, 'frozen', False):
    env_file_path = os.path.join(os.path.dirname(sys.executable), '.env')
load_dotenv(dotenv_path=env_file_path)

# App setting
APP_NAME = "Takodachi"
APP_TITLE = "Wah!"
APP_ICON_PATH = os.path.join(project_root, "assets", "icon_logo.png")

APP_PROCESS_NAME = "takodachi.pyw"
APP_STATUS_BAT_PATCH = os.path.join(project_root, "scripts", "takodachi-bot-status.bat")
if getattr(sys, 'frozen', False):
    APP_STATUS_BAT_PATCH = os.path.join(os.path.dirname(sys.executable), "takodachi-bot-status.bat")

# Service setting
SERVICE_APP_ICON = 'app_icon'
SERVICE_DISCORD_BOT = 'discord_bot'
SERVICE_VOLUME_CONTROL = 'volume_control'

SERVICE_SCHEDULER = 'scheduler'
SERVICE_HOLOLIVE_SCHEDULE = 'hololive_schedule'

# Database setting
DATABASE_NAME = "data/data.db"
DATABASE_MARIADB_USER = os.getenv("MARIADB_USER")
DATABASE_MARIADB_PASSWORD = os.getenv("MARIADB_PASSWORD")
DATABASE_MARIADB_HOST = os.getenv("MARIADB_HOST")
DATABASE_MARIADB_PORT = os.getenv("MARIADB_PORT")
DATABASE_MARIADB_NAME = os.getenv("MARIADB_NAME")
DATABASE_MARIADB_URL = f"mariadb+pymysql://{DATABASE_MARIADB_USER}:{quote_plus(str(DATABASE_MARIADB_PASSWORD))}@{DATABASE_MARIADB_HOST}:{DATABASE_MARIADB_PORT}/{DATABASE_MARIADB_NAME}"

# Logger setting
LOG_DIRECTORY = 'logs'
LOGGER_CONFIGS_PATH = os.path.join(src_dir, 'library', 'logger.conf')
LOGGER_CONFIGS_EXE_PATH = os.path.join(src_dir, 'library', 'logger_exe.conf')

# API setting
API_YOUTUBE_KEY = os.getenv("YOUTUBE_API_KEY")

# region Archive module
# File patch
FOLDER_YT_DLP_BAT_PATCH                  = os.getenv("FOLDER_YT_DLP_BAT_PATCH")
ARCHIVE_YOUTUBE_STREAM_BAT_PATCH         = os.getenv("ARCHIVE_YOUTUBE_STREAM_BAT_PATCH")
ARCHIVE_VIDEO_BAT_PATCH                  = os.getenv("ARCHIVE_VIDEO_BAT_PATCH")

FOLDER_STREAMLINK_BAT_PATCH              = os.getenv("FOLDER_STREAMLINK_BAT_PATCH")
ARCHIVE_AND_PLAY_TWITCH_STREAM_BAT_PATCH = os.getenv("ARCHIVE_AND_PLAY_TWITCH_STREAM_BAT_PATCH")
ARCHIVE_TWITCH_STREAM_BAT_PATCH          = os.getenv("ARCHIVE_TWITCH_STREAM_BAT_PATCH")

# Archive command
ARCHIVE_YOUTUBE_LIVE_COMMAND             = os.getenv("ARCHIVE_YOUTUBE_LIVE_COMMAND")
ARCHIVE_TWITCH_LIVE_COMMAND              = os.getenv("ARCHIVE_TWITCH_LIVE_COMMAND")
ARCHIVE_VIDEO_COMMAND                    = os.getenv("ARCHIVE_VIDEO_COMMAND")
# endregion

# region Discord Bot setting
BOT_DESCRIPTION = "A DD Takodachi"
BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
BOT_PREFIX = os.getenv("DISCORD_BOT_PREFIX", '!')

DISCORD_EXCEPTION_CHANNEL_ID = 1185820334146981958
# endregion