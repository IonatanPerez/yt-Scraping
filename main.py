from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time

def get_source_code(url):
    # Initialize the WebDriver
    driver = webdriver.Chrome()  # Make sure you have the ChromeDriver installed and in your PATH
    driver.get(url)
    

    time.sleep(2)  # Allow 2 seconds for the web page to open
    scroll_pause_time = 1 # You can set your own pause time. My laptop is a bit slow so I use 1 sec
    screen_height = driver.execute_script("return window.screen.height;")   # get the screen height of the web
    urls_found = 0

    while True:
        source_code = driver.page_source
        urls = extract_urls(source_code)
        if len(urls) == urls_found:
            print (f"Found {len(urls)} urls in total, it looks like we reached the end of the page")
            break
        urls_found = len(urls)
        print (f"Found {len(urls)} urls until now, we will scroll down to find more")
        remove_elements_by_class(driver, "style-scope ytd-rich-item-renderer")
        driver.execute_script(f"window.scrollBy(0, {10*screen_height});")  # We set on 10 screen to ensure that we move until the hidden elements because the page load more than one screen of elements.
        time.sleep(scroll_pause_time)
    driver.quit()    
    return source_code
    

def extract_urls(source_code):
    # Parse the source code with BeautifulSoup
    soup = BeautifulSoup(source_code, "html.parser")
    # Find the main content with specific id and class
    video_grid_elements = soup.find_all(class_="style-scope ytd-rich-item-renderer", id="content")
    print(f"Found {len(video_grid_elements)} video grid elements.")
    # Extract the URLs
    urls = []
    for video_grid_element in video_grid_elements:
        link_element = video_grid_element.find_all("a", "yt-simple-endpoint inline-block style-scope ytd-thumbnail")
        assert len(link_element) == 1, f"Expected 1 URL, but found {len(link_element)}."
        link_element = link_element[0]
        urls.append(link_element["href"])
    return urls


def remove_elements_by_class(driver, class_name):
    script = f"""
    var elements = document.getElementsByClassName("{class_name}");
    while(elements.length > 0){{
        elements[0].parentNode.removeChild(elements[0]);
    }}
    """
    driver.execute_script(script)

# Example usage
url = "https://www.youtube.com/c/ArchivoHist%C3%B3ricoRTA/videos"
source_code = get_source_code(url)
print(source_code)
