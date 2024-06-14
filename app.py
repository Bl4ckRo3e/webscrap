# import requests
# from bs4 import BeautifulSoup
# import os
# import json
# import threading

# class UnsplashImageScraper:
#     def __init__(self):
#         self.PROXY = {
#             'http': 'http://127.0.0.1:4392',
#             'https': 'https:/127.0.0.1:443'
#         }
#         self.UNSPLASH_URL = "https://unsplash.com"
#         self.SAVE_DIR = "images"

#         if not os.path.exists(self.SAVE_DIR):
#             os.makedirs(self.SAVE_DIR)

#     def get_image_links(self):
#         response = requests.get(self.UNSPLASH_URL, proxies=self.PROXY)
#         soup = BeautifulSoup(response.text, 'html.parser')
#         links = []
#         for img in soup.find_all('img', {'srcset': True}):
#             links.append(img['src'])
#         return links

#     def download_image(self, url, save_path):
#         response = requests.get(url)
#         with open(save_path, 'wb') as file:
#             file.write(response.content)

#     def save_metadata(self, image_id, photographer, category, save_path):
#         metadata = {
#             'image_id': image_id,
#             'photographer': photographer,
#             'category': category
#         }
#         with open(save_path, 'w') as file:
#             json.dump(metadata, file, indent=4)

#     def download_and_save_image(self, link, idx):
#         image_id = f'image_{idx}'
#         save_path = os.path.join(self.SAVE_DIR, image_id + '.jpg')
#         metadata_path = os.path.join(self.SAVE_DIR, image_id + '.json')

#         self.download_image(link, save_path)
#         self.save_metadata(image_id, "Unknown", "Uncategorized", metadata_path)

# unsplash_image_scraper = UnsplashImageScraper()

# image_links = unsplash_image_scraper.get_image_links()

# threads = []
# for idx, link in enumerate(image_links):
#     thread = threading.Thread(target=unsplash_image_scraper.download_and_save_image, args=(link, idx))
#     threads.append(thread)
#     thread.start()

# for thread in threads:
#     thread.join()


import requests
from bs4 import BeautifulSoup
import os
import json
import threading

class UnsplashImageScraper:
    def __init__(self):
        self.PROXY = {
            'http': 'http://127.0.0.1:4392',
            'https': 'https:/127.0.0.1:443'
        }
        self.UNSPLASH_URL = "https://unsplash.com"
        self.SAVE_DIR = "images"

        if not os.path.exists(self.SAVE_DIR):
            os.makedirs(self.SAVE_DIR)

    def get_image_links(self):
        response = requests.get(self.UNSPLASH_URL, proxies=self.PROXY)
        soup = BeautifulSoup(response.text, 'html.parser')
        links = []
        for img in soup.find_all('img', {'srcset': True}):
            links.append(img['src'])
        return links

    def download_image(self, url, save_path):
        response = requests.get(url)
        with open(save_path, 'wb') as file:
            file.write(response.content)

    def save_metadata(self, image_id, photographer, category, save_path):
        metadata = {
            'image_id': image_id,
            'photographer': photographer,
            'category': category
        }
        with open(save_path, 'w') as file:
            json.dump(metadata, file, indent=4)

    def download_and_save_image(self, link, idx):
        image_id = f'image_{idx}'
        save_path = os.path.join(self.SAVE_DIR, image_id + '.jpg')
        metadata_path = os.path.join(self.SAVE_DIR, image_id + '.json')

        self.download_image(link, save_path)
        self.save_metadata(image_id, "Unknown", "Uncategorized", metadata_path)

class PhotoTagAPI:
    def __init__(self):
        self.URL = "https://server.phototag.ai/api/keywords"
        self.HEADERS = {
            "Authorization": f'Bearer YOUR_API_KEY_HERE'
        }

    def get_tags(self, image_path):
        with open(image_path, 'rb') as image:
            payload = {
                "language": "en",
                "MacKeys": 4,
                "Keys": "",
                "cCON": ""
            }
            files = {'file': image}

            response = requests.post(self.URL, headers=self.HEADERS, data=payload, files=files)
            if response.status_code == 200:
                data = response.json()
                keywords = data.get('keywords')
                return keywords
            else:
                return []

def main():
    unsplash_image_scraper = UnsplashImageScraper()
    image_links = unsplash_image_scraper.get_image_links()

    threads = []
    for idx, link in enumerate(image_links):
        thread = threading.Thread(target=unsplash_image_scraper.download_and_save_image, args=(link, idx))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    photo_tag_api = PhotoTagAPI()

    for filename in os.listdir(unsplash_image_scraper.SAVE_DIR):
        if filename.endswith('.jpg'):
            image_path = os.path.join(unsplash_image_scraper.SAVE_DIR, filename)
            tags = photo_tag_api.get_tags(image_path)
            print(f'Tags for {filename}: {tags}')

if __name__ == '__main__':
    main()
