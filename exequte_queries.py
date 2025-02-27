import sqlite3
from connector_db import DBConnector


class QueryHandler(DBConnector):
    def __init__(self, dbconfig):
        super().__init__(dbconfig)
        self.sqlite_conn = sqlite3.connect('search_history.db')
        self.sqlite_cursor = self.sqlite_conn.cursor()

    def save_search_query(self, query):
        self.sqlite_cursor.execute('''
            INSERT INTO search_history (search_query) VALUES (?)
        ''', (query,))
        self.sqlite_conn.commit()

    def get_film_by_keyword(self, keyword):
        cursor = self.get_cursor()
        query = """
            SELECT f.title, f.release_year, c.name
            FROM film AS f 
            JOIN film_category AS fc ON f.film_id = fc.film_id
            JOIN category AS c ON fc.category_id = c.category_id
            WHERE f.title LIKE %s OR f.description LIKE %s
        """
        cursor.execute(query, (f"%{keyword}%", f"%{keyword}%"))
        records = cursor.fetchall()


        self.save_search_query(f"Keyword: {keyword}")

        return records

    def get_film_by_janr_and_year(self, genre, year):
        cursor = self.get_cursor()
        query = """
            SELECT f.title, f.release_year, c.name
            FROM film AS f 
            JOIN film_category AS fc ON f.film_id = fc.film_id
            JOIN category AS c ON fc.category_id = c.category_id
            WHERE c.name = %s AND f.release_year = %s
        """
        cursor.execute(query, (genre, year))
        records = cursor.fetchall()

        self.save_search_query(f"Genre: {genre}, Year: {year}")

        return records

    def get_popular_searches(self):
        self.sqlite_cursor.execute('''
            SELECT search_query, COUNT(*) as search_count 
            FROM search_history 
            GROUP BY search_query 
            ORDER BY search_count DESC 
            LIMIT 10
        ''')
        return self.sqlite_cursor.fetchall()

    def close(self):
        self.sqlite_conn.close()