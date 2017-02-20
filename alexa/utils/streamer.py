import pafy
import subprocess
import logging


class Stream:
    def __init__(self, video_id):
        self.__video_id = video_id
        self.__length = -1

        video = pafy.new(video_id)
        best_audio = video.getbestaudio()
        self.__audio_stream_url = best_audio.url

    @property
    def length(self):
        if self.__length == -1:
            cmd = list()
            cmd.append('avprobe')
            cmd.append('-v')
            cmd.append('quiet')
            cmd.append(self.__audio_stream_url)
            cmd.append('-show_format_entry')
            cmd.append('duration')
            logging.debug('Running: %s' % ' '.join(cmd))
            try:
                self.__length = float(subprocess.check_output(cmd))
                logging.debug('Got %s seconds from command' % str(self.__length))
            except:
                self.__length = 0
                logging.error('Cannot get duration of video')

        return self.__length * 128100 / 8

    def get(self):
        cmd = list()
        cmd.append('avconv')
        cmd.append('-i')
        cmd.append(self.__audio_stream_url)
        cmd.append('-f')
        cmd.append('mp3')
        cmd.append('-b')
        cmd.append('128000')
        cmd.append('pipe:1')
        logging.debug('Running: %s' % ' '.join(cmd))

        converter = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        try:
            f = converter.stdout
            byte = f.read(65536)
            while byte:
                yield byte
                byte = f.read(65536)
        finally:
            converter.kill()
