"Grab youtube subtitles"

""" =================================================================
| youtube_subtitle.py -- NetWeaver/apps/youtube_subtitle.py
|
| Created by Jack on 07/11/2023
| Copyright © 2023 jacktogon. All rights reserved.
================================================================= """

import argparse, sys
from pathlib import Path

from selenium.common.exceptions import TimeoutException

from netweaver.netweaver import *
from netweaver.enhancedwebelement import *

# =============================
# Uitlity
# =============================
def try_close_ad_popup(
    weaver: NetWeaver, 
    label: str, 
) -> None:
    try:
        btn = weaver.wait_get_xpath_elements_present(
            f'//button[@aria-label="{label}"]',
            timeout=.3,
        )
        weaver.try_click_elements(btn)
    except TimeoutException as e:
        print(f"[INFO] '{label}' button not found.")


# =============================
# Main Functions
# =============================
def main(
    url: str,
    save_path: str,
    headless=False,
    use_tab=False,
) -> None:
    nw = NetWeaver(
        url,
        timeout_range=[3., 6.],
        browser="chrome",
        use_headless=headless,
        incognito=True
    )
    nw.set_window_size(DesktopSize.SMALL)
    nw.position_window(0, 0)
    
    nw.wait_for_page_load()

    title_elem = nw.wait_get_xpath_elements_present(
        "//div[@id='title']//yt-formatted-string",
    )[0]
    title = title_elem.get_direct_text()
    
    try_close_ad_popup(nw, "No thanks")
    try_close_ad_popup(nw, "Dismiss")

    
    # action_menus = nw.wait_get_xpath_elements_present(
    #     '//button[@aria-label="More actions"]'
    # )
    # nw.try_click_elements(action_menus)


    # menu_items = nw.wait_get_xpath_elements_visible(
    #     '//ytd-menu-service-item-renderer'
    # )
    # for item in menu_items:
    #     elems = item.get_descendants_with_direct_text("Show transcript")
    #     if elems: elems[0].click()
    # nw.sleep(2.5)

    description = nw.wait_get_xpath_elements_present(
        "//div[@id='description']",
        timeout=10
    )[0]
    
    description.click()
    
    
    try_close_ad_popup(nw, "No thanks")
    try_close_ad_popup(nw, "Dismiss")
    
    
    show_transcript_btns = nw.wait_get_xpath_elements_present(
        "//button[@aria-label='Show transcript']",
    )
    nw.try_click_elements(show_transcript_btns)
    
    transcript_segments_container = nw.wait_get_xpath_elements_present(
        "//div[@id='segments-container' and @class='style-scope ytd-transcript-segment-list-renderer']",
        timeout=10
    )[0]

    save_path: Path = Path(save_path)
    save_path.parent.mkdir(parents=True, exist_ok=True)
    if not str(save_path).endswith('.txt'):
        save_path = save_path.with_suffix('.txt')

    caption_idx = 0
    
    # nw.bot.save_screenshot(Path("test/ss.png"))

    with open(save_path, "w") as f:
        delimiter = "\t" if use_tab else " " * 4
        
        f.write(f"# Transcripts for *{title}*\n\n")
        f.write(f"# Metadata:\n")
        f.write(f"caption_idx{delimiter}timestamp{delimiter}caption\n\n")
        
        for i, segment in enumerate(transcript_segments_container):
            if segment.tag_name == "ytd-transcript-section-header-renderer":
                formatted_str_elems = nw.wait_get_xpath_elements_present(
                    ".//yt-formatted-string",
                    segment
                )[0]
                line = f"### Chapter *{formatted_str_elems.get_direct_text()}*"
                f.write(line + '\n')

            elif segment.tag_name == "ytd-transcript-segment-renderer":
                timestamp = nw.wait_get_xpath_elements_present(
                    ".//div[@class='segment-timestamp style-scope ytd-transcript-segment-renderer']",
                    segment
                )[0]
                transcript = nw.wait_get_xpath_elements_present(
                    ".//yt-formatted-string",
                    segment
                )[0]
                cleaned = transcript.get_direct_text().replace('\n', '')
                line = f"{caption_idx}{delimiter}{timestamp.get_direct_text().strip()}{delimiter}{cleaned}"
                f.write(line + '\n')
            
            caption_idx += 1
        
            max_dots = 3
            dots = "." * (i % max_dots + 1)
            spaces = " " * (max_dots - i % max_dots)
            print(f'\r{dots}{spaces}\033[10C', end='', flush=True)
        print(f'\nTranscript saved to: {save_path}')
        nw.bot.quit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=
        "'Extracting generated subtitles from YouTube URL"
    )
    parser.add_argument("-u", "--youtube_url", type=str, metavar="", required=True,
                        help="URL of the YouTube video")
    parser.add_argument("-s", "--save_path", type=str, metavar="", required=True,
                        help="Where to save the transcript txt file")
    parser.add_argument("-hl", "--headless", action="store_true", default=False,
                        help="Use headless?")
    parser.add_argument("-t", "--use_tab", action="store_true", default=False,
                        help="Use tab as delimiter?")
    args = parser.parse_args()
    
    main(args.youtube_url, args.save_path, args.headless, args.use_tab)