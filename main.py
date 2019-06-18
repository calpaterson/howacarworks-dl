from os import environ
import json
import re

from selenium import webdriver

from selenium.webdriver.common.keys import Keys

config_regex = re.compile("var config = (.*);")

def handle_script(script):
    script_text = script.get_attribute("innerHTML")
    mobj = config_regex.search(script_text)
    unparsed_json = mobj.groups()[0]
    parsed_json = json.loads(unparsed_json)
    files = parsed_json["request"]["files"]["progressive"]
    print(json.dumps(files, indent=4))
    breakpoint()


def handle_episode(driver, episode):
    episode.click()
    player_frame = driver.find_element_by_css_selector("#vimeo_player > iframe")
    driver.switch_to.frame(player_frame)
    script = driver.find_element_by_css_selector(".vp-center > script")

    handle_script(script)

    driver.switch_to.default_content()


def handle_section(driver, section):
    for episode in section.find_elements_by_css_selector(".Episode ._content"):
        handle_episode(driver, episode)


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

    driver.implicitly_wait(3)
    sections = driver.find_elements_by_css_selector(".Section")
    for section in sections:
        handle_section(driver, section)

    driver.quit()

if __name__ == "__main__":
    main()
