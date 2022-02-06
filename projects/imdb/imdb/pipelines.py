# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import pymongo
import sqlite3


class MongoDBPipeline:
    collection_name = "best_movies"

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(
            "mongodb+srv://admin:admin@imdb.fluvw.mongodb.net/imdb?retryWrites=true&w=majority")
        self.db = self.client["imdb"]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[self.collection_name].insert_one(item)
        return item


class SQLitePipeline:
    def open_spider(self, spider):
        self.connection = sqlite3.connect('imdb.db')
        self.c = self.connection.cursor()
        try:
            self.c.execute('''
                CREATE TABLE 
                        best_movies(
                        title TEXT,
                        year TEXT,
                        duration TEXT,
                        genre TEXT,
                        rating TEXT,
                        movie_url TEXT
                    )
            ''')
        except:
            pass
        self.connection.commit()

    def close_spider(self, spider):
        self.connection.close()

    def process_item(self, item, spider):
        self.c.execute(
            '''
                INSERT INTO 
                    best_movies(title, year, duration, genre, rating, movie_url)
                VALUES
                    (?, ?, ?, ?, ?, ?)
            ''', 
            (
                item.get("title"),
                item.get("year"),
                item.get("duration"),
                item.get("genre"),
                item.get("rating"),
                item.get("movie_url"),
            )
        )
        self.connection.commit()
        return item
