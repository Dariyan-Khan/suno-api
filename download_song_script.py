import time
import requests
from playwright.sync_api import sync_playwright, Page, expect
import re
import os
from copy import deepcopy
from tqdm import tqdm


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


if __name__ == "__main__":

    id_list = ["e5b93785-4a00-4b7d-aae5-fadd073cb632",
               "2e73951a-618c-4d64-93f0-9c8e110e4c59",
               "e6feea03-f54d-4c9b-bb19-efbdfcffb2d0",
               "cfd56826-7d83-418f-bf0f-2bbe7c5c774c",
               "05b11074-f817-4146-97c5-430286b4d2e5",
               "53e9f84f-ea2a-407a-b1b4-9d86e407259a",
               "6b26270f-5de8-47f7-b8e0-755daadcd110",
               "8e33f3f4-2568-484e-add5-2cb63949572f",
               "7ebf858d-d1d5-410a-a590-8ff047803898",
               "068391d1-f088-43af-a6e7-e632b6f90f19"
               ]
    #assert False

    for id in tqdm(id_list):
        download(id)
    