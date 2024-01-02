import requests
from dotenv import load_dotenv
from urllib.parse import quote
from unidecode import unidecode
import os
import re
from scraper import get_imdb_rating, get_rt_url, get_rt_scores


load_dotenv()

TMDB_API_KEY = os.getenv("TMDB_API_KEY")

session = requests.Session()


## Search for Movie or TV show to generate search results


# Sanitize user input and search in TMDB API
def search_title(user_input):
    title = quote(user_input)
    url = f"https://api.themoviedb.org/3/search/multi?api_key={TMDB_API_KEY}&query={title}&include_adult=false&language=en-US&page=1"
    search_results = get_search_results(url)
    clean_results = clean_search_results(search_results)

    # If no results are found, return None
    if not clean_results:
        return None

    return clean_results


# Get search results from TMDB API
def get_search_results(url):
    try:
        response = session.get(url)
        response.raise_for_status()
    except requests.HTTPError as http_error:
        print(f"HTTP error occurred: {http_error}")
        return None

    return response.json()


# Clean search results and return only the relevant details
def clean_search_results(search_results):
    base_poster_url = "https://www.themoviedb.org/t/p/w185"
    # Keep track of TMDB ids that are already seen to avoid duplicates
    checked_tmdb_ids = set()
    clean_results = []

    for result in search_results["results"]:
        tmdb_id = result.get("id")
        poster_path = result.get("poster_path")
        media_type = result.get("media_type")
        poster_image = get_poster_image(base_poster_url, poster_path)

        # If the TMDB id is not already seen, add it to the set and get the clean results
        if tmdb_id not in checked_tmdb_ids:
            checked_tmdb_ids.add(tmdb_id)
            clean_result = get_clean_results(result, media_type, tmdb_id, poster_image)

            # Append to the clean results if it's a not an existing result
            if clean_result:
                clean_results.append(clean_result)

    return clean_results


# Get the poster image for the search results
def get_poster_image(base_poster_url, poster_path):
    # Use image placeholder if no poster file path exists
    if poster_path is None:
        return "/static/img/no_poster.webp"
    else:
        return f"{base_poster_url}{poster_path}"


# Get the clean results for the search results for both Movie and TV shows
def get_clean_results(result, media_type, tmdb_id, poster_image):
    if media_type == "movie":
        return {
            "tmdb_id": tmdb_id,
            "title": result.get("title"),
            "year": result.get("release_date")[0:4],
            "media_type": media_type.title(),
            "poster_image": poster_image,
        }

    elif media_type == "tv":
        return {
            "tmdb_id": tmdb_id,
            "title": result.get("name"),
            "year": result.get("first_air_date")[0:4],
            "media_type": media_type.upper(),
            "poster_image": poster_image,
        }


## Fetch all details of the selected Movie or TV show


# Get the details of the selected title
def get_media_details(tmdb_id, media_type, TMDB_API_KEY):
    url = f"https://api.themoviedb.org/3/{media_type.lower()}/{tmdb_id}?api_key={TMDB_API_KEY}&language=en-US&append_to_response=release_dates,watch/providers,external_ids,credits,videos"
    response = session.get(url)
    response.raise_for_status()

    return response.json()


# Get the poster image for the selected title
def get_poster_details(media_details):
    poster_path = media_details.get("poster_path")
    poster_image = (
        f"https://image.tmdb.org/t/p/w500{poster_path}"
        if poster_path
        else "/static/img/no_poster.webp"
    )

    return poster_image


# Get the runtime for the selected title
def get_runtime(media_details):
    runtime = media_details.get("runtime")
    if runtime:
        hours, minutes = divmod(runtime, 60)
        return f"{hours}h {minutes}m"
    return None


# Format the title to be used in the URL for Rotten Tomatoes
def format_title(title):
    title = unidecode(title)  # Replace special characters
    title = title.lower()  # Convert to lowercase
    title = title.replace("&", "and")  # Replace & with and
    title = title.replace("'", "")  # Remove apostrophes
    title = re.sub(r"\W+", " ", title)  # Remove all non-alphanumeric characters
    title = title.replace(" ", "_")  # Replace spaces with underscores
    return title


# Get the director(s) for the selected title if it's a Movie
def get_director(media_details):
    crew = media_details.get("credits", {}).get("crew", [])
    directors = []
    for director in crew:
        if director.get("job") == "Director":
            directors.append(director.get("name"))
    return directors


# Get the creator(s) for the selected title if it's a TV show
def get_creator(media_details):
    creators = media_details.get("created_by", [])
    creator_names = []
    for creator in creators:
        creator_names.append(creator.get("name"))
    return creator_names


# Get the genre(s) for the selected title
def get_genre(media_details):
    genres = media_details.get("genres", [])
    genre_names = []
    for genre in genres:
        genre_names.append(genre.get("name"))
    return genre_names


# Get the YouTube trailer ID for the selected title using IMDb ID
def get_youtube_trailer_id(media_details):
    videos = media_details.get('videos', {}).get('results', [])

    # Find the first YouTube trailer in the results
    for video in videos:
        if video["site"] == "YouTube" and "Trailer" in video["type"]:
            return video["key"]
    return None


# Get the Movie details for the selected title
def get_movie_details(media_details):
    imdb_id = media_details.get("imdb_id")
    title = media_details.get("title")
    year = media_details.get("release_date")[0:4]
    runtime = get_runtime(media_details)
    genre = get_genre(media_details) or None
    director = get_director(media_details) or None
    overview = media_details.get("overview")
    tmdb_rating = round(media_details.get("vote_average"), 1) or None
    imdb_rating = get_imdb_rating(imdb_id)
    rt_url = get_rt_url(title, year, "Movie")
    rt_scores = get_rt_scores(rt_url)
    trailer_id = get_youtube_trailer_id(media_details)

    return (
        imdb_id,
        title,
        year,
        runtime,
        genre,
        director,
        overview,
        tmdb_rating,
        imdb_rating,
        rt_url,
        rt_scores,
        trailer_id,
    )


# Get the TV show details for the selected title
def get_tv_details(media_details):
    imdb_id = media_details.get("external_ids")["imdb_id"]
    title = media_details.get("name")
    year = media_details.get("first_air_date")[0:4]
    genre = get_genre(media_details) or None
    creator = get_creator(media_details) or None
    number_of_seasons = media_details.get("number_of_seasons") or None
    number_of_episodes = media_details.get("number_of_episodes") or None
    overview = media_details.get("overview")
    tmdb_rating = round(media_details.get("vote_average"), 1) or None
    imdb_rating = get_imdb_rating(imdb_id)
    rt_url = get_rt_url(title, year, "TV")
    rt_scores = get_rt_scores(rt_url)
    trailer_id = get_youtube_trailer_id(media_details)

    return (
        imdb_id,
        title,
        year,
        genre,
        creator,
        number_of_seasons,
        number_of_episodes,
        overview,
        tmdb_rating,
        imdb_rating,
        rt_url,
        rt_scores,
        trailer_id,
    )


# Get all the details for the selected title
def get_all_details(tmdb_id, media_type, TMDB_API_KEY):
    media_details = get_media_details(tmdb_id, media_type, TMDB_API_KEY)
    poster_image = get_poster_details(media_details)

    if media_type == "Movie":
        (
            imdb_id,
            title,
            year,
            runtime,
            genre,
            director,
            overview,
            tmdb_rating,
            imdb_rating,
            rt_url,
            rt_scores,
            trailer_id,
        ) = get_movie_details(media_details)
        filtered_details = {
            "tmdb_id": tmdb_id,
            "media_type": media_type,
            "poster_image": poster_image,
            "imdb_id": imdb_id,
            "title": title,
            "year": year,
            "runtime": runtime,
            "genre": genre,
            "director": director,
            "overview": overview,
            "tmdb_rating": tmdb_rating,
            "imdb_rating": imdb_rating,
            "rt_url": rt_url,
            "rt_scores": rt_scores,
            "trailer_id": trailer_id,
        }

    elif media_type == "TV":
        (
            imdb_id,
            title,
            year,
            genre,
            creator,
            number_of_seasons,
            number_of_episodes,
            overview,
            tmdb_rating,
            imdb_rating,
            rt_url,
            rt_scores,
            trailer_id,
        ) = get_tv_details(media_details)
        filtered_details = {
            "tmdb_id": tmdb_id,
            "media_type": media_type,
            "poster_image": poster_image,
            "imdb_id": imdb_id,
            "title": title,
            "year": year,
            "genre": genre,
            "creator": creator,
            "number_of_seasons": number_of_seasons,
            "number_of_episodes": number_of_episodes,
            "overview": overview,
            "tmdb_rating": tmdb_rating,
            "imdb_rating": imdb_rating,
            "rt_url": rt_url,
            "rt_scores": rt_scores,
            "trailer_id": trailer_id,
        }

    return filtered_details
