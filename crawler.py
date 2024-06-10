import base64
import re
from datetime import datetime
from urllib.parse import urlparse

import arrow
import requests
from parsel import Selector

from model import SevenPrint, SevenPrintProduct


def fetch_page(url: str) -> str:
    return requests.get(url).text


def fetch_image(url: str) -> str:
    res = requests.get(url)
    return f"data:image/png;base64,{base64.b64encode(res.content).decode('utf-8')}"


def extract_products(host: str, html: str) -> list[SevenPrintProduct]:
    items = []
    page = Selector(text=html)
    for product in page.css("dd.item_products li.item"):
        image_url = f"{host}{product.css('img::attr(src)').get()}"
        image = fetch_image(image_url)
        reservation = {}
        name = ""
        for tr_index, tr in enumerate(product.css("tr"), start=1):
            if tr_index == 1:
                name = tr.css("td.name::text").get()
            else:
                size = "預設"
                if mid_size := tr.css("td.mid_size::text").get():
                    size = mid_size
                token = tr.css("td.right_no::text").get()
                reservation[token] = size

        items.append(SevenPrintProduct(name=name, image=image, reservation_id=reservation))

    return items


def extract_datetime(text: str) -> str | None:
    regex = r"～(?P<datetime>\d{4}年\d{1,2}月\d{1,2}日（.）\d{1,2}:\d{1,2})"
    match = re.search(regex, text)
    if match:
        return match.group("datetime")
    return None


def extract_info(url: str, host: str, html: str) -> SevenPrint:
    page = Selector(text=html)
    name = (
        "".join(page.css("p.title").css("*::text").extract()).replace("\xa0", " ").replace("\r", "").replace("\n", "")
    )
    sell_end = None
    pager_url = [url]
    for dl in page.css("div.summary > dl.table"):
        if dl.css("dt::text").get() == "販売期間":
            sell_end = extract_datetime(dl.css("dd > span.nw:last-child::text").get())
    if pager := page.css("div.pager:first-child"):
        pager_url += [f"{host}{next_page_url}" for next_page_url in set(pager.css("a::attr(href)").getall())]
    print(f"> {url=}")
    print(f"> {sell_end=}")
    print(f"> {pager_url=}")
    return SevenPrint(name=name, url=url, sell_end=sell_end, pager_url=pager_url, products=[])


def get_seven_print(url: str) -> SevenPrint:
    host = "{uri.scheme}://{uri.netloc}".format(uri=urlparse(url))
    html = fetch_page(url)
    seven_print = extract_info(url, host, html)
    for index, next_page_url in enumerate(seven_print.pager_url):
        if index > 0:
            html = fetch_page(next_page_url)
        seven_print.products += extract_products(host, html)
    return seven_print
