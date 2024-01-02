from flask import Flask, render_template, request
from search import search_title, get_all_details, format_title
from requests.exceptions import HTTPError
from dotenv import load_dotenv
import os
import logging


# Load environment variables once
load_dotenv()

# Get the TMDB_API_KEY once
TMDB_API_KEY = os.getenv("TMDB_API_KEY")

# Configure logging
logging.basicConfig(
    filename="app.log",
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s",
)


app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    try:
        if request.method == "POST":
            user_input = request.form.get("user_input")
            # If there is no user input, display Sweet Alert error message
            if not user_input:
                return render_template(
                    "index.html", error="Please enter a search term."
                )
            results = search_title(user_input)
            # If there are no results, display error message on page
            if results is None:
                return render_template(
                    "index.html",
                    error="No results were found for your search. Try again.",
                )
            # If there are matches, display results
            return render_template(
                "results.html", body_class="index-body-2", results=results
            )
        return render_template("index.html")

    except HTTPError as http_error:
        app.logger.error(
            f"HTTP error occurred: {http_error.response.status_code} {http_error.response.reason}"
        )
        return render_template(
            "error.html",
            message=f"HTTP error occurred: {http_error.response.status_code} {http_error.response.reason}",
        )
    except Exception as error:
        app.logger.error(str(error))
        return render_template("error.html", message=str(error))


@app.route("/details/<tmdb_id>/<media_type>")
def details(tmdb_id, media_type):
    try:
        # Get all details based on TMDB ID and media type using TMDB API
        details = get_all_details(tmdb_id, media_type, TMDB_API_KEY)
    except Exception as error:
        app.logger.error(f"Error getting details: {error}")
        return render_template(
            "error.html", message="Error getting details. Try again."
        )

    # Render the details page if all information is fetched
    return render_template("details.html", details=details)


# Custom filter to sanitize title
app.jinja_env.filters["format_title"] = format_title

if __name__ == "__main__":
    app.run(debug=True)
