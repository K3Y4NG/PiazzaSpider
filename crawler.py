import time
from selenium import webdriver
import json
firefox_options = webdriver.FirefoxOptions()
firefox_options.add_argument('--headless')
browser = webdriver.Firefox(executable_path='./geckodriver', firefox_options=firefox_options)
browser.get('https://piazza.com')
browser.find_element_by_id("login_button").click()

#get the login page handle
for handle in browser.window_handles:
    browser.switch_to_window(handle)
browser.find_element_by_id("email_field").send_keys("keyangru@usc.edu")
browser.find_element_by_name("password").send_keys("r12345678")
browser.find_element_by_id("modal_login_button").click()

data = []
for i in range(6,885): #choose the post number you want
    try:
        browser.get("https://piazza.com/class/isccqbm3kzy7kq?cid=" + str(i))
        time.sleep(1)
        item = {}
        title = browser.find_element_by_xpath("//h1[@data-pats='title_text']")
        tag = browser.find_element_by_class_name("tag")
        text = browser.find_element_by_xpath("//div[@id='questionText']")
        update_text = browser.find_element_by_xpath("//div[@data-pats='updated_text']")
        #print("============== post ============")
        item["title"] = title.text
        #print("Title: " + title.text)
        item["number"] = str(i)
        print("No: " + str(i))
        #print("tag: " +str(tag.text))
        item["tag"] = tag.text
        post_time = update_text.find_element_by_tag_name("span")
        names = update_text.find_elements_by_class_name("user_name")
        time_field = post_time.get_attribute("title")
        item["time"] = time_field
        #print("Time: " + time_field)
        item["author"] = []
        if len(names) == 0:
            item["author"].append("Anonymous")
            #print("Author: " + "Anonymous")
        else:
            for name in names:
                item["author"].append(name.text)
                #print("Author: " + name.text)
        item["text"] = text.text
        #print("Text: " + text.text)

        student_answers = browser.find_elements_by_id("s_answer")
        item["student_answer"] = []
        for student_answer in student_answers:
            #print("============== student answers ============")
            names = student_answer.find_elements_by_class_name("user_name")
            answer_list = {}
            answer_list["author"] = []
            if len(names) == 0:
                answer_list["author"].append("Anonymous")
                #print("Author: " + "Anonymous")
            else:
                for name in names:
                    answer_list["author"].append(name.text)
                    #print("Author: " + name.text)
            post_time = student_answer.find_element_by_class_name("post_region_actions_meta").find_element_by_tag_name("span")
            time_field = post_time.get_attribute("title")
            answer_list["time"] = time_field
            #print("time: " + time_field)
            text = student_answer.find_element_by_class_name("post_region_text").text
            answer_list["text"] = text
            #print("text: " + text)
            item["student_answer"].append(answer_list)


        contents = browser.find_elements_by_xpath("//div[@data-pats='followup']")
        item["followup"] = []
        for content in contents:
            followup = {}
            #print("======== discussions =======")
            name = content.find_element_by_class_name("discussion_poster")
            text = content.find_element_by_class_name("actual_text")
            post_time = content.find_element_by_class_name("dicussion_meta").find_element_by_tag_name("span")
            followup["name"] = name.text
            #print("name: " + name.text)
            time_field = post_time.get_attribute("title")
            followup["time"] = time_field
            #print("time: " + time_field)
            followup["text"] = text.text
            #print("text: " + text.text)

            replies = content.find_elements_by_class_name("existing_reply")
            followup["replies"] = []
            for reply in replies:
                rep = {}
                #print("    ======== reply ========")
                name = reply.find_element_by_class_name("user_name")
                post_time = reply.find_element_by_class_name("dicussion_meta").find_element_by_tag_name("span")
                text = reply.find_element_by_class_name("actual_reply_text")
                rep["name"] = name.text
                #print("    name: " + name.text)
                time_field = post_time.get_attribute("title")
                rep["time"] = time_field
                #print("    time: " + time_field)
                rep["text"] = text.text
                #print("    text: " + text.text)
                followup["replies"].append(rep)
            item["followup"].append(followup)
        data.append(item)
    except Exception as e:
        print(e)

with open("data.json", 'w') as outfile:
    json.dump(data, outfile)



browser.close()
