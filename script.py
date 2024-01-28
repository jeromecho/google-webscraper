'''
In this example we iterating over 4 search queries,
doing pagination on each query until results is present,
and extracting original size image + optionally saving locally
'''

import urllib.request
from serpapi import GoogleSearch
from dotenv import load_dotenv
import os

load_dotenv() # brings all environment variables from .env file to os.environ

# to avoid getting images of downy mildew
def contains_downy(url):
    return "downy" in url.lower()

def contains_word(url, word):
    return word.lower() in url.lower()

def serpapi_get_google_images():
    image_results = []
    
    for query in ["grape leaf powdery mildew"]:
        # search query parameters
        params = {
            "engine": "google",               # search engine. Google, Bing, Yahoo, Naver, Baidu...
            "q": query,                       # search query
            "tbm": "isch",                    # image results
            "num": "100",                     # number of images per page
            "ijn": 0,                         # page number: 0 -> first page, 1 -> second...
            "api_key": os.environ['API_KEY'],                 # https://serpapi.com/manage-api-key
            # other query parameters: hl (lang), gl (country), etc  
        }
    
        search = GoogleSearch(params)         # where data extraction happens
    
        images_is_present = True
        while images_is_present:
            results = search.get_dict()       # JSON -> Python dictionary
    
            # checks for "Google hasn't returned any results for this query."
            if "error" not in results:
                for image in results["images_results"]:
                    if "original" in image and image["title"] not in image_results and not contains_word(image["title"], 'recipe') and not contains_word(image["title"], 'stuff') and not contains_word(image["title"], 'eat') and not contains_word(image["title"], 'chart') and not contains_word(image["title"], 'install') and not contains_word(image["title"], "downy") and not contains_word(image["title"], "fruit"):
                        image_results.append(image["original"])
                
                # update to the next page
                params["ijn"] += 1
            else:
                print(results["error"])
                images_is_present = False
    
    # -----------------------
    # Downloading images
    print(len(image_results))

    for index, image in enumerate(image_results, start=1):
        print(f"Downloading {index} image...")

        opener=urllib.request.build_opener()
        opener.addheaders=[("User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.79 Safari/537.36")]
        urllib.request.install_opener(opener)

        try:
            urllib.request.urlretrieve(image, f"./images/grape_leaf_pm{index}.jpg")
        except: 
            print(f"Failed to download {index} image")


    print(json.dumps(image_results, indent=2))
    print(len(image_results))

serpapi_get_google_images()
