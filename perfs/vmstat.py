import subprocess
import helpers as h

class Vmstat:

    def set_recording_time(self, recording_time):
        assert type(recording_time) == int
        self.__recording_time = recording_time

    def set_filename(self, filename):
        assert type(filename) == str
        self.__filename = filename

    def __init__(self, recording_time, filename):
        self.__recording_time = recording_time
        self.__filename = '/sdcard/'+filename

    def __call__(self):
        subprocess.call(['adb', 'shell', 'vmstat', '1', str(self.__recording_time), '>', self.__filename], shell=False)

    def pull_data(self, target_folder):
        h.pull_data(self.__filename, target_folder)
