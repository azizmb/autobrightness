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


def init_default_config():
    home_path = os.getenv("HOME")
    config_folder_path = os.path.join(home_path, '.config')
    app_config_folder_path = os.path.join(home_path, '.config', 'wildguppy')
    config_file_path = os.path.join(app_config_folder_path, 'config.json')

    if os.path.exists(config_file_path):
        try:
            with open(config_file_path) as fp:
                config = json.load(fp)
        except:
            print "Error loading configuration"
    else:
        config_dir = os.path.dirname(config_file_path)
        if not os.path.exists(config_dir):
            os.makedirs(config_dir)
        with open(config_file_path, 'w') as fp:
            json.dump(default_config, fp)
        config = default_config


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
    plugins = (
        ScreenBrightnessPlugin(config.get('screen_brightness', {})),
        ThinkpadKeyboardBrightnessPlugin(config.get('keyboard_brightness', {}))
    )
    ambient_brightness = get_ambient_brightness()

    print ambient_brightness

    for plugin in plugins:
        plugin.process(ambient_brightness)

    return True


def run(config):
    samplerate = config['samplerate']

    while True:
        run_once(config)
        time.sleep(samplerate)



# if __name__ == "__main__":
#     run = False
#     args = sys.argv
#     if len(args) >= 2:
#         for i in xrange(len(args)):
#             error = True
#             if args[i] == "help" or args[i] == "--help" or args[i] == "-help" or args[i] == "-h":
#                 print "USAGE: autobrightness [OPTION]... [VALUE]...\n\n Adjusts a laptop's brightness automatically, by using camera samples taken at a user definable interval.\n\n -s, --set              set time between samples to your configuration file\n -t, --time             set time between samples for this session\n -x, --max              set maximium brightness level to the config file\n -n, --min              set minimium brightness level to the config file"
#                 sys.exit()

#             if args[i] == "-s" or args[i] == "--set":
#                 error = False
#                 try:
#                     float(args[i+1])
#                     config['samplerate'] = args[i+1]
#                     json.dump(config, open('config.json', 'w'))
#                     print "Your default time interval is now '%s' seconds\n" % args[i+1]
#                 except IndexError:
#                     error_msg(1, args[i])
#                     sys.exit()
#                 except ValueError:
#                     error_msg(3, args[i+1])
#                     sys.exit()

#             if args[i] == "-x" or args[i] == "--max":
#                 try:
#                     float(args[i+1])
#                     config['maxbrightness'] = args[i+1]
#                     json.dump(config, open('config.json', 'w'))
#                     print "Your maximium brightness value is now '%s'\n" % args[i+1]
#                 except IndexError:
#                     error_msg(1, args[i])
#                     sys.exit()
#                 except ValueError:
#                     error_msg(3, args[i+1])
#                     sys.exit()

#             if args[i] == "-n" or args[i] == "--min":
#                 try:
#                     float(args[i+1])
#                     config['minbrightness'] = args[i+1]
#                     json.dump(config, open('config.json', 'w'))
#                     print "Your minimium brightness value is now '%s'\n" % args[i+1]
#                 except IndexError:
#                     error_msg(1, args[i])
#                     sys.exit()
#                 except ValueError:
#                     error_msg(3, args[i+1])
#                     sys.exit()

#             if args[i] == "-t" or args[i] == "--time":
#                 error = False
#                 run = True
#                 try:
#                     arg = float(args[i+1])
#                     if arg < 0:
#                         print "Your sampling rate cannot be a negative number.  Resetting to default value of 5."
#                     else:
#                         samplerate = arg
#                 except IndexError:
#                     error_msg(1, args[i])
#                     sys.exit()
#                 except ValueError:
#                     error_msg(3, args[i+1])
#                     sys.exit()
#                 break
#             if args[i] == "-g" or args[i] == "--gui":
#                error = False
#                os.system("./panel_app.py")

#         if error:
#             error_msg(2, args[i])
#     else:
#         run = True

#     if run:
#         a = autoBrightness()
#         a.run()
