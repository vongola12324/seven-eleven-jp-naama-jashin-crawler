import json
from hashlib import sha1

from crawler import get_seven_print
from encoder import EnhancedJSONEncoder
from model import RequestedSevenPrint, RequestedSevenPrintForRender, SevenPrint, SevenPrintProduct
from render import render


def read_request_products_json() -> list[RequestedSevenPrint]:
    with open("request.json", "r", encoding="utf-8") as fd:
        items = [RequestedSevenPrint(**item) for item in json.load(fd)]
    return items


def dump_full_seven_print(seven_print: SevenPrint) -> None:
    with open(f"output/full/{seven_print.name}.json", "w", encoding="utf-8") as fd:
        json.dump(seven_print, fd, ensure_ascii=False, indent=4, cls=EnhancedJSONEncoder)


def dump_requested_seven_print(name: str, products: list[SevenPrintProduct]) -> None:
    with open(f"output/requested/{name}.json", "w", encoding="utf-8") as fd:
        json.dump(products, fd, ensure_ascii=False, indent=4, cls=EnhancedJSONEncoder)


def main():
    requested_items = read_request_products_json()
    final_products = []
    for requested_product in requested_items:
        print(f"Crawling {requested_product.name}")
        seven_print = get_seven_print(requested_product.url)
        dump_full_seven_print(seven_print)

        print(f"Filtering requested items: {requested_product.requested_id}")
        product_map = {
            pid: product
            for product in seven_print.products
            for pid in product.reservation_id.keys()
            if pid in requested_product.requested_id
        }
        products = [product_map[pid] for pid in requested_product.requested_id]
        dump_requested_seven_print(requested_product.name, products)
        print(f"> Done! Find [{len(products)}/{len(requested_product.requested_id)}]")
        final_products.append(
            RequestedSevenPrintForRender(
                pid=sha1(requested_product.name.encode("utf-8")).hexdigest(),
                name=requested_product.name,
                sell_end=seven_print.sell_end,
                products=products,
                requested=requested_product.requested_id,
            )
        )
    print("Generating HTML...")
    render(final_products)


if __name__ == "__main__":
    main()
