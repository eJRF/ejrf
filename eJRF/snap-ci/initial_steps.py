import glob
import os
import logging

from lettuce import *
from splinter import Browser
from django.core.management import call_command

from django.template.defaultfilters import slugify


@before.each_scenario
def flush_database(step):
    call_command('flush', interactive=False)


@before.all
def clear_screen_shots():
    screen_shots = glob.glob('./screenshots/*.png')
    for screen_shot in screen_shots:
        os.remove(screen_shot)
    open_browser()


def open_browser():
    logging.warning("about to open browser")

    username = os.getenv('SAUCE_USERNAME')
    access_key = os.getenv('SAUCE_ACCESS_KEY')
    git_commit = os.getenv('SNAP_COMMIT_SHORT')
    snap_build = os.getenv('SNAP_PIPELINE_COUNTER')
    browser = os.getenv('BROWSER', 'internetexplorer')
    browser_version = os.getenv('VERSION', '9')
    platform = os.getenv('PLATFORM', 'Windows 7')
    sauce_url = "http://%s:%s@ondemand.saucelabs.com:80/wd/hub" % (username, access_key)

    browser_options = {
        'driver_name': 'remote',
        'browser': browser,
        'version': browser_version,
        'platform': platform,
        'url': sauce_url,
        'name': "%s on %s %s, %s - Build: %s" % (git_commit, browser, browser_version, platform, snap_build),
        'build': snap_build
    }

    world.browser = Browser(**browser_options)
    logging.warning("browser set")
    world.browser.driver.set_window_size(1024, 720)
    logging.warning("window size set")

@after.each_scenario
def take_screen_shot(scenario):
    if scenario.failed:
        world.browser.driver.save_screenshot('screenshots/%s.png' % slugify(scenario.name))


@before.outline
def cleanup(args, *kwargs):
    call_command('flush', interactive=False)


@after.outline
def take_screen_shot(args, *kwargs):
    key = kwargs[1].keys()[0]
    if kwargs[-1] != []:
        world.browser.driver.save_screenshot('screenshots/%s.png' % slugify(kwargs[1][key]))


@after.each_scenario
def clear_cookies(scenario):
    world.browser.driver.delete_all_cookies()


@after.all
def close_browser(total):
    world.browser.quit()


@after.all
def tear_down(step):
    os.system('rm *.pdf')
    os.system("rm -rf media/user_uploads/*")