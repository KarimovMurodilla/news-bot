import aiohttp
import asyncio
import gzip
from io import BytesIO
from bs4 import BeautifulSoup

async def fetch_html(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
    }

    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(url) as response:
            # Check if the response is successful
            if response.status == 200:
                # Read the response content
                raw_content = await response.read()
                return raw_content
                
                # Check if the response is gzip-encoded
            #     if response.headers.get('Content-Encoding') == 'gzip':
            #         # Decompress the gzip-encoded content
            #         buffer = BytesIO(raw_content)
            #         with gzip.GzipFile(fileobj=buffer) as f:
            #             decompressed_content = f.read()
            #     else:
            #         decompressed_content = raw_content

            #     # Decode the decompressed content to a string
            #     html_content = decompressed_content.decode('utf-8', errors='ignore')
            #     return html_content
            # else:
            #     print(f"Failed to retrieve content: Status {response.status}")
            #     return None

async def parse_html(url):
    html_content = await fetch_html(url)
    if html_content:
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Example: Extract all image URLs
        all_images = soup.find_all('img')
        for img in all_images:
            if 'src' in img.attrs:
                img_src = img['src']
                print(f"Image src: {img_src}")
    else:
        print("No HTML content to parse.")

async def main():
    url = 'https://xabar.uz/uz/siyosat'
    await parse_html(url)

# Run the main function
asyncio.run(main())
