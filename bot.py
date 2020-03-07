from selenium import webdriver
import urllib.request
import os
import time
from collections import OrderedDict

class InstagramBot:
   def __init__(self,Order):
      print(Order)
      self.username = Order[0]
      self.password = Order[1]
      self.user = Order[2]
      self.Command = Order[3]
      self.basic_url= 'https://www.instagram.com'
      self.driver = webdriver.Chrome('chromedriver.exe')
      self.login()

   def login(self):
      self.driver.get('{}/accounts/login/'.format(self.basic_url))
      time.sleep(10)
      self.driver.find_element_by_name('username').send_keys(self.username)
      self.driver.find_element_by_name('password').send_keys(self.password)
      self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[4]').click()
      time.sleep(10)
      self.navigate_profile()

   def navigate_profile(self):
      self.driver.get('{}/{}/'.format(self.basic_url,self.user))
      time.sleep(5)
      #self.follow_profile()
      #self.photo_liker()
      self.worker()
   
   def worker(self):
      if(self.Command == '0000' or self.Command == '1100'):
         print("what do you really wanna do???")
      elif(self.Command == '0011' or self.Command == '1111'):
         self.initiate_download_image()
         self.photo_liker()
      elif(self.Command == '0010' or self.Command == '1110'):
         self.photo_liker()
      elif(self.Command == '0001' or self.Command == '1101'):
         self.initiate_download_image()
      elif(self.Command == '1011'):
         self.follow_profile()
         self.initiate_download_image()
         self.photo_liker()
      elif(self.Command == '0111'):
         self.initiate_download_image()
         self.photo_liker()
         self.unfollow_profile()
      elif(self.Command == '1010'):
         self.follow_profile()
         self.photo_liker()
      elif(self.Command == '1001'):
         self.follow_profile()
         self.initiate_download_image()
      elif(self.Command == '0110'):
         self.photo_liker()
         self.unfollow_profile()
      elif(self.Command == '0101'):
         self.initiate_download_image()
         self.unfollow_profile()
      elif(self.Command == '0100'):
         self.unfollow_profile()
      else:
         self.follow_profile()
      self.driver.close() 
      
         

        
    
   def follow_profile(self):
      follow_button = self.driver.find_element_by_xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "_6VtSN", " " ))]')
      follow_button.click()
      time.sleep(5)
    
   def initiate_download_image(self):
      img_srcs = []
      finished = False
      while not finished:

         finished = self.bottom_scroll()

         img_srcs.extend([img.get_attribute('src') for img in self.driver.find_elements_by_class_name('FFVAD')]) 

      img_srcs = list(OrderedDict.fromkeys(img_srcs))

      for index, src in enumerate(img_srcs):
         self.download_image(src, index, self.user)
        
      self.top_scroll()
        
   def download_image(self, src, image_filename, folder):
      folder_path = './{}'.format(folder)
      if not os.path.exists(folder_path):
         os.mkdir(folder_path)

      urllib.request.urlretrieve(src, '{}/{}'.format(folder, 'image_{}.jpg'.format(image_filename)))


   def bottom_scroll(self):
        
      SCROLL_PAUSE_TIME = 5

      self.last_height = self.driver.execute_script("return document.body.scrollHeight")

      self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

      time.sleep(SCROLL_PAUSE_TIME)

      self.new_height = self.driver.execute_script("return document.body.scrollHeight")


      if self.new_height == self.last_height:
         return True

      self.last_height = self.new_height
      return False

   def top_scroll(self):
      SCROLL_PAUSE_TIME = 1
      self.last_height = self.driver.execute_script("return document.body.scrollHeight")
      self.driver.execute_script("window.scrollTo(document.body.scrollHeight,0);")
      time.sleep(SCROLL_PAUSE_TIME)
      self.new_height = self.driver.execute_script("return document.body.scrollHeight")
      if self.new_height == self.last_height:
         return True
      self.last_height = self.new_height
      return False
    
    
   def unfollow_profile(self):
      finished = False
      while not finished:
         finished = self.top_scroll()
      unfollow_button = self.driver.find_elements_by_xpath("//*[text()='{}']".format('Following'))
      unfollow_button[0].click()
      time.sleep(2)
      unfollow_confirm = self.driver.find_element_by_xpath('/html/body/div[3]/div/div/div[3]/button[1]')
      unfollow_confirm.click()
      time.sleep(10)
      
    
   
   def photo_liker(self):
      self.driver.find_elements_by_class_name('_9AhH0')[0].click()
      time.sleep(5)
      self.driver.find_element_by_xpath("//*[@aria-label='{}']".format('Like')).click()
      time.sleep(5)
      self.driver.execute_script("window.history.go(-1)")
      time.sleep(5)







