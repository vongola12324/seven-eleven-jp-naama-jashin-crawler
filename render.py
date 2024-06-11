import arrow

from model import RequestedSevenPrintForRender


def generate_product_image_block(name: str, token: str, image: str):
    return f"""
    <div class="flex flex-wrap w-full sm:w-1/2 md:w-1/3 lg:w-1/4 xl:w-1/5 2xl:w-1/6 print:w-1/3 print:break-inside-avoid">
      <div class="w-full p-1 md:p-2">
        <img
          alt="{name}"
          class="block w-full rounded-lg object-cover object-center"
          src="{image}" />
        <p class="text-center">
          <span class="text-2xl">{name}</span><br>
          <span class="text-sm text-slate-600">{token}</span>
        </p>
      </div>
    </div>
    """


def generate_product_block(seven_print: RequestedSevenPrintForRender, add_page_break: bool = False) -> str:
    image_blocks = []
    for product in seven_print.products:
        if len(product.reservation_id) > 1:
            token = list(filter(lambda x: x[0] in seven_print.requested, product.reservation_id.items()))[0][0]
        else:
            token = list(product.reservation_id.keys())[0]
        block = generate_product_image_block(product.name, token, product.image)
        image_blocks.append(block)
    return f"""
    <div class="-m-1 flex flex-wrap md:-m-2 products hidden print:flex {'print:break-before-page' if add_page_break else ''}" id="block-{seven_print.pid}">
        <div class="hidden print:flex print:justify-center print:items-center pt-2 pb-4 w-full">
            <p class="text-blue-500 font-bold text-xl">
                {seven_print.name}
                <span class="p-1 text-center align-baseline text-xs leading-none text-red-500 font-bold">
                    ({len(seven_print.products)})
                </span>
            </p>
        </div>
        {"".join(image_blocks)}
    </div>
    """


def generate_tab_item(name: str, pid: str, count: int) -> str:
    return f"""
    <li role="presentation">
        <a href="#"
           class="block border-x-0 border-b-2 border-t-0 border-transparent px-2 py-2 text-xs font-medium uppercase hover:isolate hover:border-transparent hover:bg-neutral-100 hover:text-red-500 focus:isolate focus:border-transparent data-[tab-active]:text-blue-500 data-[tab-active]:font-bold"
           id="tab-{pid}"
           data-product-id="{pid}"
           onclick="javascript:changeProduct(this.id)"
           role="tab">
            {name}
            <span class="inline-block rotate-0 skew-x-0 skew-y-0 whitespace-nowrap rounded-full bg-red-800 p-1 text-center align-baseline text-xs leading-none text-white">
                {count}
            </span>
        </a>
    </li>
    """


def generate_tabs(seven_prints: list[RequestedSevenPrintForRender]) -> str:
    tab_items = [
        generate_tab_item(seven_print.name, seven_print.pid, len(seven_print.products)) for seven_print in seven_prints
    ]
    return f"""
    <div class="flex flex-col items-center print:hidden">
        <ul class="flex list-none flex-row flex-wrap border-b-0 ps-0" role="tablist">
            {"".join(tab_items)}
        </ul>
      </div>
    """


def render(seven_prints: list[RequestedSevenPrintForRender]) -> None:
    tabs = generate_tabs(seven_prints)
    blocks = []
    for index, seven_print in enumerate(seven_prints):
        blocks.append(generate_product_block(seven_print, index >= 1))

    with open("template/index.html", "r", encoding="utf-8") as fd:
        html = fd.read()
    html = html.replace("{{{ tabs }}}", tabs)
    html = html.replace("{{{ blocks }}}", "".join(blocks))
    html = html.replace("{{{ defaultTabId }}}", f"tab-{seven_prints[0].pid}")
    html = html.replace("{{{ generateTime }}}", arrow.now().format("YYYY-MM-DD HH:mm:ss ZZZ"))
    with open(f"output/index-{arrow.now().format('YYYY-MM-DD-HH-mm-ss')}.html", "w+", encoding="utf-8") as fd:
        fd.write(html)
