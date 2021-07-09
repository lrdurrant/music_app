'''
Functions needed to analyze scraped reviews
Note: get_average_review_scores_and_count should be called first to aggregate album scores and remove duplicates
'''
# gets an average score from multiple reviews of same album
# alters num_of_reviews attribute to reflect number of times album has been reviewed
def get_average_review_scores_and_count(scraper_results):
    album_scores = {}

    # get all scores for each album
    for scraper_result in scraper_results:
        for album_review in scraper_result:
            if album_review['title'] not in album_scores:
                album_scores[album_review['title']] = album_review

            else:
                album_scores[album_review['title']]['score'] = str(float(album_scores[album_review['title']]['score']) + float(album_review['score']))
                album_scores[album_review['title']]['num_of_reviews'] = str(int(album_scores[album_review['title']]['num_of_reviews']) + 1)



    averaged_album_scores = []
    
    # average scores
    for title in album_scores:
        album_scores[title]['score'] = str(float(album_scores[title]['score']) / float(album_scores[title]['num_of_reviews']))
        averaged_album_scores.append(album_scores[title])
    
    return averaged_album_scores


# get albums that have a low number of reviews, but high score
def get_highest_rated_with_low_review_count(albums, number_of_albums='all'):
    if number_of_albums == 'all':
        sorted_albums = sorted(albums, key = lambda x: x['score'], reverse=True)
    
        
    return sorted_albums


