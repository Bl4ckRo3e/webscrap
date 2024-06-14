# webscrap
This code script that scrapes images from the Unsplash website, downloads and saves them locally, and then uses the PhotoTag API to generate keywords/tags for each image.

The UnsplashImageScraper class is responsible for scraping image links from the Unsplash website, downloading and saving the images locally, and saving metadata (image ID, photographer, category) for each image.

The PhotoTagAPI class is responsible for interacting with the PhotoTag API to generate tags for each image using the image file path.

The main function creates an instance of the UnsplashImageScraper class, scrapes image links from Unsplash, and then creates multiple threads to download and save the images concurrently. Once the images are downloaded, it uses the PhotoTagAPI class to generate tags for each image and prints the tags.

To run the code, you would need to replace "YOUR_API_KEY_HERE" in the PhotoTagAPI class with your actual API key for the PhotoTag API. The code will then scrape images from Unsplash, download and save them locally, generate tags using the PhotoTag API, and print the tags for each image.

# writers 
1. Esmail Taghizadeh
2. Ali Akbar Fanilari
