import os
import requests
import json
from threading import Thread
from queue import Queue

# Define the URL to scrape
url = "https://unsplash.com/"

# Create a directory to store images
if not os.path.exists("images"):
    os.makedirs("images")

# Create a Queue for image URLs
image_queue = Queue()

# Function to download image from URL
def download_image(url, directory):
    image_name = url.split("/")[-1]
    image_path = os.path.join(directory, image_name)
    
    r = requests.get(url)
    if r.status_code == 200:
        with open(image_path, 'wb') as f:
            f.write(r.content)
        return image_path
    
# Function to process image metadata with PhotoTag.ai
def process_image_metadata(image_name):
    # Add code to communicate with PhotoTag.ai and get enhanced metadata
    # For now, let's just create a dummy metadata
    metadata = {
        "title": "Dummy Title",
        "description": "Dummy Description",
        "tags": ["tag1", "tag2"]
    }
    return metadata

# Function to save metadata as JSON file
def save_metadata(metadata, directory):
    metadata_path = os.path.join(directory, "metadata.json")
    with open(metadata_path, 'w') as f:
        json.dump(metadata, f)

# Worker function for each thread
def worker():
    while not image_queue.empty():
        image_url, directory = image_queue.get()
        image_path = download_image(image_url, directory)
        if image_path:
            metadata = process_image_metadata(image_path)
            save_metadata(metadata, directory)
        image_queue.task_done()

# Main function for downloading and processing images
def main():
    # Add code to scrape image URLs from Unsplash
    # For now, let's use some sample image URLs
    image_urls = ["https://unsplash.com/photos/example1.jpg", "https://unsplash.com/photos/example2.jpg"]
    
    for image_url in image_urls:
        image_id = image_url.split("/")[-1].split(".")[0]
        photographer_name = "john_doe"  # You can extract photographer name from image URL
        directory = os.path.join("images", f"{image_id}_{photographer_name}")
        if not os.path.exists(directory):
            os.makedirs(directory)
        image_queue.put((image_url, directory))
    
    # Create and start threads
    for i in range(5):  # Number of threads
        t = Thread(target=worker)
        t.daemon = True
        t.start()
    
    # Wait for all threads to complete
    image_queue.join()
    print("Download and metadata processing complete.")

if __name__ == "__main__":
    main()
