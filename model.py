from dataclasses import dataclass
from datetime import datetime


@dataclass
class SevenPrintProduct:
    name: str
    image: str
    reservation_id: dict[str, str]  # {token: size}


@dataclass
class SevenPrint:
    name: str
    url: str
    sell_end: str
    pager_url: list[str]
    products: list[SevenPrintProduct]


@dataclass
class RequestedSevenPrint:
    name: str
    url: str
    requested_id: list[str]


@dataclass
class RequestedSevenPrintForRender:
    pid: str
    name: str
    sell_end: str
    products: list[SevenPrintProduct]
    requested: list[str]
