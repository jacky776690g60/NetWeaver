"Utility module for NetWeaver"

""" =================================================================
| utility.py -- NetWeaver/netweaver/utility.py
|
| Created by Jack on 07/11/2023
| Copyright © 2023 jacktogon. All rights reserved.
================================================================= """


from enum import Enum
from typing import *

class DesktopSize(Enum):
    "Common desktop sizes."
    
    SMALL   = (1024, 768)
    "Standard 4:3 aspect ratio."
    HD      = (1280, 720)
    "HD resolution, 16:9 aspect ratio."
    FHD     = (1920, 1080)
    "Full HD resolution, 16:9 aspect ratio."
    QHD     = (2560, 1440)
    "Quad HD resolution, 16:9 aspect ratio."
    ULTRAHD = (3840, 2160)
    "Ultra HD resolution, also known as 4K, 16:9 aspect ratio."
    UWHD    = (2560, 1080)
    "Ultra Wide HD resolution, 21:9 aspect ratio."
    UWFHD   = (3440, 1440)
    "Ultra Wide Full HD resolution, 21:9 aspect ratio."
    UWQHD   = (3440, 1440)
    "Duplicate of UWFHD, Ultra Wide Quad HD resolution, 21:9 aspect ratio."
    UHDPLUS = (5120, 2160)
    "Ultra Wide 5K resolution, wider than 4K for extra workspace."


class MobileSize(Enum):
    "Common mobile sizes."
    
    
    STANDARD = (375, 667)
    "Standard iPhone resolution, common before iPhone 6."
    PLUS = (414, 736)
    "Plus iPhone resolution, used for larger iPhone models."
    XL = (412, 846)
    "XL size, slightly taller than Plus models."

    ANDROID_SMALL = (720, 1280)
    "Common smaller Android resolution."
    ANDROID_MEDIUM = (1080, 1920)
    "Common medium Android resolution."
    ANDROID_LARGE = (1440, 2560)
    "Common large Android resolution."
    GALAXYS10 = (1440, 3040)
    "Samsung Galaxy S10 resolution."
    GALAXYS20 = (1440, 3200)
    "Samsung Galaxy S20 resolution."
    PIXEL4 = (1080, 2280)
    "Google Pixel 4 resolution."
    PIXEL5 = (1080, 2340)
    "Google Pixel 5 resolution."

    RETINA_HD = (750, 1334)
    "Retina HD resolution, used for iPhone 6/6s/7/8."
    IPHONE11_12 = (828, 1792)
    "iPhone 11 and 12 standard resolution."
    IPHONE11PRO_12MINI = (1125, 2436)
    "iPhone 11 Pro and 12 Mini resolution."
    IPHONE11PROMAX_12PROMAX = (1242, 2688)
    "iPhone 11 Pro Max and 12 Pro Max resolution."
    IPHONE13MINI = (1080, 2340)
    "iPhone 13 Mini resolution."
    IPHONE13PRO = (1170, 2532)
    "iPhone 13 Pro resolution."
    IPHONE13PROMAX = (1284, 2778)
    "iPhone 13 Pro Max resolution."

    FHD_PLUS = (1080, 2340)
    "Full HD Plus resolution, common in newer high-end phones."