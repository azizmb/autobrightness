import os
import subprocess

import Image
import ImageStat


class Plugin(object):

    TMP_SCREEN_IMAGE = "/tmp/autobrightness-%s-screen-sample.jpg" % os.getenv("USER")

    DEFAULT_CONFIG = {
        'max_brightness': 100.0,
        'min_brightness': 0.0
    }

    def __init__(self, config):
        self.min_brightness = config.get(
            'min_brightness',
            self.DEFAULT_CONFIG['min_brightness']
        )
        self.max_brightness = config.get(
            'max_brightness',
            self.DEFAULT_CONFIG['max_brightness']
        )

    def get_screen_content_brightness(self):
        subprocess.call("scrot %s" % self.TMP_SCREEN_IMAGE, shell=True)
        im = Image.open(self.TMP_SCREEN_IMAGE).convert('L')
        stat = ImageStat.Stat(im)
        return stat.rms[0]

    def process(self, ambient_brightness):
        screen_content_brightness = self.get_screen_content_brightness()

        new_screen_brightness_value = (
            ambient_brightness + 255 - screen_content_brightness
        ) / 2.0 / 255.0
        new_screen_brightness = self.min_brightness + (
            self.max_brightness - self.min_brightness
        ) * new_screen_brightness_value

        subprocess.call(
            'xbacklight -set %s' % new_screen_brightness, shell=True
        )
        return True
