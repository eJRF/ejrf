import glob
import os

from lettuce import *
from splinter import Browser
from django.core.management import call_command

from django.template.defaultfilters import slugify


@before.each_scenario
def flush_database(step):
    call_command('flush', interactive=False)

@before.all
def clear_screenshots():
    screenshots = glob.glob('./screenshots/*.png')
    for screenshot in screenshots:
        os.remove(screenshot)
    open_browser()


def open_browser():
    world.browser = Browser("phantomjs")
    world.browser.driver.set_window_size(1024, 720)


@after.each_scenario
def take_screenshot(scenario):
    if scenario.failed:
        world.browser.driver.save_screenshot('screenshots/%s.png' % slugify(scenario.name))

@after.each_scenario
def clear_cookies(scenario):
    world.browser.cookies.delete()

@after.all
def close_browser(total):
    world.browser.quit()
