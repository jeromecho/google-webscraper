import urllib.request
from serpapi import GoogleSearch
from dotenv import load_dotenv
from tqdm import tqdm
import os
from filters.Filter import Filter

load_dotenv() # brings all environment variables from .env file to os.environ

REQUEST_HEADERS: tuple = ("User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.79 Safari/537.36")

def contains_word(url, word):
    return word.lower() in url.lower()

class Job:
  def __init__(self, query_string: str, filters: list[Filter] = [], save_dir: str = 'images') :
    self.query_string = query_string
    self.filters = filters
    self.save_dir = save_dir

  def run(self):
    image_results = []
    params = {
      "engine": "google",               # search engine. Google, Bing, Yahoo, Naver, Baidu...
      "q": self.query_string,                       # search query
      "tbm": "isch",                    # image results
      "num": "100",                     # number of images per page
      "ijn": 0,                         # page number: 0 -> first page, 1 -> second...
      "api_key": os.environ['API_KEY'],                 # https://serpapi.com/manage-api-key
      # other query parameters: hl (lang), gl (country), etc  
    }

    search = GoogleSearch(params)         # where data extraction happens
    images_is_present = True

    print(f"----- APPENDING IMAGES -----")
    while images_is_present:
      results = search.get_dict()       # JSON -> Python dictionary

      # checks for "Google hasn't returned any results for this query."
      if "error" not in results:
        for image in tqdm(results["images_results"]):
          # Avoids duplicates
          if "original" in image and image["original"] in image_results:
            continue
          for filter in self.filters:
            if contains_word(image[filter.image_attribute], filter.filter_string):
                continue
          image_results.append(image["original"])
                # update to the next page
        params["ijn"] += 1
      else:
        print(results["error"])
        images_is_present = False

    # Downloading images
    print(f"------ DOWNLOADING {len(image_results)} IMAGES -----")

    # Make the save directory if it doesn't already exist
    try:
        os.mkdir(self.save_dir)
    except OSError:
        print(f"Directory '{self.save_dir}' already exists")
    except:
        print(f"Unable to create directory '{self.save_dir}'")

    for index, image in tqdm(enumerate(image_results, start=1)):
        opener=urllib.request.build_opener()
        opener.addheaders=[REQUEST_HEADERS]
        urllib.request.install_opener(opener)

        try:
          urllib.request.urlretrieve(image, f"./{self.save_dir}/image-{index}.jpg")
        except urllib.error.HTTPError:
          print(f"HTTPError: Forbidden from downloading this resource")
        except:
          print(f"Something unexpected happened trying to download {image['title']}")
