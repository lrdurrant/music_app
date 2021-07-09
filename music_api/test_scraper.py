from scraper.scrapers import *
import pytest


'''
ScraperBuilder tests
'''

# test building with invalid genre fails gracefully
def test_ScraperBuilder_invalid_genre():
    builder = ScraperBuilder()
    assert builder.build_scrapers('not_a_genre') == []

def test_ScraperBuilder_valid_genre():
    builder = ScraperBuilder()
    assert len(builder.build_scrapers('rap')) == 2


'''
RapScrapersBuilder tests
'''
# test number of scrapers built matches with scrapers known to the builder
def test_ScraperBuilder_num_of_scrapers():
    builder = RapScrapersBuilder()
    assert len(builder.build_scrapers()) == len(builder.scraper_dict)


'''
BaseScraper tests
'''
# test base class has no link
def test_BaseScraper_no_link():
    builder =  BaseScraper()
    assert builder.link == None

# test getting page with invalid link fails gracefully
def test_BaseScraper_invalid_link():
    builder =  BaseScraper()
    assert builder.get_page('not_a_valid_link') == None

# test getting an invalid page chunck fails gracefully
def test_BaseScraper_html_parsing_invalid_page():
    builder = BaseScraper()
    assert builder.get_page_chunk_html('invalid_page') == None

