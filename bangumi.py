import re
import requests


class Query:
    def __init__(self, session_id: int = -1) -> None:
        self.session_id = session_id
        self.url = f"https://www.bilibili.com/bangumi/play/ss{session_id}"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
        }
        self.response = requests.get(url=self.url, headers=self.headers)

    def get_bangumi_title(self) -> str:
        return re.findall(r"<title>(.*?)<\/title>", self.response.text)[0].split("-")[0]

    def get_ep_id_list(self) -> list:
        return re.findall(r"[\'|\"]ep_id[\'|\"]:\s*(\d*)", self.response.text)

    def get_player_ep_title_list(self) -> list:
        return re.findall(r"[\'|\"]playerEpTitle[\'|\"]:\s*[\'|\"](.*?)[\'|\"]", self.response.text)


class Ep:
    def __init__(self, ep_id: int = -1) -> None:
        self.ep_id = ep_id
        self.url = f"https://api.bilibili.com/pgc/player/web/v2/playurl?ep_id={ep_id}"
        self.headers = {
            "Cookie": "buvid3=FA80BA3B-DB9E-7158-A537-87E03A7F557D97910infoc; b_nut=1711604597; i-wanna-go-back=-1; b_ut=7; _uuid=510463218-B4101-9F15-2444-DE413E51B72E98795infoc; enable_web_push=DISABLE; home_feed_column=5; buvid4=20A644FD-2565-64AD-BADA-DC5F8DB49F2B98436-024032805-nnNopXvJJxE688yoGqHZBw%3D%3D; buvid_fp=c84e5c3aeae2553566b1438e75929b29; SESSDATA=87bf58e2%2C1727156608%2Cb0c6f%2A31CjAxh6X4QHHYWcEIYtT54C_PNpq3OOR1qnL--jccDfgOkZ8tiXp7Tij31B4hr7_RHKISVlVpejN0bml5bENBVmZST002Rm14WjJlT1UxbnVmRmRTZmxUVnZvOTJVc2pNcEVVeVJxbk5jUjJJcEgtQXhfbVc1SHQ2LWMtMEdUaWY1TnF5dWNfd0p3IIEC; bili_jct=bbb2be99e82fd07737ba2d107ee49621; DedeUserID=1152955917; DedeUserID__ckMd5=b5490f35b0858424; sid=4v5j6cfl; hit-dyn-v2=1; FEED_LIVE_VERSION=V_WATCHLATER_PIP_WINDOW; header_theme_version=CLOSE; browser_resolution=1920-476; CURRENT_BLACKGAP=0; CURRENT_FNVAL=4048; rpdid=|(k|k)J~uJmm0J'u~uuY|luYR; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MTE4NjQzNjUsImlhdCI6MTcxMTYwNTEwNSwicGx0IjotMX0.atOEdy_ZMPZ2G4gJ0T6XbtqLUbGh32rj9tEPpcNOV2M; bili_ticket_expires=1711864305; PVID=6;",
            "Referer": f"https://www.bilibili.com/bangumi/play/ep{ep_id}",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
        }
        self.response = requests.get(url=self.url, headers=self.headers)

    def get_ep_url(self) -> str:
        return self.response.json()["result"]["video_info"]["durl"][0]["url"]


def bangumi(session_id: int) -> dict:
    bangumi_dictionary = {}
    query = Query(session_id)
    bangumi_dictionary.update({"title": query.get_bangumi_title()})
    ep_id_list = query.get_ep_id_list()
    player_ep_title_list = query.get_player_ep_title_list()
    for ep in range(len(ep_id_list)):
        ep_url = Ep(ep_id_list[ep]).get_ep_url()
        ep_title = player_ep_title_list[ep]
        bangumi_dictionary.update({ep_title: ep_url})
    return bangumi_dictionary
