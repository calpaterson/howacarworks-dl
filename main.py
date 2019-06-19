from os import environ
from sys import stdout
import json
import re
import time

from selenium import webdriver

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement

config_regex = re.compile("var config = (.*);")

def handle_script(script: WebElement) -> str:
    """Returns download url of highest quality version"""
    script_text = script.get_attribute("innerHTML")
    mobj = config_regex.search(script_text)
    unparsed_json = mobj.groups()[0]
    parsed_json = json.loads(unparsed_json)
    files = parsed_json["request"]["files"]["progressive"]
    top_quality = sorted(files, key=lambda f: f["height"], reverse=True)[1]["url"]
    return top_quality


def handle_episode(driver, section_name, episode):
    episode_name = episode.text.split("\n")[0]
    episode.click()
    time.sleep(3)

    player_frame = driver.find_element_by_css_selector("#vimeo_player > iframe")

    driver.switch_to.frame(player_frame)
    time.sleep(3)
    script = driver.find_element_by_css_selector(".vp-center > script")

    url = handle_script(script)
    stdout.write("%s\n  dir=%s\n  out=%s.mp4\n" % (url, section_name, episode_name))

    driver.switch_to.default_content()


def handle_section(driver, section):
    section_name = section.find_element_by_css_selector("h2").text
    for episode in section.find_elements_by_css_selector(".Episode ._content"):
        handle_episode(driver, section_name, episode)


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
