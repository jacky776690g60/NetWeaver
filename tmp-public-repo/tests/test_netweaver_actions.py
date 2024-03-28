"""
Make sure you have internet
"""
import unittest, warnings
from unittest import skipIf

from netweaver.netweaver import NetWeaver, By, ActionChains, TimeoutException, EnhancedWebElement
from netweaver.utility import *
from netweaver.utility import Script

class TestNetWeaver(unittest.TestCase):
    
    TEST_SCROLLING              = False #TODO: Need more testing
    
      
    def setUp(self):
        warnings.simplefilter("ignore", category=ResourceWarning)
    
    
    # =========================================================================
    # Test cases
    # =========================================================================
    # --
    # Proxy
    # ----------------------------
    @skipIf(not TEST_SCROLLING, "")
    def test_scroll_end_of_page(self):
        nw = NetWeaver(
            "https://www.wikipedia.org/",
            # use_headless = False,
            init_pos     = (850, 0),
            # window_size  = DesktopSize.FHD.value,
            use_sandbox  = True,
            incognito    = True,
        )
        print("Testing scroll to page bottom.")
        body = nw.get_elements_by_xpath("//body")[0]
        nw.scroll_to_window_scrollHeight()
        nw.sleep(1)
        print(nw.bot.execute_script(Script.get_element_scrollTop(), body))
        print(nw.bot.execute_script(Script.get_element_scrollHeight(), body))
    
    
if __name__ == '__main__':
    unittest.main()