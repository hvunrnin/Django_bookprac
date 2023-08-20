import requests
import json
import os
import sys
from .models import Book

api_key = "ttbhmkwon09191336002"
api_url = "http://www.aladdin.co.kr/ttb/api/ItemList.aspx"

params = {
    "ttbkey": api_key,
    "Query": "소설",
    "MaxResults": 10  # 원하는 결과 수
}
response = requests.get(api_url, params=params)
data = response.json()
books = data.get('item')

for book_data in books:
    title = book_data.get('title', '')
    author = book_data.get('author', '')
    publication_year = int(book_data.get('pubDate', '0')[:4])
    genre = book_data.get('categoryName', '')
    publisher = book_data.get('publisher', '')

    book, created = Book.objects.get_or_create(
        title=title,
        author=author,
        publication_year=publication_year,
        genre=genre,
        publisher=publisher
    )

print("Data saved successfully.")