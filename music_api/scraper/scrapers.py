import requests
import re
from bs4 import BeautifulSoup
import dateparser

'''
Gets all scrapers needed for a genre
'''
class ScraperBuilder:
    def build_scrapers(self, genre, options=None):
        scrapers_list = []
        if genre == 'rap':
            rap_scraper_builder = RapScrapersBuilder()
            scrapers_list = rap_scraper_builder.build_scrapers()
        if genre == 'rock':
            pass
        if genre == 'jazz':
            pass
        else:
            pass

        return scrapers_list

'''
Builds web scrapers for each target rap genre review site
'''
class RapScrapersBuilder:
    def __init__(self):
        # add another entry here to let the builder know to build a new web scraper
        self.scraper_dict = {'pitchfork' : 'https://pitchfork.com/reviews/albums/?genre=rap',
                             'rapreviews' : 'https://www.rapreviews.com/category/review/'
                            }
    def build_scrapers(self, options=None):
        scrapers = []
        # add a new webname and scraper constructor here to build a new scraper
        for web_name in self.scraper_dict:
            if web_name == 'pitchfork':
                # create pitchfork scraper
                new_scraper = PitchforkScraper(self.scraper_dict[web_name])
            elif web_name == 'rapreviews':
                # create rapreviews scraper
                new_scraper = RapreviewsScraper(self.scraper_dict[web_name])
            else:
                # no match
                new_scraper = None

            if new_scraper:
                scrapers.append(new_scraper)
        
        return scrapers

'''
A base scraper method for common functionality
'''
class BaseScraper:
    def __init__(self):
        self.link = None
    
    def get_page(self, link):
        try:
            page = requests.get(link)
        except:
            page = None
        
        if page and page.ok:
            return page

    def get_page_chunk_html(self, page):
        try:
            soup_page = BeautifulSoup(page.content, 'html.parser')
        except:
            soup_page = None
        
        return soup_page

'''
For scraping funtionality that is specific to Pitchfork website
'''
class PitchforkScraper(BaseScraper):
    def __init__(self, full_link):
        self.full_link = full_link
        self.base_link = 'https://pitchfork.com'

    # structure of pitchfork review page is good for grabbing each album html separately
    def get_album_reviews_html(self, all_reviews_html):
        return all_reviews_html.findAll("div", {"class": "review"})

    # pitchfork album scores are not on main review page
    # score for album must be accessed on separate review page
    def get_album_score(self, album_review_link):
        score_page = self.get_page_chunk_html(self.get_page(album_review_link))

        # check for errors
        return score_page.find('span', class_='score').text

    # get an album review with all the needed info
    def get_album_review_with_attributes(self, review_html):
        album_review = {}
        try:
            album_title = review_html.find('h2', class_='review__title-album').text
            album_artist = review_html.find('ul', class_='artist-list review__title-artist').text
            album_date = review_html.find('time', class_='pub-date').text
            album_date = str(dateparser.parse(album_date))
            review_score_link = self.base_link + review_html.find('a')['href']
            album_score = self.get_album_score(review_score_link)


            album_review['title'] = album_title
            album_review['artist'] = album_artist
            album_review['date'] = album_date
            album_review['score'] = album_score
            album_review['num_of_reviews'] = '1'
        except:
            album_title = ''
        
        # only return an album review if necessary attributes have a value
        if album_title and album_artist and album_date and album_score:
            return album_review
        else:
            return {}
    
    # function to get every album availble on Pitchfork website front page
    def get_all_albums_reviews(self):
        all_album_reviews = []
        review_page_chunk = self.get_page_chunk_html(self.get_page(self.full_link))
        album_reviews_html = self.get_album_reviews_html(review_page_chunk)

        if album_reviews_html:
            for review in album_reviews_html:
                album = self.get_album_review_with_attributes(review)
                if album:
                    all_album_reviews.append(album)
        
        return all_album_reviews

'''
For scraping functionality related to Rapreviews website
'''
class RapreviewsScraper(BaseScraper):
    def __init__(self, full_link):
        self.full_link = full_link


    def get_album_reviews_html(self, all_reviews_html):
        # an individual review is under an id tag with format <post-XXXXX>
        return all_reviews_html.findAll("article", {"id": re.compile('post-')})

    # get an album review with all the needed info  
    def get_album_review_with_attributes(self, review_html):
        album_review = {}

        try:
            # title and artist are in the following format: <title :: artist>
            album_title_and_artist = review_html.find('h2', class_='cb-post-title').text.split('::')
            album_title, album_artist = album_title_and_artist[0], album_title_and_artist[1]
            album_date = review_html.find('time').text
            album_date = str(dateparser.parse(album_date))
            album_score = review_html.find('span', class_='cb-score').text


            album_review['title'] = album_title
            album_review['artist'] = album_artist
            album_review['date'] = album_date
            album_review['score'] = album_score
            album_review['num_of_reviews'] = '1'
        except:
            album_title = ''
        
        # only return an album review if necessary attributes have a value
        if album_title and album_artist and album_date and album_score:
            return album_review
        else:
            return {}

    def get_all_albums_reviews(self):
        all_album_reviews = []
        review_page_chunk = self.get_page_chunk_html(self.get_page(self.full_link))
        album_reviews_html = self.get_album_reviews_html(review_page_chunk)

        if album_reviews_html:
            for review in album_reviews_html:
                album = self.get_album_review_with_attributes(review)
                if album:
                    all_album_reviews.append(album)
        
        return all_album_reviews


