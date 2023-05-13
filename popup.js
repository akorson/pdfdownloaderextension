import re
import requests
from bs4 import BeautifulSoup
import asyncio

class PDFDownloader:

    @staticmethod
    async def get_pdf_urls(url):
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(None, requests.get, url)
        soup = BeautifulSoup(response.text, 'html.parser')
        links = []
        for link in soup.find_all("a"):
            href = str(link.get('href', ''))
            if ".pdf" in href:
                links.append(href)
        return links

    @staticmethod
    async def download_pdfs(pdf_urls):
        async def download_pdf(url):
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(None, requests.get, url)
            filename = url.split("/")[-1]
            with open(filename, 'wb') as f:
                f.write(response.content)

        tasks = [download_pdf(url) for url in pdf_urls]
        await asyncio.gather(*tasks)

    @staticmethod
    async def generate_url_with_sort(url, links):
        sorted_links = sorted([(re.search(r'\d{7}', i).group(0), i) for i in links])
        return [url + y for x, y in sorted_links]

    @staticmethod
    async def get_sorted_pdf_urls(url):
        pdf_links = await PDFDownloader.get_pdf_urls(url)
        return await PDFDownloader.generate_url_with_sort(url, pdf_links)

    @staticmethod
    async def run(url):
        pdf_links = await PDFDownloader.get_sorted_pdf_urls(url)
        await PDFDownloader.download_pdfs(pdf_links)