# FlickPicker - Find the Flicks You Love

## Link to live project: <https://flickpicker.glitch.me/>
[![FlickPicker - Find The Flicks You Love](https://imgtr.ee/images/2023/12/17/4897de9702a251fa66c71de377e66e43.jpeg)](https://flickpicker.glitch.me/)

**Note on Hosting:** The FlickPicker application is currently hosted on Glitch, a platform that offers real-time collaborative editing and instant hosting. Please be aware that the performance and availability of the app may be subject to Glitch's terms of service and usage limits.

## Description
This is a Flask web application that simplifies the process of finding information about movies and TV shows. With just a simple search, you can easily access the most important details of any title, including ratings from TMDB, IMDb, and Rotten Tomatoes, along with a YouTube trailer.

The app was designed to prioritize user-friendliness and efficiency, making sure that only the relevant information is provided to avoid overwhelming the user with data that often leads to time-consuming rabbit holes.

It uses The Movie Database (TMDB) API for searching movies and TV shows and retrieving necessary details about the selected title, and web scraping to get the rating information from IMDb and Rotten Tomatoes.

## Features

- Search for movies and TV shows using the TMDB API.
- Web scraping to get IMDb and Rotten Tomatoes ratings.
- Get detailed information about the selected title such as:
    - Name of Movie/TV show
    - Year
    - Runtime (Movie only)
    - Genre
    - Director (Movie) or Creator (TV show)
    - Total number of seasons (TV show only)
    - Total number of episodes (TV show only)
    - Overview
    - TMDB rating with link to title
    - IMDb rating with link to title
    - Rotten Tomatoes ratings (Tomatometer and Audience Score) with link to title
    - Embedded YouTube trailer
- Clean and user-friendly interface.
- Efficient and fast search results.
- Error handling:
    - User input validation
    - HTTP errors
    - General exceptions

## Video Demo: <https://youtu.be/67DIyT4fnSs>

[![FlickPicker - Find The Flicks You Love](https://imgtr.ee/images/2023/12/17/ee018e25dcb267dadd5d3c609a9e1a7b.jpeg)](https://youtu.be/67DIyT4fnSs)

## Usage
To use this application, you need to run the app.py script. This script takes a title as user input and returns a list of matching results. You can then select a title to get more detailed information.

## Environment Variables
This project uses the following environment variables:

```
# .env file template
# Replace <Your TMDB API key> with your actual TMDB API key without the angle brackets
TMDB_API_KEY=<Your TMDB API key>
```

You need to set these environment variables in a .env file in the project directory.

## Dependencies
This project uses the following Python packages:

- Built-in Python Modules:
    - Flask
    - logging
    - os
    - re

- External Python Modules:
    - **requests:** This package is used to send HTTP requests to the TMDB API and to the IMDb and Rotten Tomatoes websites. It allows the application to communicate with these services and retrieve data.

    - **beautifulsoup4:** This package is used to parse the HTML content returned by the requests to the IMDb and Rotten Tomatoes websites. It allows the application to extract specific pieces of information, such as the IMDb rating, and the Rotten Tomatoes URL and scores.

    - **python-dotenv:** This package is used to load the TMDB_API_KEY environment variable from the .env file in the project directory, which is needed to authenticate the requests to the TMDB API.

    - **unidecode:** This package is used to handle Unicode characters that may be present in the movie and TV show titles. It can convert these characters to their closest ASCII equivalents, which is helpful when dealing with foreign language titles.

    - **quote from urllib.parse:** This function is used to create a percent-encoded string suitable for including in a URL. It's used to sanitize the user input before including it in the URL for the TMDB API request to ensure that the user input doesn't break the URL if it contains special characters.

## Roadmap/Future Enhancements

- Watchlist integration
- 3 Movies/TV show recommendations based on the selected title
- Optimize further for mobile devices

## Acknowledgments

I would like to thank Professor David Malan and the entire CS50 team for making this course one of the best courses out there!

## License

MIT License

Copyright (c) 2023, Ranuk De Silva

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## Third-Party Software Licenses

Below is a list of third-party software used in the FlickPicker project, along with their licenses:

- **Lato Font:**
  Copyright (c) 2010-2014, Łukasz Dziedzic (dziedzic@typoland.com), with Reserved Font Name [Lato](https://www.latofonts.com/).<br>
  Licensed under the [SIL Open Font License, Version 1.1](http://scripts.sil.org/OFL).<br>
  [View on Google fonts](https://fonts.google.com/specimen/Lato)

- **SweetAlert2:**
  The MIT License (MIT)<br>
  Copyright (c) 2014 Tristan Edwards & Limon Monte<br>
  [View on GitHub](https://sweetalert2.github.io/)

## Disclaimer

This app is not used for commercial purposes and is only intended for educational purposes. This website uses TMDB and the TMDB APIs but is not endorsed, certified, or otherwise approved by TMDB. Information about movies and TV shows are obtained from IMDb and Rotten Tomatoes but are not endorsed, certified, or otherwise approved by IMDb or Rotten Tomatoes.




