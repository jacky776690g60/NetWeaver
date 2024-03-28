"""
Make sure you have internet
"""
import unittest, warnings
from unittest import skipIf

from netweaver.netweaver import NetWeaver, By, ActionChains, TimeoutException, EnhancedWebElement
from netweaver.utility import *

class TestNetWeaver(unittest.TestCase):
    
    TEST_CSS_STYLE          = True
    TEST_PSEUDO_ELEM        = True
    TEST_EXTERNAL_SOURCE    = True
    TEST_RETRIEVE_TEXT      = True
    TEST_RETRIEVE_FUNC      = True
    TEST_ACTIONCHAINS       = True
    TEST_JSON_SERIALIZABLE  = True
    TEST_ATTR               = True
    
    def setUp(self):
        warnings.simplefilter("ignore", category=ResourceWarning)
    
    # =========================================================================
    # Test cases
    # =========================================================================
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ CSS Style ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 
    @skipIf(not TEST_CSS_STYLE, "")
    def test_get_inline_style(self):
        nw = NetWeaver(
            root_url     = "https://jacktogon.com", 
            use_headless = True
        )
        div = nw.get_elements_by_xpath("//div[@id='landing']")[0]
        self.assertIsInstance(div.inline_style, dict, "inline css style is not a 'dict'")
        self.assertEqual(len(div.inline_style.keys()), 1, "got more than just inline-style")
        self.assertEqual(div.inline_style["display"], "block", "Incorrect inline_style")

    @skipIf(not TEST_CSS_STYLE, "")
    def test_set_inline_style(self):
        nw = NetWeaver(
            root_url     = "https://jacktogon.com",
            use_headless = True
        )
        div = nw.get_elements_by_xpath("//div[@id='landing']")[0]
        border_css = "1px solid yellow"
        div.set_inline_style(f"border: {border_css};", True)
        self.assertEqual(div.inline_style["display"], "block", "original inline style was replaced.")
        self.assertEqual(div.inline_style["border"], border_css, "inline style was not set correctly.")
        
    @skipIf(not TEST_CSS_STYLE, "")
    def test_is_displayed(self):
        nw = NetWeaver(
            root_url     = "https://jacktogon.com",
            use_headless = True
        )
        div = nw.get_elements_by_xpath("//div[@id='works']")[0]
        self.assertEqual(div.displayed, False, "getting incorrect value.")
       
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~ pseudo element ~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 
    @skipIf(not TEST_PSEUDO_ELEM, "")
    def test_pseudo_elements(self):
        nw = NetWeaver(
            "https://www.psiservice.com/student/login",
            use_headless = True,
            use_sandbox  = True,
            incognito    = True
        )
        nw.set_window_size(DesktopSize.HD)
        
        containers = nw.get_elements_by_xpath(
            "//div[@class='container']"
        )
        self.assertEqual(containers[0].has_pseudo_elem("after"),  True, "::after not found in container (maybe something changed on the website?)")
        self.assertEqual(containers[0].has_pseudo_elem("before"), True, "::before not found in container (maybe something changed on the website?)")
        
        font_size = containers[0].get_pseudo_elem_style("after")['font-size']
        self.assertEqual(
            any(unit in font_size for unit in ['px', 'em', 'rem']),
            True, 
            "no font unit found..."
        )
        
        no_pseudo_div = nw.get_elements_by_xpath(
            "//div[@class='page-wrapper light-gray-bg']"
        )[0]
        self.assertEqual(no_pseudo_div.has_pseudo_elem("after"),  False, "::after found in div (maybe something changed on the website?)")
        self.assertEqual(no_pseudo_div.has_pseudo_elem("before"), False, "::before found in div (maybe something changed on the website?)")
        
    # ~~~~~~~~~~~~~~~~~~~~~~~ fetch external sources ~~~~~~~~~~~~~~~~~~~~~~~
    @skipIf(not TEST_EXTERNAL_SOURCE, "")
    def test_fetch_external_resource(self):
        nw = NetWeaver(
            "https://jacktogon.com",
            use_headless = True,
            use_sandbox  = True,
            incognito    = True
        )
        antler_img = nw.get_elements_by_xpath(
            "//img[@id='profile_img_burn']",
            timeout=1
        )[0]
        fetch_from_element = antler_img.fetch_from_src()
        direct_fetch       = nw.fetch_external_resource("https://jacktogon.com/resources/imgs/smoke_profile/elk_antler.png")
        assert fetch_from_element == direct_fetch, "Fetching external source encountered error"


    # ~~~~~~~~~~~~~~~~~~~~~~~~ retrieve text ~~~~~~~~~~~~~~~~~~~~~~~~
    @skipIf(not TEST_RETRIEVE_TEXT, "")
    def test_text_from_all_and_from_self(self):
        nw = NetWeaver(
            "https://coolors.co/",
            use_headless = True,
            use_sandbox  = True,
            incognito    = True,
            use_mobile   = True   #NOTE: using it to bypass Cloudflare
        )
        home_a_tag = nw.get_element_by_id("homepage_hero_text_title")
        self.assertEqual(
            home_a_tag.get_direct_text_forward_lineage(), "The super  fast  color palettes generator!",
            "Did not get all texts from self and descendants"
        )
        self.assertEqual(
            home_a_tag.get_direct_text_self(), "The super   color palettes generator!",
            "Did not get texts from just self"
        )


    # ~~~~~~~~~~~~~~~~~~~ retrieving functions ~~~~~~~~~~~~~~~~~~~    
    @skipIf(not TEST_RETRIEVE_FUNC, "")
    def test_get_descendants_with_direct_text(self):
        nw = NetWeaver(
            "https://jacktogon.com",
            use_headless = True,
            use_sandbox  = True,
            use_mobile   = True
        )
        nw.set_window_size(DesktopSize.FHD)
        linkTree = nw.get_elements_by_xpath(
            "//ul[@class='link_tree']",
            timeout=3
        )
        self.assertTrue(all(elem.get_direct_text_self() == "LinkedIn" for elem in linkTree[0].get_descendants_with_direct_text("LinkedIn", True)))
        self.assertTrue(all(elem.get_direct_text_self() == "LinkedIn" for elem in linkTree[0].get_descendants_with_direct_text("linkeDIN", False)))
        self.assertEqual(len(linkTree[0].get_descendants_with_direct_text("lInkEdIn", False)), 1)
        self.assertEqual(len(linkTree[0].get_descendants_with_direct_text("lInkEdIn", True)), 0)


    @skipIf(not TEST_RETRIEVE_FUNC, "")
    def test_immediate_siblings(self):
        nw = NetWeaver(
            "https://jacktogon.com",
            use_headless = True,
            use_sandbox  = True,
            incognito    = True
        )
        name_label = nw.get_elements_by_xpath("//label[@for='name']")[0]
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
            nw.get_elements_visible_by_xpath(
                "//form[@action='/submit']"
            )
        contact_btn = nw.get_elements_by_xpath(
            "//div[@id='navbar_curtain']/a[3]"
        )[0]
        contact_btn.click()
        nw.get_elements_visible_by_xpath(
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
        cat_btn = nw.get_elements_by_xpath(
            "//div[@id='colorcruise']//button[contains(@class, 'catBtn')]"
        )[0]
        attrs = cat_btn.data_attributes
        self.assertEqual(attrs['data-background'], 'black')

    
    # ~~~~~~~~~~~~~~~~~~~~~~~~ Action Chains ~~~~~~~~~~~~~~~~~~~~~~~~
    @skipIf(not TEST_ACTIONCHAINS, "")
    def test_native_drag_and_drop(self):
        nw = NetWeaver(
            "https://the-internet.herokuapp.com/drag_and_drop",
            use_headless = True,
            use_sandbox  = True,
            incognito    = True,
        )
        column_a = nw.get_elements_by_xpath(
            "//div[@id='column-a']"
        )[0]
        
        def get_columnA_header():
            nonlocal column_a
            return nw.get_elements_by_xpath(
                    "./header",
                    column_a
                )[0]
            
        self.assertEqual(get_columnA_header().get_direct_text_self(), "A")
        
        source_element: EnhancedWebElement = nw.bot.find_element(By.ID, 'column-a')
        target_element: EnhancedWebElement = nw.bot.find_element(By.ID, 'column-b')
        ActionChains(nw.driver).drag_and_drop(
            source_element, target_element
        ).perform()
        
        self.assertEqual(get_columnA_header().get_direct_text_self(), "B")
    
    
    @skipIf(not TEST_ACTIONCHAINS, "")
    def test_drag_and_drop(self):
        nw = NetWeaver(
            "https://the-internet.herokuapp.com/drag_and_drop",
            use_headless = True,
            use_sandbox  = True,
            incognito    = True,
        )
        column_a = nw.get_elements_by_xpath(
            "//div[@id='column-a']"
        )[0]
        column_a.highlight(revert_timeout=1)
        
        def get_columnA_header():
            nonlocal column_a
            return nw.get_elements_by_xpath(
                    "./header",
                    column_a
                )[0]
            
        self.assertEqual(get_columnA_header().get_direct_text_self(), "A")
        
        source_element = nw.bot.find_element(By.ID, 'column-a')
        target_element = nw.bot.find_element(By.ID, 'column-b')
        source_element.drop_on(target_element)
        
        self.assertEqual(get_columnA_header().get_direct_text_self(), "B")
        
        
    # ~~~~~~~~~~~~~~~~~~~~~~~ JSON Serializable ~~~~~~~~~~~~~~~~~~~~~~~
    @skipIf(not TEST_JSON_SERIALIZABLE, "")
    def test_json_serializable(self):
        nw = NetWeaver(
            "https://www.joaoverissimo.work/contact",
            use_headless = False,
            use_sandbox  = True,
            incognito    = True,
        )
        name_input = nw.get_elements_by_xpath("//input[@name='Name']")[0]
        name_input.set_attribute('value', 'jack')
        self.assertEqual(name_input.get_attribute('value'), 'jack', "Attribute value is not set")

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~ Attribute ~~~~~~~~~~~~~~~~~~~~~~~~~~
    @skipIf(not TEST_ATTR, "")
    def test_json_serializable(self):
        nw = NetWeaver(
            "https://jacktogon.com/",
            use_headless = True,
            use_sandbox  = True,
            incognito    = True,
        )
        btns = nw.get_elements_by_xpath(
            "//div[@id='colorcruise']//button"
        )
        self.assertEqual(btns[0].data_attributes['data-background'], 'black', "Did not get the correct data-attribute")
        assert len(btns[0].data_attributes.keys()) == 2, "Did not get all the `data-`"
        assert 'style' not in btns[0].data_attributes, "Get attribute other than just `data-`"


if __name__ == '__main__':
    unittest.main()
