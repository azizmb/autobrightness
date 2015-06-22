#!/usr/bin/env python
import argparse
import json
import math
import os
import subprocess
import sys
import time

import Image
import ImageStat

from plugins.screen_brightness import Plugin as ScreenBrightnessPlugin
from plugins.thinkpad_keyboard_brightness import Plugin as ThinkpadKeyboardBrightnessPlugin


TMP_CAMERA_IMAGE = "/tmp/autobrightness-%s-camera-sample.jpg" % os.getenv("USER")

DEFAULT_CONFIG = {
    'sample_rate': 5,
}

HOME_PATH = os.getenv("HOME")
CONFIG_FOLDER_PATH = os.path.join(HOME_PATH, '.config')
APP_CONFIG_FOLDER_PATH = os.path.join(CONFIG_FOLDER_PATH, '.config', 'wildguppy')
CONFIG_FILE_PATH = os.path.join(APP_CONFIG_FOLDER_PATH, 'config.json')

def init_default_config(config_file_path):
    if not os.path.exists(config_file_path):
        config_dir = os.path.dirname(config_file_path)
        if not os.path.exists(config_dir):
            os.makedirs(config_dir)
        with open(config_file_path, 'w') as fp:
            json.dump(DEFAULT_CONFIG, fp)


def brightness(im_file):
    im = Image.open(im_file).convert('L')
    stat = ImageStat.Stat(im)
    return stat.rms[0]


def get_ambient_brightness():
    subprocess.call(
        "fswebcam -r 356x292 -d /dev/video0 %s" % TMP_CAMERA_IMAGE, shell=True
    )
    return brightness(TMP_CAMERA_IMAGE)


def run_once(config, plugins):
    ambient_brightness = get_ambient_brightness()

    print ambient_brightness

    for plugin in plugins:
        plugin.process(ambient_brightness)

    return True

def init_plugins(config):
    return (
        ScreenBrightnessPlugin(config.get('screen_brightness', {})),
        ThinkpadKeyboardBrightnessPlugin(config.get('keyboard_brightness', {}))
    )

def run(config):
    samplerate = config['samplerate']

    plugins = init_plugins(config)

    while True:
        run_once(config, plugins)
        time.sleep(samplerate)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process ambient light.')
    parser.add_argument('--config', dest='config', action='store',
                        default=None,
                        help='Config file to use.')

    args = parser.parse_args()

    if not args.config:
        config_file = CONFIG_FILE_PATH
        init_default_config(config_file)
    else:
        config_file = args.config

    with open(config_file) as fp:
        config = json.load(fp)

    run(config)
