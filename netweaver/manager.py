"NetWeaver manager for multithreading"

""" =================================================================
| manager.py -- NetWeaver/netweaver/manager.py
|
| Created by Jack on 07/11/2023
| Copyright © 2023 jacktogon. All rights reserved.
================================================================= """

import threading, time, os, sys
from typing import *

from pytools import Logger, LogLevel, TermArtist

from .netweaver import *
from .utility import *

__all__ = 'WeaversManager',

class WeaversManager():
    def __init__(self) -> None:
        raise NotImplementedError("Not yet implement")

def _run_netweaver_instance(
    root_url: str, 
    position: Tuple[int, int]
) -> None:
    """
    A simple function to initialize and run a NetWeaver instance.
    This can be expanded to include more tasks.
    """
    nw = NetWeaver(root_url)
    nw.set_window_size(MobileSize.STANDARD)
    nw.position_window(*position)
    nw.driver.get(root_url)
    nw.sleep(5) 
    nw.driver.quit()




if __name__ == "__main__":
    urls = [
        "https://example1.com", 
        "https://example2.com", 
        "https://example3.com"
    ]
    
    threads = []
    for i, url in enumerate(urls):
        t = threading.Thread(
            target=_run_netweaver_instance, 
            args=(url, (500 * i, 100))
        )
        t.start()
        threads.append(t)
    
    # Wait for all threads to finish.
    for t in threads:
        t.join()

    print("All NetWeaver tasks completed!")
