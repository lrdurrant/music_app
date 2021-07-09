from scraper.scrapers import *
from analyzer.analyze import *
from spotify_api.spotify_api_helpers import similar, get_album_art_url, add_album_art_to_albums
import flask
from flask import request, jsonify
import sqlite3


app = flask.Flask(__name__)
app.config["DEBUG"] = True

def scraper_helper(genre):
        builder = ScraperBuilder()
        scrapers = builder.build_scrapers(genre)

        if not scrapers:
            return None
        scrape_results = []
        
        for scraper in scrapers:
            scrape_results.append(scraper.get_all_albums_reviews())

        return scrape_results


@app.route('/', methods=['GET'])
def home():
    return '''<h1>App for finding best new music</h1>'''


@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404

'''
Main get call to receive scaped albums based on genre, filter and score
'''
@app.route('/api/v1/resources/albums', methods=['GET'])
def api_album_filter():
    query_parameters = request.args

    genre = query_parameters.get('genre')
    album_search_filter = query_parameters.get('filter')
    min_score = query_parameters.get('min-score')

    if genre:
        scrape_results = scraper_helper(genre)
        
        if not scrape_results:
            return page_not_found(404)

        average_review_scores = get_average_review_scores_and_count(scrape_results)
    
    if album_search_filter:
        if album_search_filter == 'low-review-count':
            filtered_results = get_highest_rated_with_low_review_count(average_review_scores)
        else:
            filtered_results = average_review_scores
    
    if min_score:
        filtered_results = [album for album in filtered_results if float(album['score']) > float(min_score)]

    add_album_art_to_albums(filtered_results)
    print(filtered_results)
    
    if not (genre or album_search_filter or min_score):
        return page_not_found(404)

    return jsonify(filtered_results)


app.run()
