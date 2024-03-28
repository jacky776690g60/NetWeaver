"""
Make sure you have internet
"""
import unittest, warnings
from unittest import skipIf
from pathlib import Path

from netweaver.netweaver import NetWeaver
from netweaver.utility import *

class TestNetWeaver(unittest.TestCase):
    
    TEST_INITIALIZATION          = True
    
    def setUp(self):
        # Suppress all warnings during test execution
        warnings.filterwarnings("ignore")
        
    def tearDown(self):
        # Attempt to close the browser if it's open
        try:
            self.nw.driver.quit()
        except AttributeError:
            # Handle the case where the test failed before the browser was initialized
            pass
    
    @skipIf(not TEST_INITIALIZATION, "")
    def test_init_undetected(self):
        try:
            self.nw = NetWeaver(
                root_url        = "https://example.com", 
                use_headless    = True,
                use_undetected  = True,
                binary_location = Path("./drivers/chrome/123.0.6262.0/chrome-mac-x64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing"),
                executable_path = Path("./drivers/chrome/123.0.6262.0/chromedriver-mac-x64/chromedriver")
            )
        except FileNotFoundError as e:
            raise FileNotFoundError("Driver and executable not found. Manually download it first.")
        
        
if __name__ == '__main__':
    unittest.main()