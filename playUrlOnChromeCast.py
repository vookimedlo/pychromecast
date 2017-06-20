from __future__ import print_function
import time
import pychromecast
import mimetypes

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("ChromeCast", help="ChromeCast Name")
parser.add_argument("URL", help="URL to be casted")
args = parser.parse_args()

# My chromecast names
# VooVideoCast@MyRoom
# VooVideoCast@LivingRoom

chromecasts = pychromecast.get_chromecasts()
print ([cc.device.friendly_name for cc in chromecasts]);

try:
    mime = mimetypes.guess_type(args.URL)[0]
    cast = next(cc for cc in chromecasts if cc.device.friendly_name == args.ChromeCast)  # raises a StopIteration exception 
    cast.wait()
    cast.quit_app()

    ## Following sleep is just a workaround, chromecast controller cannot be started flawlessly until the previous one is still being exexuted
    ## TODO: find a better way how to handle that
    time.sleep(3)
    
    mc = cast.media_controller
    mc.play_media(args.URL, mime);
    mc.block_until_active()

    print("URL", args.URL, "is casted to", args.ChromeCast, "with mime type", mime)

    ## Following sleep is just a workaround, python cannot quit its execution until the data are realy streamed by the chromecast controller
    ## TODO: find a better way how to handle that
    time.sleep(5)
except StopIteration:
    print("No suitable chromecast found")
except:
    print("Error")
