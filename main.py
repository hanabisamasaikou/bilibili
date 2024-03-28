from bangumi import *
from download import *
from video import *

if __name__ == '__main__':
    while True:
        url = input(">> ")
        if url.startswith("https://www.bilibili.com/bangumi/play/ss"):
            session_id = re.findall(r"\d+", url)[0]
            bangumi_dictionary = bangumi(session_id)
            download_bangumi(bangumi_dictionary)
        elif url.startswith("https://www.bilibili.com/bangumi/play/ep"):
            ep_id = re.findall(r"\d+", url)[0]
            ep = Ep(ep_id)
            download_ep(ep.get_ep_url(), ep_id)
        elif url.startswith("https://www.bilibili.com/video/BV"):
            bvid = re.findall(r"BV(.*?)\/", url)[0]
            video_dictionary = video(bvid)
            download_video(video_dictionary)
        else:
            print("Wrong url!")
            continue
