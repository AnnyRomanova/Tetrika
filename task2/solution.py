import requests
from bs4 import BeautifulSoup
from collections import Counter
import csv


def get_soup(url):
    response = requests.get(url)
    return BeautifulSoup(response.text, "lxml")


def get_animals_from_page(soup):
    letter_counts = Counter()
    data = soup.find("div", class_="mw-category mw-category-columns")
    if data:
        animal_list = data.find_all("li")
        for animal in animal_list:
            name = animal.find("a").text
            letter_counts[name[0].upper()] += 1
    return letter_counts


def get_next_page_url(soup, base_url):
    next_page_div = soup.find("div", id="mw-pages")
    if not next_page_div:
        return None
    for link in next_page_div.find_all("a"):
        if link.text.strip() == "Следующая страница":
            return base_url + link.get("href")
    return None


def collect_all_animals(start_url, base_url="https://ru.wikipedia.org"):
    url = start_url
    visited_urls = set()
    total_counts = Counter()

    while url and url not in visited_urls:
        visited_urls.add(url)
        soup = get_soup(url)
        total_counts.update(get_animals_from_page(soup))
        url = get_next_page_url(soup, base_url)

    return total_counts


def sort_by_key(item):
    return item[0]


def sort_letters(counter: Counter) -> dict:
    cyrillic = []
    latin = []
    for symbol, count in counter.items():
        if ('А' <= symbol <= 'я') or symbol in ('ё', 'Ё'):
            cyrillic.append((symbol, count))
        else:
            latin.append((symbol, count))
    return dict(sorted(cyrillic, key=sort_by_key) + sorted(latin, key=sort_by_key))


def save_to_csv(counter, filename="beasts.csv"):
    sorted_counter = sort_letters(counter)
    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        for letter, count in sorted_counter.items():
            writer.writerow([letter, count])


# Главная точка входа
if __name__ == "__main__":
    start_url = "https://ru.wikipedia.org/wiki/Категория:Животные_по_алфавиту"
    letter_counts = collect_all_animals(start_url)
    save_to_csv(letter_counts)
