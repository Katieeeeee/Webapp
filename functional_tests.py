from selenium import webdriver
import unittest

class eLearningTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_page_will_start_and_display_the_home_page(self):
        self.browser.get('http://localhost:8000')
        
        self.assertIn ('eLearning', self.browser.title)

if __name__ == '__main__':
    unittest.main(warnings='ignore')
