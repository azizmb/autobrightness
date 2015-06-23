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
        self.current_value = None

    def process(self, ambient_brightness):

        ambient_brightness = int(ambient_brightness)

        if ambient_brightness in xrange(0, 16):
            new_light_level = 2
        elif ambient_brightness in xrange(16, 25):
            new_light_level = 1
        elif ambient_brightness in xrange(25, 256):
            new_light_level = 3

        if new_light_level != self.current_value:
            print 'Setting keyboard light level to %s' % new_light_level
            subprocess.call(
                '%s %d' % (self.driver_bin_path, new_light_level),
                shell=True
            )
            self.current_value = new_light_level
        else:
            print 'No change in keyboard brightness'

        return True
