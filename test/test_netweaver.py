"""
Make sure you have internet
"""
import unittest, warnings
from unittest import skipIf

from netweaver.netweaver import NetWeaver, By, ActionChains, TimeoutException, EnhancedWebElement
from netweaver.utility import *

class TestNetWeaver(unittest.TestCase):
    
    # ◼︎ Change this to bypass some test cases
    TEST_PROXY              = False
    
    TEST_INIT               = True
    TEST_GETSET             = True
    TEST_CONFIG             = True
    TEST_POS_WINDOW         = True
    TEST_RETRIEVE_FUNC      = True
    TEST_EXTERNAL_SOURCE    = True
    TEST_ACTIONCHAINS       = True
    TEST_JSON_SERIALIZABLE  = True
    
      
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
            use_headless=False,
            use_sandbox=True,
            incognito=True,
            proxy="27.79.54.108:10004"
        )
        divs = nw.wait_get_xpath_elements_present(
           "//div[@id='infoDiv']",
           timeout=5
        )
    
    
    # --
    # constructor
    # ----------------------------
    @skipIf(not TEST_INIT, "")
    def test_default_initialization(self):
        nw = NetWeaver(root_url="http://example.com", use_headless=True)
        self.assertEqual(nw.root_url, "http://example.com")
        self.assertEqual(nw.timeout_range, (2., 5.))

    @skipIf(not TEST_INIT, "")
    def test_custom_initialization(self):
        nw = NetWeaver("https://example.com", (1920, 1080), (3., 4.), use_headless=True)
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
    
    # --
    # reconfig
    # ----------------------------
    @skipIf(not TEST_CONFIG, "")
    def test_reconfiguration(self):
        nw = NetWeaver(
            "http://example.com",
            use_headless=True,
            use_mobile=False
        )
        old_driver = nw.bot
        self.assertEqual(id(old_driver), id(nw.bot), "Not same driver")
        
        nw.allow_CORS = True
        nw.config_driver_options()
        self.assertNotEqual(id(old_driver), id(nw.bot), "Still same driver")
        self.assertIn("--disable-web-security", nw.options.arguments, "Did not allow CORS")
    

    # --
    # window size
    # ----------------------------
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

    
    # --
    # retrieving functions
    # ----------------------------
    @skipIf(not TEST_RETRIEVE_FUNC, "")
    def test_get_direct_text(self):
        nw = NetWeaver(
            "https://www.artstation.com/blogs",
            use_headless=True,
            use_sandbox=True,
            use_mobile=True # bypass Cloudflare
        )
        nw.set_window_size(DesktopSize.FHD)
        mainMenuBtns = nw.wait_get_xpath_elements_present(
            "//button[@class='main-menu-bar-link dropdown-toggle-action']", 
            timeout=10
        )
        # print(nw.bot.page_source)
        self.assertEqual(mainMenuBtns[0].get_direct_text(), "")
        self.assertEqual(mainMenuBtns[0].text, "Explore")
        
        
    @skipIf(not TEST_RETRIEVE_FUNC, "")
    def test_get_descendants_with_direct_text(self):
        nw = NetWeaver(
            "https://jacktogon.com",
            use_headless=True,
            use_sandbox=True,
            use_mobile=True # bypass Cloudflare
        )
        nw.set_window_size(DesktopSize.FHD)
        linkTree = nw.wait_get_xpath_elements_present(
            "//ul[@class='link_tree']", 
            timeout=3
        )
        self.assertTrue(all(elem.get_direct_text() == "LinkedIn" for elem in linkTree[0].get_descendants_with_direct_text("LinkedIn", True)))
        self.assertTrue(all(elem.get_direct_text() == "LinkedIn" for elem in linkTree[0].get_descendants_with_direct_text("linkeDIN", False)))
        self.assertEqual(len(linkTree[0].get_descendants_with_direct_text("lInkEdIn", False)), 1)
        self.assertEqual(len(linkTree[0].get_descendants_with_direct_text("lInkEdIn", True)), 0)



    @skipIf(not TEST_RETRIEVE_FUNC, "")
    def test_pseudo_elements(self):
        nw = NetWeaver(
            "https://www.psiservice.com/student/login",
            use_headless=True,
            use_sandbox=True,
            incognito=True
        )
        nw.set_window_size(DesktopSize.HD)
        
        containers = nw.wait_get_xpath_elements_present(
            "//div[@class='container']"
        )
        self.assertEqual(containers[0].has_pseudo_elem("after"), True, "::after not found in container (maybe something changed on the website?)")
        self.assertEqual(containers[0].has_pseudo_elem("before"), True, "::before not found in container (maybe something changed on the website?)")
        
        font_size = containers[0].get_pseudo_elem_styles("after")['font-size']
        self.assertEqual(
            any(unit in font_size for unit in ['px', 'em', 'rem']),
            True, 
            "no font unit found..."
        )
        
        no_pseudo_div = nw.wait_get_xpath_elements_present(
            "//div[@class='page-wrapper light-gray-bg']"
        )[0]
        
        self.assertEqual(no_pseudo_div.has_pseudo_elem("after"), False, "::after found in div (maybe something changed on the website?)")
        self.assertEqual(no_pseudo_div.has_pseudo_elem("before"), False, "::before found in div (maybe something changed on the website?)")
        
    
    @skipIf(not TEST_RETRIEVE_FUNC, "")
    def test_immediate_siblings(self):
        nw = NetWeaver(
            "https://jacktogon.com",
            use_headless=True,
            use_sandbox=True,
            incognito=True
        )
        name_label = nw.wait_get_xpath_elements_present(
            "//label[@for='name']"
        )[0]
        self.assertEqual(name_label.immediate_sibling("after").tag_name, "input", "Elements not matching")


    @skipIf(not TEST_RETRIEVE_FUNC, "")
    def test_wait_visible(self):
        nw = NetWeaver(
            "https://jacktogon.com",
            use_headless=True,
            use_sandbox=True,
            incognito=True
        )
        with self.assertRaises(TimeoutException):
            nw.wait_get_xpath_elements_visible(
                "//form[@action='/submit']"
            )
        contact_btn = nw.wait_get_xpath_elements_present(
            "//div[@id='navbar_curtain']/a[3]"
        )[0]
        contact_btn.click()
        nw.wait_get_xpath_elements_visible(
            "//form[@action='/submit']"
        )


    @skipIf(not TEST_RETRIEVE_FUNC, "")
    def test_wait_visible(self):
        nw = NetWeaver(
            "https://jacktogon.com",
            use_headless=True,
            use_sandbox=True,
            incognito=True
        )
        cat_btn = nw.wait_get_xpath_elements_present(
            "//div[@id='colorcruise']//button[contains(@class, 'catBtn')]"
        )[0]
        attrs = cat_btn.data_attributes
        self.assertEqual(attrs['data-background'], 'black')



    # --
    # fetch external sources
    # ----------------------------
    @skipIf(not TEST_EXTERNAL_SOURCE, "")
    def test_fetch_external_resource(self):
        nw = NetWeaver(
            "https://jacktogon.com",
            use_headless=True,
            use_sandbox=True,
            incognito=True
        )
        antler_img = nw.wait_get_xpath_elements_present(
            "//img[@id='profile_img_burn']",
            timeout=1
        )[0]
        fetch_from_element = antler_img.fetch_from_src()
        direct_fetch = nw.fetch_external_resource("https://jacktogon.com/resources/imgs/smoke_profile/elk_antler.png")
        assert fetch_from_element == direct_fetch, "Fetching external source encountered error"



    
    
    # --
    # Action Chains
    # ----------------------------
    @skipIf(not TEST_ACTIONCHAINS, "")
    def test_native_drag_and_drop(self):
        nw = NetWeaver(
            "https://the-internet.herokuapp.com/drag_and_drop",
            use_headless=True,
            use_sandbox=True,
            incognito=True,
        )
        column_a = nw.wait_get_xpath_elements_present(
            "//div[@id='column-a']"
        )[0]
        
        def get_columnA_header():
            nonlocal column_a
            return nw.wait_get_xpath_elements_present(
                    "./header",
                    column_a
                )[0]
            
        self.assertEqual(get_columnA_header().get_direct_text(), "A")
        
        source_element = nw.bot.find_element(By.ID, 'column-a')
        target_element = nw.bot.find_element(By.ID, 'column-b')
        ActionChains(nw.driver).drag_and_drop(source_element, target_element).perform()
        
        self.assertEqual(get_columnA_header().get_direct_text(), "B")
    
    
    @skipIf(not TEST_ACTIONCHAINS, "")
    def test_drag_and_drop(self):
        nw = NetWeaver(
            "https://the-internet.herokuapp.com/drag_and_drop",
            use_headless=True,
            use_sandbox=True,
            incognito=True,
        )
        column_a = nw.wait_get_xpath_elements_present(
            "//div[@id='column-a']"
        )[0]
        column_a.highlight(revert_timeout=1)
        
        def get_columnA_header():
            nonlocal column_a
            return nw.wait_get_xpath_elements_present(
                    "./header",
                    column_a
                )[0]
            
        self.assertEqual(get_columnA_header().get_direct_text(), "A")
        
        source_element = nw.bot.find_element(By.ID, 'column-a')
        target_element = nw.bot.find_element(By.ID, 'column-b')
        source_element.drop_on(target_element)
        
        self.assertEqual(get_columnA_header().get_direct_text(), "B")
        
        
        
        
        
        
        
    @skipIf(not TEST_JSON_SERIALIZABLE, "")
    def test_drag_and_drop(self):
        nw = NetWeaver(
            "https://www.joaoverissimo.work/contact",
            use_headless=False,
            use_sandbox=True,
            incognito=True,
        )
        name_input = nw.wait_get_xpath_elements_present(
            "//input[@name='Name']"
        )[0]
        name_input.set_attribute('value', 'jack')
        assert name_input.get_attribute('value') == 'jack', "Attribute value is not set"
        
        

if __name__ == '__main__':
    unittest.main()
