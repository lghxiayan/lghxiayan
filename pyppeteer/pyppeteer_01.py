import asyncio
from pyppeteer import launch
from pyquery import PyQuery as pq


async def main():
    browser = await launch()
    page = await browser.newPage()
    # await page.goto('http://quotes.toscrape.com/js/')
    await page.goto('https://etax99.hubei.chinatax.gov.cn:5100/')
    doc = pq(await page.content())
    print(doc)
    print('Quotes:', doc('.quote').length)
    await browser.close()


asyncio.get_event_loop().run_until_complete(main())
