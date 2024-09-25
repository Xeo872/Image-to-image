import requests
from bs4 import BeautifulSoup
import os
import time
import random

# Cookies formatted as a dictionary
cookies = {
    'user_id': '1330442',
    'pass_hash': '057efa0eef7e99bc1f8ec3c981f7cd5921321640',
    'PHPSESSID': 'OvWsF3UOn37phgsJ5mVNtQuNosEND8GViwzEC3lAHFijy85ku%2C7O7fVqCL5bLYKq2Nc-dkLdZZ8yzy--IR2oy7ih9Z%2CUKpjHvDF1LmnPARbQ-QkVaDBaRlCVCaxVINU-',
    'fringeBenefits': 'yup',
    'comment_threshold': '0',
    'post_threshold': '0',
    'show_sample': '1',
    'resize-notification': '1'
}

def download_image(url, img_filename):
    # Fetch the image content and save it
    img_data = requests.get(url).content
    with open(img_filename, 'wb') as handler:
        handler.write(img_data)
    print(f"Image downloaded and saved as {img_filename}")

def scrape_and_download_images(start_url):
    # Step 1: Create a session and pass the cookies
    session = requests.Session()
    session.cookies.update(cookies)

    # Step 2: Fetch the webpage while logged in
    response = session.get(start_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Step 3: Find all article tags with class 'thumbnail-preview'
    article_tags = soup.find_all('article', class_='thumbnail-preview')

    if not article_tags:
        print("No article tags with class 'thumbnail-preview' found")
        return

    print(f"Found {len(article_tags)} article(s).")

    # Step 4: Iterate over each article tag
    for idx, article_tag in enumerate(article_tags):
        print(f"\nProcessing article {idx+1}/{len(article_tags)}")

        # Find the 'a' tag inside the article and extract its href (URL)
        a_tag = article_tag.find('a')
        if a_tag is None or 'href' not in a_tag.attrs:
            print("No 'a' tag or URL found in this article")
            continue

        article_url = a_tag['href']
        if not article_url.startswith('http'):
            article_url = requests.compat.urljoin(start_url, article_url)
        
        print(f"Found article URL: {article_url}")

        # Step 5: Fetch the second webpage
        response_article = session.get(article_url)
        soup_article = BeautifulSoup(response_article.text, 'html.parser')

        # Step 6: Find the img tag with id="image"
        img_tag = soup_article.find('img', id='image')
        if img_tag is None or 'src' not in img_tag.attrs:
            print("No image tag with id 'image' found in this article")
            continue

        img_url = img_tag['src']
        if not img_url.startswith('http'):
            img_url = requests.compat.urljoin(article_url, img_url)

        print(f"Found image URL: {img_url}")

        # Step 7: Download the image
        img_filename = img_url.split('/')[-1]
        download_image(img_url, img_filename)

        # Step 8: Delay between requests to avoid rate-limiting or IP ban
        delay = random.uniform(5, 10)  # Random delay between 5 and 10 seconds
        print(f"Waiting for {delay:.2f} seconds before next request...")
        time.sleep(delay)

# Example usage
start_url = 'https://gelbooru.com/index.php?page=post&s=list&tags=boku_wa_tomodachi_ga_sukunai'  # Replace with the actual URL
scrape_and_download_images(start_url)
