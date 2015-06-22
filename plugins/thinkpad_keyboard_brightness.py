import math
import os
import subprocess


class Plugin(object):

    DEFAULT_CONFIG = {
        'driver_bin_path': os.path.join('/', 'usr', 'bin', 'thinklight')
    }

    def __init__(self, config):
        self.driver_bin_path = config.get(
            'driver_bin_path',
            self.DEFAULT_CONFIG['driver_bin_path']
        )

    def process(self, ambient_brightness):

        ambient_brightness = int(ambient_brightness)

        if ambient_brightness in xrange(0, 17):
            new_light_level = 2
        elif ambient_brightness in xrange(17, 40):
            new_light_level = 1
        elif ambient_brightness in xrange(40, 255):
            new_light_level = 3

        subprocess.call(
            '%s %d' % (self.driver_bin_path, new_light_level),
            shell=True
        )
        return True
