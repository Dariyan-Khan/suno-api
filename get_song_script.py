import time
import requests
from playwright.sync_api import sync_playwright, Page, expect
import re

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



def download(self, song: str | Clip, path: str = "./downloads",) -> str:
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
        if isinstance(song, Clip):
            id = song.id
            url = song.audio_url
        elif isinstance(song, str):
            id = song
            url = self.get_song(id).audio_url
        else:
            raise TypeError
        logger.info(f"Audio URL : {url}")
        response = requests.get(url)
        if not response.ok:
            raise Exception(
                f"failed to download from audio url: {response.status_code}"
            )
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Check for HTTP errors
        filename = self._get_dl_path(id, path)
        with open(filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:  # Filter out keep-alive chunks
                    f.write(chunk)
        logger.info(f"Download complete: {filename}")
        return filename


# def download_song():
#     with sync_playwright() as p:
#         browser = p.chromium.launch(headless=False)
#         page = browser.new_page(accept_downloads=True)
#         download_song_inner(page)
#         browser.close()


# # def download_song_inner(page: Page) -> None:
# def download_song_inner():
#     with sync_playwright() as p:
#         browser = p.chromium.launch(headless=False)
#         context = browser.new_context(accept_downloads=True)
#         page = context.new_page()
#         page.goto("https://suno.com/")
#         page.get_by_text("Sign Up / Log In").click()
#         page.locator(".cl-socialButtons > button:nth-child(2)").click()
#         page.get_by_label("Email or Phone Number*").click()
#         page.get_by_label("Email or Phone Number*").fill("dariyankhan01@gmail.com")
#         page.get_by_label("Password*").click()
#         page.get_by_label("Password*").fill("choco46D")
#         page.get_by_role("button", name="Log In").click()

#         page2 = context.new_page()
#         page2.goto("https://suno.com/")
#         page2.goto("https://suno.com/song/b6b23513-7e02-4192-8349-081c77ff62e8")
#         page2.locator("div").filter(has_text=re.compile(r"^10Share SongReuse Promptv3\.522 June 2024 at 21:03$")).get_by_label("More Actions").click()
#         with page2.expect_download() as download_info:
#             page2.get_by_test_id("download-audio-menu-item").click()
#         download = download_info.value

#         download.save_as("/songs_generated" + download.suggested_filename)




if __name__ == '__main__':
    data = generate_audio_by_prompt({
        "prompt": "An r&b song about Cardiff",
        "make_instrumental": False,
        "wait_audio": False
    })

    ids = f"{data[0]['id']},{data[1]['id']}"
    print(f"ids: {ids}")

    for _ in range(60):
        data = get_audio_information(ids)
        if data[0]["status"] == 'streaming':
            print(f"{data[0]['id']} ==> {data[0]['audio_url']}")
            print(f"{data[1]['id']} ==> {data[1]['audio_url']}")
            break
        # sleep 5s
        time.sleep(5)

    # download_song_inner()

