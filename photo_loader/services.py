import asyncio
import base64
import os
import aiohttp
import aioftp
from django.core.files.uploadedfile import UploadedFile
import aiofiles


class FTPImagesProcessor:
    def __init__(self):
        # FTP Client session
        self.ftp = None

        # Semaphore for get_product_name function
        self.sem_get_product_name = asyncio.Semaphore(10)

    # FTP login function
    async def ftp_login(self):
        self.ftp = aioftp.Client()
        await self.ftp.connect(os.getenv('ftp_server'), 21)
        await self.ftp.login(os.getenv('ftp_username'), os.getenv('ftp_password'))
        await self.ftp.change_directory('DomostroyPhoto')
        await self.ftp.change_directory('1500x1500')

    # FTP images handling
    async def ftp_images_handling(self, files: UploadedFile):
        await self.ftp_login()
        user_encoded_files = list()
        server_encoded_files = list()
        tasks = list()

        for file in files:
            # Get user files data
            user_encoded_files.append({
                'data': base64.b64encode(file.read()).decode('utf-8'),
                'name': file.name
            })

            # If file exists then get its data or return file 404
            if await self.ftp.exists(file.name):
                async with self.ftp.download_stream(file.name) as stream:
                    server_file_data = await stream.read()

                server_encoded_files.append({
                    'data': base64.b64encode(server_file_data).decode('utf-8'),
                    'name': file.name
                })
            else:
                async with aiofiles.open('media/server_media/404.jpg', 'rb') as image_404:
                    server_encoded_files.append({
                        'data': base64.b64encode(await image_404.read()).decode('utf-8'),
                        'name': f'{file.name} (Не найден на сервере)'
                    })

            task = asyncio.create_task(self.get_product_name(file))
            tasks.append(task)

        product_names = await asyncio.gather(*tasks)

        # Ending the ftp client session
        self.ftp.quit()

        return [user_encoded_files, server_encoded_files, product_names]

    # Get the product name
    async def get_product_name(self, file: UploadedFile):
        # Split the file name by '.' and '_' to extract its base name
        base_file_name = file.name.split('.')[0].split('_')[0]
        vendor_code = base_file_name

        # Fetching product information from the Domostroy API and processing the results
        domostroy_api_key = os.getenv('domostroy_api_key')
        async with self.sem_get_product_name:
            async with aiohttp.ClientSession() as session:
                async with session.get(f'https://sort.diginetica.net/search?st={vendor_code}'
                                       f'&apiKey={domostroy_api_key}&fullData=true&withSku=true') as response:
                    domostroy_response = await response.json()

                    products = domostroy_response.get('products')
                    if not products or products[0].get('attributes').get('артикул')[0] != base_file_name:
                        return 'Название товара не найдено'

                    return products[0]['name']
