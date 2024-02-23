# Define your item pipelines here
import sqlite3
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem

class FoodmanduPipeline:
 # Constructor method to initialize the database connection and table creation
    def __init__(self):
        self.create_connection()
        self.create_table()

    def create_connection(self):
        self.conn = sqlite3.connect("foodmandu.db")
    
    def create_table(self):
        self.conn.execute("""DROP TABLE IF EXISTS restaurants""")
        self.conn.execute("""
        Create TABLE restaurants (
            url TEXT,
            image TEXT,
            name TEXT,
            address TEXT,
            cuisine TEXT
        )
    """)

    # Method to process each item scraped
    def process_item(self, item, spider):
        self.store_db(item)
        return item
    
    def store_db(self,item):
        self.conn.execute("""INSERT INTO restaurants (url,image,name,address,cuisine) VALUES (?,?,?,?,?)""",(
            item['url'],
            item['image'],
            item['name'],
            item['address'],
            item['cuisine']
        ))
        #Committing the transaction to save changes to the database
        self.conn.commit()

class DuplicatesPipeline:

    def __init__(self):
        self.visited_urls = set()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if adapter['url'] in self.visited_urls:
            raise DropItem(f"Duplicate item found: {item!r}")
        else:
            self.visited_urls.add(adapter['url'])
            return item