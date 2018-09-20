import time
from selenium import webdriver

browser = webdriver.Chrome(executable_path='./chromedriver')
browser.get('https://piazza.com/')
browser.find_element_by_id("login_button").click()

#get the login page handle
for handle in browser.window_handles:
    browser.switch_to_window(handle)
browser.find_element_by_id("email_field").send_keys("keyangru@usc.edu")
browser.find_element_by_name("password").send_keys("r12345678")
browser.find_element_by_id("modal_login_button").click()


for i in range(6,9): #choose the post number you want
    browser.get("https://piazza.com/class/isccqbm3kzy7kq?cid=" + str(i))
    time.sleep(2)
    title = browser.find_element_by_xpath("//h1[@data-pats='title_text']")
    text = browser.find_element_by_xpath("//div[@id='questionText']")
    author = browser.find_element_by_xpath("//div[@data-pats='updated_text']")
    print("============== post ============")
    print("Title: " + title.text)
    print("No: " + str(i))
    names = author.find_elements_by_class_name("user_name")
    if len(names) == 0:
        print("Author: " + "Anonymous")
    else:
        for name in names:
            print("Author: " + name.text)
    print("Text:" + text.text)

    selected_answers = browser.find_elements_by_id("s_answer")
    for selected_answer in selected_answers:
        print("============== selected answers ============")
        names = selected_answer.find_elements_by_class_name("user_name")
        if len(names) == 0:
            print("Author: " + "Anonymous")
        else:
            for name in names:
                print("name: " + name.text)
        print("text: " + selected_answer.find_element_by_class_name("post_region_text").text)


    contents = browser.find_elements_by_xpath("//div[@data-pats='followup']")
    for content in contents:
        print("======== discussions =======")
        name = content.find_element_by_class_name("discussion_poster")
        text = content.find_element_by_class_name("actual_text")
        print("name: " + name.text)
        print("text: " + text.text)
        replies = content.find_elements_by_class_name("existing_reply")
        for reply in replies:
            print("    ======== reply ========")
            print("    name: " + reply.find_element_by_class_name("user_name").text)
            print("    text: " + reply.find_element_by_class_name("actual_reply_text").text)


browser.close()

