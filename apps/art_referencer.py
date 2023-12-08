"""
Provide a set of keywords and let the program auto garther image references 
from major platforms

You should properly cite your references if applicable
"""

""" =================================================================
| art_referencer.py -- Python/NetWeaver/apps/art_referencer.py
|
| Created by Jack on 07/11/2023
| Copyright © 2023 jacktogon. All rights reserved.
================================================================= """

import argparse, sys, traceback, re
import threading
import concurrent.futures
import json


from datetime import datetime
from typing import *
from pathlib import Path

from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException
from selenium.webdriver.common.keys import Keys

from netweaver.netweaver import *
from netweaver.enhancedwebelement import EnhancedWebElement

from tools.logger import *
from tools.termartist import TermArtist as ta

LOGGER = Logger(LogLevel.DEBUG)



def main():
    parser = argparse.ArgumentParser(description=
        "'Auto find image references based on keywords"
    )
    parser.add_argument("-k", "--keywords", type=str, metavar="", required=True,
                        help="Keywords, seperated by 'comma'")
    parser.add_argument("-s", "--save_path", type=str, metavar="", required=True,
                        help="A root folder to save the img files")
    parser.add_argument("-hl", "--headless", action="store_true", default=False,
                        help="Use headless?")
    args = parser.parse_args()
    
    KEYWORDS        = str(args.keywords).split(",")
    SAVE_PATH       = Path(args.save_path) if args.save_path else Path("output/")
    HEADLESS: bool  = args.headless
    
    if not SAVE_PATH.exists():
        LOGGER.info("Creating the save path: ", SAVE_PATH, start=ta.Foreground.GREEN)
        SAVE_PATH.mkdir(parents=True, exist_ok=True)


    LOGGER.info(f"Searching keywords: {' | '.join(KEYWORDS)}")


    
    nw = NetWeaver(
        "https://jacktogon.com",
        window_size=(1000, 1080),
        timeout_range=(2., 4.),
        init_pos=(670, 0),
        use_headless=HEADLESS,
        use_sandbox= True,
        incognito= True,
        use_undetected=True
    )
    
    def scroll_to_bottom(num):
        for _ in range(num): nw.scroll_to_page_bottom(); nw.sleep(1);
        

    def search_artstation():
        for keyword in KEYWORDS:
            nw.bot.get("https://www.artstation.com/search")
            search_bar = nw.wait_get_xpath_elements_present(
                "//input[@type='search' and contains(@class, 'search-block-input ng-untouched ng-pristine ng-valid')]",
                timeout=10
            )[0]
            search_bar.send_keys(keyword)
            nw.wait_for_page_load(verbose=True)
            
            # scroll_to_bottom(1)
            
            img_blocks = nw.wait_get_xpath_elements_present(
                "//a[@target='_blank' and contains(@class, 'gallery-grid-link')]"
            )
            pages = [img_block.get_property("href") for img_block in img_blocks]
            
            
            
            def fetch_image(save_path, page_i, keyword, img, img_i):
                cleaned_url = img.get_property("src").split("?")[0]
                try:
                    content = nw.fetch_external_resource(cleaned_url)
                except RuntimeError:
                    LOGGER.debug("Skipping Forbidden: {}".format(cleaned_url))
                    return

                filename = f"AS_{keyword}_{page_i}_{img_i}_{cleaned_url.split('/')[-1]}"
                with open(save_path / filename, 'wb') as f:
                    f.write(content)
                    LOGGER.info("Saved: {}".format(filename))


            def fetch_images_from_page(page_i, page, save_path, keyword):
                nw.sleep(1.5)
                imgs = nw.wait_get_xpath_elements_present("//img[contains(@class, 'img img-fluid')]")

                with concurrent.futures.ThreadPoolExecutor() as executor:
                    futures = {executor.submit(fetch_image, save_path, page_i, keyword, img, img_i): img for img_i, img in enumerate(imgs)}
                    for future in concurrent.futures.as_completed(futures):
                        future.result()
            
            
            
            
            
            
            
            
            
            
            
            
            
            for page_i, page in enumerate(pages):
                nw.bot.get(page)
                nw.sleep(.5)
                fetch_images_from_page(page_i, page, SAVE_PATH, keyword)
            # sys.exit()
            # input("Press enter to continue to next keyword ")
            
            
    def search_pinterest():
        for keyword in KEYWORDS:
            search_query = "%20".join(keyword.split(" "))
            nw.bot.get(f"https://www.pinterest.com/search/pins/?q={search_query}&rs=typed")
    
            idx = 0
            
            for _ in range(3):
                scroll_to_bottom(1)
                
                img_blocks = nw.wait_get_xpath_elements_present(
                    "//img[@fetchpriority and @loading and @src]"
                )
                for img_block in img_blocks:
                    try: 
                        original_url = img_block.get_property("src").split("/")
                    except TypeError as e:
                        LOGGER.warn(e)
                        continue
                    url_strs = original_url[:3] + ["originals"] + original_url[4:]
                    img_url = "/".join(url_strs)
                    
                    try:
                        content = nw.fetch_external_resource(img_url)
                    except RuntimeError:
                        LOGGER.debug("Skipping Forbidden:", img_url)
                        continue
                    
                    filename = f"pin_{keyword}_{idx}_{img_url.split('/')[-1]}"
                    with open(SAVE_PATH / filename, 'wb') as f:
                        f.write(content)
                        LOGGER.info(filename)
                    idx += 1
                    
    
    try: 
        search_artstation()
        search_pinterest()
        
        
        
        
        
        pass
    except KeyboardInterrupt:
        LOGGER.warn("(Manually) Quitting application...", start="\r")
        nw.bot.quit()
        sys.exit()
        
    nw.bot.quit()
    LOGGER.info("Process completed.")
    
    
    
    

if __name__ == "__main__":
    main()