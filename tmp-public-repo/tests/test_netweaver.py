"""
Make sure you have internet
"""
import unittest, warnings
from unittest import skipIf

from netweaver.netweaver import NetWeaver, By, ActionChains, TimeoutException, EnhancedWebElement
from netweaver.utility import *

class TestNetWeaver(unittest.TestCase):
    
    TEST_PROXY              = False #TODO: False b/c Proxy is not working properly yet
    TEST_INIT               = True
    TEST_GETSET             = True
    TEST_POS_WINDOW         = True
    TEST_ELEM               = True
    
      
    def setUp(self):
        warnings.simplefilter("ignore", category=ResourceWarning)
    
    
    # =========================================================================
    # Test cases
    # =========================================================================
    # --
    # Proxy
    # ----------------------------
    @skipIf(not TEST_PROXY, "")
    def test_proxy(self):
        nw = NetWeaver(
            "https://www.google.com/search?q=what+is+my+ip&sca_esv=575477965&rlz=1C5CHFA_enUS981US981&sxsrf=AM9HkKlk7yYE5f-CQ9dCjc2hgK8YIV2C8Q%3A1697913038731&ei=zhg0ZeGjLPvJkPIPjMKiuAo&ved=0ahUKEwjhwqH84oeCAxX7JEQIHQyhCKcQ4dUDCBA&uact=5&oq=what+is+my+ip&gs_lp=Egxnd3Mtd2l6LXNlcnAiDXdoYXQgaXMgbXkgaXAyChAAGIoFGLEDGEMyCBAAGIoFGJECMgcQABiKBRhDMggQABiKBRiRAjIHEAAYigUYQzIHEAAYigUYQzIFEAAYgAQyBRAAGIAEMgUQABiABDIFEAAYgARI1ChQtARYnCdwCngBkAEAmAGZAqABjRCqAQU4LjUuM7gBA8gBAPgBAagCC8ICChAAGEcY1gQYsAPCAg0QABiKBRixAxiDARhDwgINEC4YigUYxwEY0QMYQ8ICCxAuGIAEGLEDGIMBwgIOEC4YgAQYsQMYxwEY0QPCAgYQswEYhQTCAhYQABgDGI8BGOUCGOoCGLQCGIwD2AEBwgIREC4YgAQYsQMYgwEYxwEY0QPCAgsQABiABBixAxiDAcICCxAAGIoFGLEDGIMBwgIIEAAYgAQYsQPCAggQABiABBjJA8ICCBAAGIoFGJID4gMEGAAgQYgGAZAGCLoGBAgBGAo&sclient=gws-wiz-serp",
            use_headless = False,
            use_sandbox  = True,
            incognito    = True,
            proxy="27.79.54.108:10004"
        )
        divs = nw.get_elements_by_xpath(
           "//div[@id='infoDiv']",
           timeout=5
        )
    
    
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~ constructor ~~~~~~~~~~~~~~~~~~~~~~~~~~~
    @skipIf(not TEST_INIT, "")
    def test_default_initialization(self):
        nw = NetWeaver(root_url="http://example.com", use_headless=True)
        self.assertEqual(nw.root_url, "http://example.com")
        self.assertEqual(nw.timeout_range, (2., 5.))

    @skipIf(not TEST_INIT, "")
    def test_custom_initialization(self):
        nw = NetWeaver("https://example.com", 
            window_size=(1920, 1080), 
            timeout_range=(3., 4.), 
            use_sandbox=True,
            use_headless=True,
            use_mobile=True,
        )
        self.assertEqual(nw.root_url, "https://example.com")
        self.assertEqual(nw.timeout_range, (3., 4.))


    # --
    # Getters & Setters
    # ----------------------------
    # ◼︎ timeout
    @skipIf(not TEST_GETSET, "")
    def test_invalid_timeout_range(self):
        with self.assertRaises(AssertionError):
            nw = NetWeaver(root_url="https://jacktogon.com", timeout_range=(6., 5.), use_headless=True)

    @skipIf(not TEST_GETSET, "")
    def test_min_timeout_getter(self):
        nw = NetWeaver(root_url="http://example.com", use_headless=True)
        self.assertEqual(nw.min_timeout, 2.)

    @skipIf(not TEST_GETSET, "")
    def test_max_timeout_getter(self):
        nw = NetWeaver(root_url="http://example.com", use_headless=True)
        self.assertEqual(nw.max_timeout, 5)

    @skipIf(not TEST_GETSET, "")
    def test_set_min_timeout_valid(self):
        nw = NetWeaver(root_url="http://example.com", use_headless=True)
        with self.assertRaises(ValueError):
            nw.min_timeout = 6.
        
        nw.min_timeout = 3.
        self.assertEqual(nw.min_timeout, 3.)

    @skipIf(not TEST_GETSET, "")
    def test_set_max_timeout_valid(self):
        nw = NetWeaver(root_url="http://example.com", use_headless=True)
        with self.assertRaises(ValueError):
            nw.max_timeout = .5
            
        nw.max_timeout = 6.
        self.assertEqual(nw.max_timeout, 6.)

    # ◼︎ sleep time
    @skipIf(not TEST_GETSET, "")
    def test_min_sleeptime_getter(self):
        nw = NetWeaver(root_url="http://example.com", use_headless=True)
        self.assertEqual(nw.min_sleep, .5)

    @skipIf(not TEST_GETSET, "")
    def test_max_sleeptime_getter(self):
        nw = NetWeaver(root_url="http://example.com", use_headless=True)
        self.assertEqual(nw.max_sleep, 1.75)

    @skipIf(not TEST_GETSET, "")
    def test_set_min_sleeptime_valid(self):
        nw = NetWeaver(root_url="http://example.com", use_headless=True)
        with self.assertRaises(ValueError):
            nw.min_sleep = 10.
            
        nw.min_sleep = .5
        self.assertEqual(nw.min_sleep, .5)

    @skipIf(not TEST_GETSET, "")
    def test_set_max_sleeptime_valid(self):
        nw = NetWeaver(root_url="http://example.com", use_headless=True)
        with self.assertRaises(ValueError):
            nw.max_sleep = 0.
        
        nw.max_sleep = 6.
        self.assertEqual(nw.max_sleep, 6.)
    

    # ~~~~~~~~~~~~~~~~~~~~~~~~~ window size ~~~~~~~~~~~~~~~~~~~~~~~~~
    @skipIf(not TEST_POS_WINDOW, "")
    def test_set_window_size(self):
        nw = NetWeaver(root_url="http://example.com", use_headless=True)
        
        w, h = MobileSize.STANDARD.value
        nw.set_window_size(MobileSize.STANDARD)
        self.assertEqual(nw.window_size[0], w)
        self.assertEqual(nw.window_size[1], h)
        
        w, h = DesktopSize.FHD.value
        nw.set_window_size(DesktopSize.FHD)
        self.assertEqual(nw.window_size[0], w)
        self.assertEqual(nw.window_size[1], h)
        
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~ attribute ~~~~~~~~~~~~~~~~~~~~~~~~~~~
    @skipIf(not TEST_ELEM, "")
    def test_visitble_element(self):
        nw = NetWeaver(root_url="https://jacktogon.com", use_headless=True)
        
        with self.assertRaises(TimeoutException):
            nw.get_elements_visible_by_xpath("//div[@id='colorcruise']")


if __name__ == '__main__':
    unittest.main()
