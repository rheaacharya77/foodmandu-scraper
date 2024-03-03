# Foodmandu Scraper
Foodmandu Scraper extracts restaurant information from [FOODMANDU](https://foodmandu.com/Restaurant/Index) using Scrapy and Playwright. It captures details such as restaurant URLs, images, names, addresses, and cuisines. The extracted data is then stored in a SQLite database.

## Setup
To set up the project, follow these steps:

#### 1. Clone the Repository:

bash
git clone https://github.com/rheaacharya77/foodmandu-scraper.git

#### 2. Navigate to the Project Directory:

bash
cd foodmandu

#### 3. Create and Activate a Virtual Environment

bash
python -m venv venv

bash
source venv/bin/activate

#### 4. Install the Required Dependencies:
bash
pip install -r requirements.txt

#### 5. You're now ready to start using the scraper!

## Project Structure

Here's an overview of the key components in the Foodmandu Scraper project:

- `/.github/workflows/`: Contains the GitHub Actions workflow files for automation.
- `/foodmandu/`: The main project directory with all the Scrapy components.
  - `/spiders/`: Contains the spider `restaurants.py` that defines the scraping logic.
  - `items.py`: Defines the data structure for scraped data.
  - `middlewares.py`: Manages custom middleware for Scrapy.
  - `pipelines.py`: Processes and stores data items after scraping.
  - `settings.py`: Configures settings for Scrapy.
- `foodmandu.db`: The SQLite database where scraped data is stored.
- `requirements.txt`: Lists all the dependencies required to run the project.
- `scrapy.cfg`: Configuration file for Scrapy projects.

## Usage

Modify the scraping settings in `settings.py` as needed, then run the scraper with:

bash
scrapy crawl restaurants

## Pipeline

The scraper employs two main pipelines in `pipelines.py` for processing and storing scraped data:

#### FoodmanduPipeline
- Manages SQLite database interactions by establishing a connection, creating a fresh `restaurants` table, and inserting scraped data.

#### DuplicatesPipeline
- Eliminates duplicate data by checking against a set of visited URLs and dropping any repeats during the scraping session.

These pipelines ensure efficient data storage and integrity by managing database operations and eliminating duplicate data.

## Data Schema
The scraped restaurant data is stored in a SQLite database, utilizing a table with the following schema:

- `id`: An auto-incrementing integer that serves as the primary key.
- `url`: Text field storing the restaurant's URL.
- `image`: Text field storing the URL of the restaurant's image.
- `name`: Text field for the restaurant's name.
- `address`: Text field for the restaurant's address.
- `cuisine`: Text field describing the type of cuisine offered by the restaurant.

This schema is designed to capture essential details about each restaurant, facilitating easy access and analysis of the collected data.

## Github Actions
GitHub Actions is used to automate the scraping process and ensure our data is always up to date. The workflow, defined in `.github/workflows/actions.yml`, performs the following tasks:

- **Trigger**: It's set to run automatically every Saturday at 7:30 PM UTC. Additionally, it can be manually triggered via GitHub's `workflow_dispatch` event.
- **Environment Setup**: Prepares an Ubuntu environment, sets up Python 3.10, and installs all necessary dependencies from `requirements.txt`.
- **Data Scraping**: Executes our Scrapy spider named `restaurants` to scrape the latest restaurant data.
- **Commit**: Any changes in the data are committed to the repository with a timestamp.
- **Push**: Updates the main branch with the latest data.

This automated workflow minimizes manual effort and keeps our data fresh with scheduled and on-demand runs.

## Contributing
Contributions are welcome! Here's how to contribute:

1. **Fork** the repo and **clone** your fork.
2. **Create a branch** for your changes.
3. **Make your changes** and **test** them.
4. **Commit** your changes with clear messages.
5. **Submit a pull request (PR)** with a detailed description of your changes.

Thank you for helping improve the Foodmandu Scraper!


