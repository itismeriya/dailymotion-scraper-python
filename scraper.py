from selenium import webdriver
from selenium.webdriver.common.by import By
import collections
import time

# Set up the web driver
driver = webdriver.Chrome()  # Ensure you have ChromeDriver installed and in PATH

# Open the URL
driver.get('https://www.dailymotion.com/tseries2')

# Function to scroll the page
def scroll_page(driver, times):
    for _ in range(times):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # Wait for new videos to load

video_urls = set()  # Use a set to avoid duplicates
scroll_times = 50   # Adjust based on how many times you need to scroll to load 500 videos

# Scroll and collect video URLs
for _ in range(scroll_times):
    scroll_page(driver, 1)
    videos = driver.find_elements(By.CSS_SELECTOR, "a[href*='/video/']")
    for video in videos:
        url = video.get_attribute('href')
        if url and '/video/' in url:
            video_urls.add(url)
    if len(video_urls) >= 500:
        break

# Limit to the first 500 videos
video_urls = list(video_urls)[:500]

# Close the driver
driver.quit()

# Extract video IDs from URLs
video_ids = [url.split('/video/')[1] for url in video_urls]

# Concatenate all video IDs
all_ids = ''.join(video_ids)

# Count frequency of each character
counter = collections.Counter(all_ids.lower())  # Case-insensitive count

# Find the most common character
most_common_char = min([char for char, count in counter.items() if count == counter.most_common(1)[0][1]])

# Output the result
print(f"{most_common_char}:{counter[most_common_char]}")
