from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys
import time
import os

MAX_WAIT=10

class NewVisitorTest(StaticLiveServerTestCase):

    def setUp(self):
        self.browser=webdriver.Firefox()
        staging_server=os.environ.get('STAGING_SERVER')
        if staging_server:
            self.live_server_url='http://'+staging_server
            
    def tearDown(self):
        self.browser.quit()

    def wait_for_row_in_list_table(self,row_text):
        start_time=time.time()
        while True:
            try:
                table=self.browser.find_element_by_id('id_list_table')
                rows=table.find_elements_by_tag_name('tr')
                self.assertIn(row_text,[row.text for row in rows])
                return
            except (AssertionError,WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
            time.sleep(0.5)

    def test_can_start_a_list_for_one_user(self):
        #伊迪丝听说有一个很酷的在线待办事项应用
        #他去看了这个应用的首页
        self.browser.get(self.live_server_url)

        #他注意到网页的标题和头部都包含“TO-DO”这个词
        self.assertIn( 'To-Do' ,self.browser.title)
        header_text=self.browser.find_element_by_tag_name('h1').text
        self.assertIn( 'To-Do' ,header_text)
        
        #应用邀请她输入一个待办事项
        inputbox=self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
        inputbox.get_attribute('placeholder'),
        'Enter a to-do item')

        #她在一个文本框中输入了“Buy peacock feathers” (购买孔雀羽毛)
        #伊迪丝的爱好是使用假蝇做饵钓鱼
        inputbox.send_keys('Buy peacock feathers')

        #她按回车键后，页面更新了
        #待办事项表格中显示了"1: Buy peacock feathers"
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1:Buy peacock feathers')
        
        #页面又显示了一个文本框，可以输入其他的待办事项
        #她输入了“Use peacock feathers to make a fly”(使用孔雀羽毛做假蝇)
        #伊迪丝做事很有条理
        inputbox=self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)

        #页面再次更新，他的清单中显示了两个待办事项
        self.wait_for_row_in_list_table('2:Use peacock feathers to make a fly')
        self.wait_for_row_in_list_table('1:Buy peacock feathers')


        #伊迪丝想知道这个网站是否会记住他的清单
        #他看到网站为他生成了一个唯一的URL
        #而且页面中有一些文字解说这个功能
        #self.fail('Finish the test!')

        #她访问那个URL,发现她的待办事项列表还在

        #她很满意，去睡觉了

    def test_multiple_users_can_start_lists_at_different_urls(self):
        #伊迪丝新建一个待办事项清单
        self.browser.get(self.live_server_url)
        inputbox=self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy peacock feathers')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1:Buy peacock feathers')

        #他注意到清单有个唯一的URL
        edith_list_url=self.browser.current_url
        self.assertRegex(edith_list_url,'/lists/.+')
        
        #现在一名叫做弗朗西斯的新用户访问了网站

        ##我们使用了新浏览器会话
        ##确保伊莉丝的信息不会从cookie中泄露出去
        self.browser.quit()
        self.browser=webdriver.Firefox()

        #弗朗西斯访问首页
        #页面看不到伊迪丝的清单
        self.browser.get(self.live_server_url)
        page_text=self.browser.find_element_by_tag_name('body').text
        self.assertNotIn( 'Buy peacock feathers' ,page_text)
        self.assertNotIn( 'make a fly' ,page_text)

        #弗朗西斯输入一个新待办事项，新建一个清单
        #他不像伊迪丝那样兴趣盎然
        inputbox=self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1:Buy milk')
        

        #弗朗西斯获得了他的唯一URL
        francis_list_url=self.browser.current_url
        self.assertRegex(francis_list_url,'/lists/.+')
        self.assertNotEqual(francis_list_url,edith_list_url)

        #这个页面还是没有伊迪丝的清单
        page_text=self.browser.find_element_by_tag_name('body').text
        self.assertNotIn( 'Buy peacock feathers' ,page_text)
        self.assertIn( 'Buy milk' ,page_text)
       
        #两人都很满意，然后去睡觉了
       
        
    def test_layout_and_styling(self):
        #伊迪丝访问首页
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024,768)

        #她看到输入框完美地居中显示
        inputbox=self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x']+inputbox.size['width']/2,
            512,
            delta=10
        )

        #她新建了一个清单，看到输入框仍完美地居中显示
        inputbox.send_keys('testing')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1:testing')
        inputbox=self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x']+inputbox.size['width']/2,
            512,
            delta=10
        )
        
        


