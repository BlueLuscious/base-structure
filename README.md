# gea-trader-core

## Description

gea-trader-core is the product management system used by the GEA Trader
company. It is a Django application providing CRUD operations, business
logic and a translation workflow for managing products and related data.

## Requirements

- Python 3.11+ (run in a virtual environment)
- Docker (used to run the PostgreSQL development database)
- gettext tools for message catalog management (see [Translations](#translations) below)

## Development setup

Follow these steps to get a development copy running locally:

1. **Clone the repository**

   ```bash
   git clone https://github.com/BlueLuscious/gea-trader-core.git
   cd gea-trader-core
   ```
2. **Create and activate a virtual environment**

   ```bash
   python -m venv .venv

   # Windows
   .venv\Scripts\activate

   # Unix/macOS
   source .venv/bin/activate
   ```
3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```
4. **Run Docker**

   The PostgreSQL server used for development is provided by Docker; the
   Django application runs on your host but connects to the container.
   Bring up the database service before running any migration or the
   server

   ```bash
   docker compose up -d
   ```
5. **Apply migrations**

   ```bash
   python manage.py migrate
   ```
6. **Run the development server**

   ```bash
   python manage.py runserver
   ```

   Done!

## Translations

The project uses Django's internationalization framework. To work with
translations you will need the GNU gettext utilities. On Windows you can
download a build from the following link:

- [Gettext for Windows](https://github.com/mlocati/gettext-iconv-windows/releases/tag/v1.0-v1.18-r3)

To extract new strings and create or update message files:

```bash
python manage.py makemessages -l <lang> --ignore .venv --ignore node_modules --ignore '*.txt'
```

After editing the `.po` files, compile them so Django can use them:

```bash
python manage.py compilemessages -l <lang>
```
