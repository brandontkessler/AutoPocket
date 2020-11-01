import requests
from bs4 import BeautifulSoup
from collections import namedtuple


def aggregate_articles(soup_articles):
    """soup_articles should be a list of A tags
    """

    ArticleRecord = namedtuple('ArticleRecord', 'title, url')
    articles = []

    for article in soup_articles:
        article_title = article.get_text()
        article_url = f"{article.get('href')}"
        
        articles.append(ArticleRecord(article_title, article_url))
    
    return articles


def guardian(limit=10):
    url = 'https://www.theguardian.com/us'
    guardian = requests.get(url)
    soup = BeautifulSoup(guardian.content, 'html.parser')
    headlines = soup.find('div', {'data-title': 'Headlines'})

    # Get all articles from the headlines, filtering out any articles that have 
    #   a class that contains any of the strings in the class_filters list.
    class_filters = ['fc-sublink__link', 'faux']
    headline_articles = [
        headline for headline in headlines.findAll(
            "a", {"data-link-name": "article"}
        ) if not any([
            filter in h_class for h_class in headline['class'] for filter in class_filters
        ])
    ]

    articles = aggregate_articles(headline_articles)
    
    return articles[:limit]


def vice(limit=10):
    url = 'https://www.vice.com/en'
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')


    articles = soup.findAll('a', {'class': 'vice-card-hed__link'})

    aggregate = aggregate_articles(articles)

    return aggregate[:limit]

    
if __name__=='__main__':
    # guardian()
    vice()