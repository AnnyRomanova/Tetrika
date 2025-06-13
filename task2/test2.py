from unittest.mock import patch, Mock
import pytest
from bs4 import BeautifulSoup
from collections import Counter

from solution import get_animals_from_page, get_next_page_url, sort_letters, get_soup


@pytest.fixture
def sample_soup():
    html = '''
        <div class="mw-category mw-category-columns">
            <li><a href="/wiki/Ягуар">Ягуар</a></li>
            <li><a href="/wiki/Дикобраз">Дикобраз</a></li>
            <li><a href="/wiki/Cat">Cat</a></li>
        </div>
        <div id="mw-pages">
            <a href="/wiki/Категория:Животные_по_алфавиту?pagefrom=NextPage">Следующая страница</a>
        </div>
    '''
    return BeautifulSoup(html, "lxml")


def test_get_animals_from_page(sample_soup):
    result = get_animals_from_page(sample_soup)
    assert result == Counter({'Д': 1, 'Я': 1, 'C': 1})


def test_get_next_page_url(sample_soup):
    url = get_next_page_url(sample_soup, "https://ru.wikipedia.org")
    assert url == "https://ru.wikipedia.org/wiki/Категория:Животные_по_алфавиту?pagefrom=NextPage"


def test_sort_letters():
    result = sort_letters(Counter({'C': 1, 'А': 2, 'Б': 3, 'Z': 4}))
    assert list(result.keys()) == ['А', 'Б', 'C', 'Z']


@patch("solution.requests.get")
def test_get_soup_mocked(mock_get):
    mock_response = Mock()
    mock_response.text = "<html><body>test</body></html>"
    mock_get.return_value = mock_response

    soup = get_soup("https://test.ru")
    assert isinstance(soup, BeautifulSoup)
    mock_get.assert_called_once()
