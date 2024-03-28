'This module will scrape and compare the targeted account\' followings and followers'
""" =================================================================
| ig_follower_scrape.py
|
| Created by Jack on 01/23, 2024
| Copyright © 2024 jacktogon. All rights reserved.
================================================================= """
import os, sys, argparse, time
from typing import *
from pathlib import Path

from selenium.common.exceptions import TimeoutException

import pandas as pd

from netweaver import *
from pytools import *
from pytools import TermArtist as ta

logger = Logger(Logger.debug)
SCROLL_SP = 3.0
'Scrolling speed. Adjust this based on your internet speed.'




def main(acc: str, pwd: str, k_acc: str, binary, driver):
    # ===================================================
    # Variables and General Functions
    # ===================================================
    ROOT_PATH     = Path("./output/ig_scraper")
    FR_CSV_PATH   = (ROOT_PATH / f"{k_acc}_followers.csv").resolve()
    FG_CSV_PATH   = (ROOT_PATH / f"{k_acc}_following.csv").resolve()
    COMP_CSV_PATH = (ROOT_PATH / f"{k_acc}_comparison.csv").resolve()
    HEADERS       = ['Datetime', 'username', 'alias', 'status']
    
    def write_csv(row_values: list, is_followers: bool):
        write_to_csv(
            headers    = HEADERS,
            row_values = row_values,
            file_path  = FR_CSV_PATH if is_followers else FG_CSV_PATH,
            overwrite  = False
        )
        
    def prompt_exit(question: str):
        if get_valid_input(f"{question.strip()} (Press any key or '{ta.FG.BRIGHT_RED}q{ta.RESET}' to stop): ", lambda x: x == 'q'): 
            sys.exit()
    
    NW = NetWeaver(
        root_url        = "https://www.instagram.com/",
        window_size     = (830, 1080),
        timeout_range   = (2, 3),
        init_pos        = (850, 0),
        use_undetected  = True,
        incognito       = True,
        binary_location = Path(binary).resolve(),
        executable_path = Path(driver).resolve()
    )
    NW.set_window_size(MobileSize.IPHONE11_12)
    
    # =============================
    # Logging in
    # =============================
    acc_input = NW.get_elements_by_xpath(
        "//input[@aria-label='Phone number, username, or email' and @type='text']"
    )[0]
    pwd_input = NW.get_elements_by_xpath(
        "//input[@aria-label='Password' and @type='password']"
    )[0]
    login_btn = NW.get_elements_by_xpath(
        "//button[@disabled and @type='submit']"
    )[0]
    acc_input.send_keys(acc)
    pwd_input.send_keys(pwd)
    login_btn.click()
    
    try:
        not_now_noti_btn = NW.get_elements_by_xpath(
            "//button[text()='Not Now']",
            timeout=5
        )[0]
        not_now_noti_btn.click()
    except TimeoutException as e:
        logger.debug("Didn't find `turn on Notification right now button`. Skipping it")
    except Exception as e:
        raise RuntimeError("Error on processing `Notification right now button`\n", e)
    
    prompt_exit("Logged in?")
    logger.info("Confirmed logged in.")
    
    # ===============================================
    # Scraping Followers
    # ===============================================
    NW.bot.get(f"https://www.instagram.com/{k_acc}/followers/")
    NW.wait_for_page_load()
    logger.info(f"Waiting for the {ta.FG.BRIGHT_MAGENTA}Followers{ta.RESET} section to pop up...")
    NW.sleep(5)
    
    frs_container = NW.get_elements_by_xpath(
        "//div[@style='display: flex; flex-direction: column; padding-bottom: 0px; padding-top: 0px; position: relative;']",
        timeout=10.
    )[1]
    prompt_exit("Did at least one follower show up?")
    
    logger.info(f"Initially found {len(frs_container)} followers.")
    # ~~~~~~~~~~~~~~~~~ scrolling ~~~~~~~~~~~~~~~~~
    cached_len = -1
    while cached_len != len(frs_container):
        cached_len = len(frs_container)
        last_child = frs_container[-1]
        NW.scroll_to_element(last_child)
        NW.sleep(SCROLL_SP, "waited for followers to load")
    logger.info(f"Finished scrolling. {ta.FG.BRIGHT_CYAN}Found followers: {cached_len}{ta.RESET}")
    
    write_csv(['' for _ in range(4)], is_followers=True) # start with empty record first
    existing_frs_df  = pd.read_csv(FR_CSV_PATH, dtype=str)
    existing_frs_set = set(existing_frs_df[HEADERS[1]])
    
    scrapped_frs = []
    new_frs      = []
    for row in frs_container:
        row: UCEnhancedWebElement
        
        spans = row.get_relative_elements_xpath(".//span")
        usr_info = [] # username, alias
        for sp in spans:
            if (txt:= sp.get_direct_text_self()): usr_info.append(txt)
        if len(usr_info) < 2: usr_info.append('') # If no alias, append empty
        
        status = 'still a follower' if usr_info[0] in existing_frs_set else 'new follower'
        
        row = [TimeConverter.unix_to_datestring(time.time()), *usr_info, status]
        if not usr_info[0] in existing_frs_set: new_frs.append(row)
        scrapped_frs.append(row)

    no_longer_frs_set = existing_frs_set - set([u[1] for u in scrapped_frs])
    for username in existing_frs_set:
        existing_frs_df.loc[existing_frs_df['username'] == username, 'status'] = 'still a follower'
    for username in no_longer_frs_set:
        existing_frs_df.loc[existing_frs_df['username'] == username, 'status'] = 'no longer'
            
    new_frs_df      = pd.DataFrame(new_frs, columns=HEADERS)
    existing_frs_df = pd.concat([existing_frs_df, new_frs_df], ignore_index=True)
    existing_frs_df.dropna(subset=['Datetime'], inplace=True)
    existing_frs_df.to_csv(FR_CSV_PATH, index=False, mode='w', encoding='utf-8')
    logger.info("Updated follower status in the csv file.")
    # ===============================================
    # Scraping Followings
    # ===============================================
    NW.bot.get(f"https://www.instagram.com/{k_acc}/following/")
    NW.wait_for_page_load()
    logger.info(f"Waiting for the {ta.FG.BRIGHT_MAGENTA}Following{ta.RESET} section to pop up...")
    NW.sleep(5)
    
    following_container = NW.get_elements_by_xpath(
        "//div[@style='display: flex; flex-direction: column; padding-bottom: 0px; padding-top: 0px; position: relative;']",
        timeout=10.
    )[1]
    prompt_exit("Did at least one following show up?")

    logger.debug(f"Initially found {len(following_container)} following.")
    # ~~~~~~~~~~~~~~~~~~ scrolling ~~~~~~~~~~~~~~~~~~
    cached_len = -1
    while cached_len != len(following_container):
        cached_len = len(following_container)
        last_child = following_container[-1]
        NW.scroll_to_element(last_child)
        NW.sleep(SCROLL_SP, "waited for following to load")
    logger.info(f"Finished scrolling. {ta.FG.BRIGHT_CYAN}Found following: {cached_len}{ta.RESET}")


    write_csv(['' for _ in range(4)], is_followers=False) # start with empty record first
    existing_fgs_df  = pd.read_csv(FG_CSV_PATH, dtype=str)
    existing_fgs_set = set(existing_fgs_df[HEADERS[1]])        
    
    scrapped_fgs = []
    new_fgs      = []
    for row in following_container:
        row: UCEnhancedWebElement
        
        spans = row.get_relative_elements_xpath(".//span")
        usr_info = [] # username, alias
        for sp in spans:
            if (txt:= sp.get_direct_text_self()): usr_info.append(txt)
        if len(usr_info) < 2: usr_info.append('') # If no alias, append empty
        
        status = 'still following' if usr_info[0] in existing_fgs_set else 'new following'
        
        row = [TimeConverter.unix_to_datestring(time.time()), *usr_info, status]
        if not usr_info[0] in existing_fgs_set: new_fgs.append(row)
        scrapped_fgs.append(row)
    
    no_longer_fgs_set = existing_fgs_set - set([u[1] for u in scrapped_fgs])
    for username in existing_fgs_set:
        existing_fgs_df.loc[existing_fgs_df['username'] == username, 'status'] = 'still following'
    for username in no_longer_fgs_set:
        existing_fgs_df.loc[existing_fgs_df['username'] == username, 'status'] = 'no longer'
    
    new_fgs_df      = pd.DataFrame(new_fgs, columns=HEADERS)
    existing_fgs_df = pd.concat([existing_fgs_df, new_fgs_df], ignore_index=True)
    existing_fgs_df.dropna(subset=['Datetime'], inplace=True)
    existing_fgs_df.to_csv(FG_CSV_PATH, index=False, mode='w', encoding='utf-8')
    logger.info("Updated follower status in the csv file.")
    # =================================================
    # Comparing CSV files
    # =================================================
    # Filter out rows where 'status' is 'no longer' in both DataFrames
    existing_frs_df = existing_frs_df[existing_frs_df['status'] != 'no longer']
    existing_fgs_df = existing_fgs_df[existing_fgs_df['status'] != 'no longer']

    # Add a unique identifier column to each DataFrame
    existing_frs_df['source'] = 'frs'
    existing_fgs_df['source'] = 'fgs'

    # Merging the DataFrames
    merged = pd.merge(
        existing_frs_df, existing_fgs_df, 
        on='username', how='outer', 
        suffixes=('_frs', '_fgs')
    )
    # Function to classify relationship based on the new 'source' columns
    def classify_relationship(row):
        if pd.isna(row['source_fgs']):
            return '----'  # Only in followers
        elif pd.isna(row['source_frs']):
            return 'xxxx'  # Only in followings
        else:
            return 'oooo'  # In both
    # Apply the function to create the 'mutual' column
    merged['mutual'] = merged.apply(classify_relationship, axis=1)


    # Combining 'Datetime' and 'alias' columns
    merged['Datetime'] = merged['Datetime_frs'].combine_first(merged['Datetime_fgs'])
    merged['alias'] = merged['alias_frs'].combine_first(merged['alias_fgs'])

    # Creating the final DataFrame
    final_df = merged[['Datetime', 'username', 'alias', 'mutual']]
    final_df.to_csv(COMP_CSV_PATH, index=False, mode='w')
    logger.info("Finished comparing. Saved result to csv file.")



if __name__ == "__main__":    
    parser = argparse.ArgumentParser(description="Scrape an Instagram account followers and followings")
    parser.add_argument("-t", "--target_acc", required=True, type=str, help="The targeted Instagram account")
    args = parser.parse_args()
    
    user_data = JSONLoader.read_jsonc(Path("./config/ig_scraper_acc.jsonc"), ["accounts", "passwords", "chrome"])
    
    logger.info("Choose the account")
    for i, acc in enumerate(user_data["accounts"]):
        print(f'{ta.FG.GREEN}{i}.{ta.RESET}'.ljust(13), acc)
    acc_i = int(input(f"Enter a integer: {ta.FG.BRIGHT_GREEN}"))
    print(ta.RESET, end="")
    if not 0 <= acc_i < len(user_data["accounts"]): raise IndexError("Index out of range...")
    
    acc, pwd = user_data["accounts"][acc_i], user_data["passwords"][acc_i]
    logger.info(f"Using account {ta.FG.GREEN}{acc}{ta.RESET}")
    
    logger.warn(f"For future questions, enter '{ta.FG.BRIGHT_RED}q{ta.RESET}' to quit the process.")
    
    main(acc, pwd, args.target_acc, user_data["chrome"]["binary_location"], user_data["chrome"]["driver_executable"])
    