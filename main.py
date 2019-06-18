from os import environ

from selenium import webdriver

from selenium.webdriver.common.keys import Keys

def handle_section(section):
    for episode in section.find_elements_by_css_selector(".Episode ._content"):
        episode.click()
        breakpoint()

def main():
    driver = webdriver.Firefox()
    driver.get("https://www.howacarworks.com/login")

    email = driver.find_element_by_name("email")
    email.send_keys(environ["HACW_USERNAME"])
    email.send_keys(Keys.RETURN)

    driver.implicitly_wait(3)
    password = driver.find_element_by_name("password")
    password.send_keys(environ["HACW_PASSWORD"])
    password.send_keys(Keys.RETURN)

    sections = driver.find_elements_by_css_selector(".Section")
    for section in sections:
        handle_section(section)

    breakpoint()

if __name__ == "__main__":
    main()
