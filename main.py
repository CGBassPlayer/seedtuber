#!/usr/bin/python3
import os

import requests
from schedule import repeat, every, run_pending
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.webdriver import WebDriver
from webdriver_manager.firefox import GeckoDriverManager

BROWSER_INSTANCES: list[tuple[str, WebDriver]] = []


def get_live_video_urls(instance_url: str, count: int) -> list[str]:
    """
    Get a list of URLs for the videos that are currently live.
    :param count: Limit the number of results in the list
    :param instance_url: base url of the PeerTube instance that will be called
    :return: list of URLs as strings
    """
    if count > 100 or count == 0:
        count = 100
    search_url: str = f"{instance_url}api/v1/search/videos?isLive=true&sort=-publishedAt&count={count}"
    videos_json: dict = requests.get(search_url).json()
    return [v["url"] for v in videos_json["data"]]


def start_browser_instance(url: str = None) -> WebDriver:
    """
    Create a headless Firefox instance and navigate to the URL provide. Then returns the Firefox instance
    :param url: URL to send browser to
    :return: The Browser object
    """
    browser_options: Options = Options()
    browser_options.add_argument("-headless")
    browser_options.set_preference("media.autoplay.default", False)
    browser: WebDriver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()),
                                           options=browser_options)
    if url is not None:
        browser.get(url)
    return browser


@repeat(every(int(os.getenv("ping_interval", default="300"))).seconds,
        url=os.getenv("peertube_url", default="https://jupiter.tube/"),
        browser_limit=int(os.getenv("browser_limit", default="0")))
def update(url: str, browser_limit: int) -> None:
    if browser_limit == 0:
        browser_limit = 100
    print("Checking for live videos")
    live_videos: list[str] = get_live_video_urls(url, browser_limit)

    print(f"Current live videos: {len(live_videos)}")
    for (url, browser) in BROWSER_INSTANCES:
        if url not in live_videos:
            print(f"{url} is no longer live. Closing browser session")
            browser.close()
            BROWSER_INSTANCES.remove((url, browser))

    for video in live_videos:
        if video not in (i[0] for i in BROWSER_INSTANCES) and len(BROWSER_INSTANCES) <= browser_limit:
            browser: WebDriver = start_browser_instance(video)
            BROWSER_INSTANCES.append((video, browser))


if __name__ == '__main__':
    # Do first run immediately
    update(
        url=os.getenv("peertube_url", default="https://jupiter.tube/"),
        browser_limit=int(os.getenv("browser_limit", default="0")))
    while True:
        run_pending()  # Run as normal
