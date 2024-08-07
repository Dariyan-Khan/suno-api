import time
import requests
from playwright.sync_api import sync_playwright, Page, expect
import re
import os
from copy import deepcopy
from tqdm import tqdm

# replace your vercel domain
base_url = 'http://localhost:3000'


def custom_generate_audio(payload):
    url = f"{base_url}/api/custom_generate"
    response = requests.post(url, json=payload, headers={'Content-Type': 'application/json'})
    return response.json()


def extend_audio(payload):
    url = f"{base_url}/api/extend_audio"
    response = requests.post(url, json=payload, headers={'Content-Type': 'application/json'})
    return response.json()

def generate_audio_by_prompt(payload):
    url = f"{base_url}/api/generate"
    response = requests.post(url, json=payload, headers={'Content-Type': 'application/json'})
    return response.json()

def custom_generate_audio_by_prompt(payload):
    url = f"{base_url}/api/custom_generate"
    response = requests.post(url, json=payload, headers={'Content-Type': 'application/json'})
    return response.json()


def get_audio_information(audio_ids):
    url = f"{base_url}/api/get?ids={audio_ids}"
    response = requests.get(url)
    return response.json()


def get_quota_information():
    url = f"{base_url}/api/get_limit"
    response = requests.get(url)
    return response.json()

def get_clip(clip_id):
    url = f"{base_url}/api/clip?id={clip_id}"
    response = requests.get(url)
    return response.json()

def generate_whole_song(clip_id):
    payloyd = {"clip_id": clip_id}
    url = f"{base_url}/api/concat"
    response = requests.post(url, json=payload)
    return response.json()


# def get_song(self, id: str):
#         """
#         Retrieve a single song by its ID.

#         Parameters:
#         - id (str): The ID of the song to retrieve.

#         Returns:
#         Clip: A Clip object containing details about the song, such as the audio URL, song status, and other metadata.
#         """
#         self._keep_alive()  # Ensure session is active
#         logger.info("Getting Song Info...")
#         response = self.client.get(
#             f"{Suno.BASE_URL}/api/feed/?ids={id}")  # Call API
#         logger.debug(response.text)
#         self._cehck_error(response)
#         return create_clip_from_data(response.json()[0])



def download(song, path= "../songs_generated", title=None) -> str:
        """
        Downloads a Suno song to a specified location.

        Args:
            song (str | Clip): Either the ID of the song or a Clip object representing the song.
            path (str): The directory where the song should be saved. Defaults to "./downloads".

        Returns:
            str: The full filepath of the downloaded song.

        Raises:
            TypeError: If the 'song' argument is not of type str or Clip.
            Exception: If the download fails (e.g., bad URL, HTTP errors).
        """
        
        if isinstance(song, str):
            id = song
            # url = self.get_song(id).audio_url
            #url = "https://audiopipe.suno.ai/?" + song
            url = f"https://cdn1.suno.ai/{id}.mp3"
        else:
            raise TypeError
        
        print(f"Audio URL : {url}")
        
        #logger.info(f"Audio URL : {url}")
        response = requests.get(url)
        if not response.ok:
            raise Exception(
                f"failed to download from audio url: {response.status_code}"
            )
        
        # assert False

        if title is None:
            title = deepcopy(id)
            file = os.path.join(path, f"{title}.mp3")
        with open(file, "wb") as f:
            f.write(response.content)
        print(f"audio file: {file}")
    
    
# def download(ids, folder, base_title):
#     if not os.path.exists(f"../songs_generated/{folder}"):
#         os.makedirs(f"../songs_generated/{folder}")

#     for i, id in enumerate(ids):
#         download_inner(id, f"../songs_generated/{folder}", title=f"base_title_{i}")
    

def add_song_to_csv_file(id, title, prompt, date):
    song_url = f"https://cdn1.suno.ai/{id}.mp3"
    with open(f"../songs_generated/songs.csv", "a") as f:
        f.write(f"{id}, {title},{prompt}, {date}, {song_url}\n")







if __name__ == '__main__':
    # data = generate_audio_by_prompt({
    #     "prompt": "An r&b song about Cardiff",
    #     "make_instrumental": False,
    #     "wait_audio": False
    # })

    # ids = f"{data[0]['id']},{data[1]['id']}"
    # print(f"ids: {ids}")

    # for _ in range(60):
    #     data = get_audio_information(ids)
    #     if data[0]["status"] == 'streaming':
    #         print(f"{data[0]['id']} ==> {data[0]['audio_url']}")
    #         print(f"{data[1]['id']} ==> {data[1]['audio_url']}")
    #         break
    #     # sleep 5s
    #     time.sleep(5)




    # test_id = "81ec34ab-da9f-478e-8266-526035b0cb51"

    # test_info = get_audio_information(test_id)

    # print(test_info)

    #download(test_id)

    # download_song_inner()




    country = "Pakistan"
    folder = country.lower()

    # assert False


    titles = [
    "Karachi Nights",
    "Lahore Dreams",
    "Sindhi Serenade",
    "Islamabad Impressions",
    "Rivers of Punjab"
    ]


    id_list = []

    for base_title in tqdm(titles):

        data = custom_generate_audio_by_prompt({
            "prompt": "[Instrumental]",
            "tags": "lofi pakistani dhol sitar flutes",
            "title": base_title,
            "make_instrumental": False,
            "wait_audio": True
        })

        #ids = f"{data[0]['id']},{data[1]['id']}"
    
        id_list.append(data[0]['id'])
        id_list.append(data[1]['id'])

        # sleep 2 mins
        #time.sleep(60)

        if not os.path.exists(f"../songs_generated/{folder}"):
            os.makedirs(f"../songs_generated/{folder}")



        add_song_to_csv_file(data[0]['id'], f"{data[0]['title']}_0", data[0]['prompt'], data[0]['created_at'])
        add_song_to_csv_file(data[1]['id'], f"{data[1]['title']}_1", data[1]['prompt'], data[1]['created_at'])


        # download(data[0]['id'], f"../songs_generated/{folder}")
        # download(data[1]['id'], f"../songs_generated/{folder}")

        
    print(id_list)
        
    
    
    #download("6de8500d-044a-4d91-b1ed-20d8292321ec", "../songs_generated/pakistan",)




