import requests
from bs4 import BeautifulSoup

# Headers to prevent 403 Forbidden error
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate",
    "Accept": "text/html",
}

session = requests.Session()
session.headers.update(HEADERS)


# Initialize BeautifulSoup
def get_soup(url):
    try:
        response = session.get(url, timeout=15)
        response.raise_for_status()
        return BeautifulSoup(response.content, "html.parser")
    except requests.exceptions.RequestException as exc:
        print(f"An error occurred: {exc}")
        return None


# Get the IMDB rating from the IMDB page
def get_imdb_rating(imdb_id):
    if imdb_id:
        imdb_url = f"https://www.imdb.com/title/{imdb_id}/"
        soup = get_soup(imdb_url)
        if soup:
            imdb_rating = soup.find(
                "div", {"data-testid": "hero-rating-bar__aggregate-rating__score"}
            )
            if imdb_rating:
                return imdb_rating.text[:-3]
    return None


# Get Rotten Tomatoes URL from the search page
def get_rt_url(title, year, media_type):
    search_url = f"https://www.rottentomatoes.com/search?search={title}"
    soup = get_soup(search_url)
    if soup:
        attributes = {}
        if media_type == "Movie":
            attributes["releaseyear"] = year
        else:
            attributes["startyear"] = year

        search_result = soup.find("search-page-media-row", attributes)
        if search_result:
            url_tag = search_result.find("a", {"data-qa": "info-name"})
            return url_tag["href"]
    return None


# Get Rotten Tomatoes scores from the Rotten Tomatoes page
def get_rt_scores(rt_url):
    if rt_url:
        soup = get_soup(rt_url)
        if soup:
            score_board = soup.find("score-board-deprecated")
            if score_board:
                return {
                    "tomatometer": score_board.get("tomatometerscore"),
                    "tomatometer_state": score_board.get("tomatometerstate"),
                    "audience_score": score_board.get("audiencescore"),
                    "audience_state": score_board.get("audiencestate"),
                }
    return None
