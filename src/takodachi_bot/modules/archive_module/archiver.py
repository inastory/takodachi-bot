# Module: archive
# Description: Archive Live Stream / Video
# Usage:
#       1. !savel "url"
#       2. !savev "url"
# Dependencies: 

import logging, subprocess
import takodachi_bot.configs as Configs
import contextlib
import re

log = logging.getLogger('archive')
get_process_command = {
    'default' : Configs.ARCHIVE_YOUTUBE_LIVE_COMMAND,
    'twitch' : Configs.ARCHIVE_TWITCH_LIVE_COMMAND,
    'video' : Configs.ARCHIVE_VIDEO_COMMAND,
}
newlines = ['\n', '\r\n', '\r']

def get_video_id_from_command(command):
    pattern = r".*"
    if 'youtube' in command:
        pattern = r"https://www\.youtube\.com/watch\?v=([a-zA-Z0-9_-]+)"
    if 'twitch' in command:
        pattern = r"https://www.twitch.tv/(\w+)"

    match = re.search(pattern, command)

    if match:
        return match.group(1)

class Archiver():
    async def archive_live_stream(self, ctx, command):
        source_type = 'default'
        if 'twitch' in command:
            source_type = 'twitch'
        command = str(get_process_command[source_type]) + ' ' + command
        await self.start_archive(ctx, command)

    async def archive_video(self, ctx, command):
        source_type = 'video'
        command = str(get_process_command[source_type]) + ' ' + command
        await self.start_archive(ctx, command)

    # https://www.cnblogs.com/security-darren/p/4733368.html
    # https://gist.github.com/thelinuxkid/5114777
    # Unix, Windows and old Macintosh end-of-line
    async def unbuffered(self, command_result, stream='stdout'):
        stream = getattr(command_result, stream)
        with contextlib.closing(stream):
            while True:
                out = []
                last = stream.read(1)
                if last == '' and command_result.poll() is not None:
                    break
                while last not in newlines:
                    if last == '' and command_result.poll() is not None:
                        break
                    out.append(last)
                    last = stream.read(1)
                out = ''.join(out)
                yield out

    async def start_archive(self, ctx, command):
        video_id = get_video_id_from_command(command)
        await ctx.send("Start archiving: {}".format(video_id))
        log.debug("Start archiving: {}".format(command))
        # first_line = True
        try:
            command_result = subprocess.Popen(command ,stdout=subprocess.PIPE ,stderr=subprocess.STDOUT ,universal_newlines=True, shell=True)
            async for line in self.unbuffered(command_result):
                # if line.startswith("[youtube]"):
                #     if(first_line):
                #         await ctx.send(line)
                #         first_line=False
                if line.strip() == "":
                    continue
                if line.startswith("[MetadataParser]"):
                    continue
                if line.startswith("ERROR"):
                    await ctx.send("Error Occurred!: " + ':'.join(line.split(':')[-2:]).strip())
                    log.error(line.split(":", 1)[1].strip())
                    continue
                log.info(line)
        except Exception as e:
            message = 'Error Occurred : [{}] while archiving [{}]'.format(str(e),video_id)
            log.error(message)
            await ctx.send(message)
        finally:
            log.debug("Archive completed: {}".format(command))
            await ctx.send("Archive completed: {}".format(video_id))