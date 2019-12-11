from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
import os
import time
import unittest

class StrangerThings(unittest.TestCase):
    def setUp(self):
    #Call the webdriver and go to the URL
        self.driver = webdriver.Chrome()
        self.driver.get("http://immense-hollows-74271.herokuapp.com/")

    def test_create_item(self):
    #Create an item from Item Details. Upload an image, add a description and confirm creation

        try:
            image = wait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "inputImage")))
            image.send_keys(os.getcwd() + "/Images/image_to_add.jpg")
            text = self.driver.find_elements_by_class_name("form-control")[1]
            description = "Stranger Things 3: The Game is a beat 'em up game based on the third season of Stranger Things " \
                      "and is developed by BonusXP, Inc."
            text.send_keys(description)
            btn = self.driver.find_element_by_class_name("btn-success")
            btn.click()
            time.sleep(3)
            elements = self.driver.find_elements_by_class_name("story")
            self.assertEqual(elements.pop().text, description)
        finally:
            time.sleep(5)

    def test_delete_item(self):
    #Go to the item created and delete it. Confirm there is one less in the item's list.
        try:
            btn_groups = wait(self.driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "btn-group")))
            num_items = len(btn_groups)
            btn_group_last_ele = btn_groups[num_items-1]
            btn_delete = btn_group_last_ele.find_elements_by_class_name('btn')[1]
            btn_delete.click()

            btn_confirm = wait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "btn-primary")))
            btn_confirm.click()
            time.sleep(3)
            h1 = self.driver.find_element_by_tag_name("h1").text

            assert str(num_items-1) in h1
        finally:
            pass

    def test_edit_existing_item(self):
    #Go to the last item of the list, add a word at the end of description and confirm that it was added successfully
        try:
            btn_groups = wait(self.driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "btn-group")))

            num_items = len(btn_groups)
            btn_group_last_ele = btn_groups[num_items - 1]
            btn_edit = btn_group_last_ele.find_elements_by_class_name('btn')[0]
            btn_edit.click()

            new_word = "EDITED"
            description = self.driver.find_elements_by_class_name("story").pop().text + new_word
            input = self.driver.find_elements_by_class_name("form-control")[1]
            input.send_keys(new_word)
            btn = wait(self.driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "btn-primary")))
            btn.click()
            time.sleep(3)
            h1 = self.driver.find_element_by_tag_name("h1").text

            self.assertEqual(self.driver.find_elements_by_class_name("story").pop().text, description)
            assert str(num_items) in h1
        finally:
            pass

    def test_max_long(self):
    #Wrtite more than max long text in description and check if button Create Item is enabled
        try:
            text_area = wait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, "text")))
            max_long_text = "Tincidunt nibh faucibus cum est dis. Auctor ligula, diam scelerisque, duis cubilia urna. "\
                    "Lacus penatibus venenatis laoreet vehicula phasellus A, euismod lacus commodo fermentum adipiscing "\
                    "tincidunt felis, lobortis parturient torquent tempus aliquet Interdum pellentesque parturient "\
                    "vivamus. Enim blandit."
            text_area.send_keys(max_long_text)

            btn = self.driver.find_element_by_class_name("btn-success")
            assert btn.is_enabled() is False
        finally:
            pass

    def test_check_if_text_exist(self):
    #Check in the description's list if there is a text as given in the assignment
        try:
            stories = wait(self.driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "story")))

            found = False
            for story in stories:
                if story.text == 'Creators: Matt Duffer, Ross Duffer':
                    found = True
            assert found is True

        finally:
            pass

    def tearDown(self):
        self.driver.quit()