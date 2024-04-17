# DomostroyPhotoLoader

DomostroyPhotoLoader is a web application developed using Python Django framework and asynchronous libraries such as aiofiles, aioftp, and aiohttp. It also utilizes PostgreSQL as the database and python-dotenv for managing environment variables.

## Overview

DomostroyPhotoLoader is designed to streamline the process of uploading photos to an FTP server in a specific naming format for the Domostroy online store. It provides photographers with the ability to upload photos and compare them with existing ones on the FTP server, allowing them to determine whether replacements are necessary. The application automatically retrieves product names via an API, ensuring that photographers insert the correct SKU for each photo. Additionally, it includes a basic Django authentication system.

## Technologies Used

* Python
* Django
* Asynchronous programming (aiofiles, aioftp, aiohttp)
* PostgreSQL
* python-dotenv

## Features

Photo upload to FTP server with standardized naming convention (SKU_PHOTO_NUMBER.extension)
Comparison of uploaded photos with existing ones on the FTP server
Automatic retrieval of product names via API
Basic Django authentication system

## Installation

- Clone the repository:

```bash
git clone https://github.com/Dellenoam/DomostroyPhotoLoader.git
```

- Move to the cloned folder

```bash
cd DomostroyPhotoLoader
```

- Create virtual environment:

```bash
python3 -m venv .venv
```

- Activate virtual environment:

```bash
source .venv/bin/activate
```

- Install dependencies:

```bash
pip install -r requirements.txt
```

- Set up your PostgreSQL database. Simple example below

Linux
```bash
psql -d postgres -U postgres
CREATE DATABASE "YOUR_DATABASE_NAME";
\q
```

MacOS
```bash
psql postgres
CREATE DATABASE "YOUR_DATABASE_NAME";
\q
```

- Create .env file and set these variables

```
secret_key = YOUR_SECRET_KEY
allowed_host = YOUR_ALLOWED_HOST
ftp_server = YOUR_FTP_SERVER
ftp_username = YOUR_FTP_USERNAME
ftp_password = YOUR_FTP_PASSWORD
domostroy_api_key = YOUR_API_KEY
db_name = YOUR_DB_NAME
db_user = YOUR_DB_USER
db_password = YOUR_DB_PASSWORD
db_host = YOUR_DB_HOST
db_port = YOUR_DB_PORT
debug = True/False
```

Make migrations and apply them
```bash
python manage.py makemigrations
python manage.py migrate
```

Create superuser
```
python manage.py createsuperuser
```

Start the development server:
```bash
python manage.py runserver
```

Access the application at http://localhost:8000/.

# License

This project is licensed under the Apache 2.0 License.
