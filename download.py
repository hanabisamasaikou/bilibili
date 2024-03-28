import os
import time
import requests

headers = {
    "Referer": "https://www.bilibili.com/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
}


def download_video(video_dictionary: dict | None = None) -> None:
    t1 = time.time()
    print("Downloading...")
    title = video_dictionary["title"]
    audio = requests.get(url=video_dictionary["audio"], headers=headers).content
    video = requests.get(url=video_dictionary["video"], headers=headers).content
    with open("audio.m4s", "wb") as f:
        f.write(audio)
    with open("video.m4s", "wb") as f:
        f.write(video)
    os.system(f".\\ffmpeg.exe -i audio.m4s -i video.m4s -loglevel quiet -c:v copy -strict experimental {title}.mp4")
    os.remove(f"audio.m4s")
    os.remove(f"video.m4s")
    t2 = time.time()
    print(f"Downloaded. Elapsed time: {(t2 - t1):.2f} sec.")


def download_bangumi(bangumi_dictionary: dict | None = None) -> None:
    t1 = time.time()
    title = bangumi_dictionary["title"]
    os.makedirs(title, exist_ok=True)
    for name, url in bangumi_dictionary.items():
        if name != "title":
            t3 = time.time()
            print(f"Downloading {name}")
            with open(f"{title}/{name}.mp4", "wb") as f:
                f.write(requests.get(url=url, headers=headers).content)
            t4 = time.time()
            print(f"{name} finished in {((t4 - t3) / 60):.2f} min.")
    t2 = time.time()
    print(f"All done. Elapsed time: {((t2 - t1) / 60):.2f} min.")


def download_ep(url: str | None = None, name: int | None = None) -> None:
    t1 = time.time()
    print("Downloading...")
    with open(f"{name}.mp4", "wb") as f:
        f.write(requests.get(url=url, headers=headers).content)
    t2 = time.time()
    print(f"Downloaded. Elapsed time: {((t2 - t1) / 60):.2f} min.")
