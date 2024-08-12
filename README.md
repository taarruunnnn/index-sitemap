```
# Sitemap URL Indexing Automation

This Python script automates the process of fetching URLs from sitemaps, submitting them to the Google Indexing API, and keeping track of the processed URLs. It provides a user-friendly interface for entering sitemap links, selecting the Google credentials JSON file, and checking the status of random URLs.

## Features

- Fetches URLs from one or multiple sitemaps
- Submits the URLs to the Google Indexing API for indexing
- Removes duplicate URLs to avoid redundant processing
- Saves the processed URLs and their status in an Excel sheet
- Checks for duplicate URLs and allows the user to choose whether to continue with duplicate URLs or not
- Provides an option to check the status of random URLs
- Displays the number of processed URLs, the file location, the current API quota, and the next available API usage time
- Shows the URLs being processed in the terminal

## Prerequisites

Before running the script, ensure that you have the following:

- Python 3.x installed on your system
- Required libraries: `requests`, `beautifulsoup4`, `pandas`, `google-auth`, `google-auth-oauthlib`, `google-auth-httplib2`, `google-api-python-client`, `openpyxl`, `tkinter`
- Google API credentials JSON file for authentication

## Installation

1. Clone the repository:

   ```
   git clone https://github.com/your-username/sitemap-url-indexing.git
   ```

2. Navigate to the project directory:

   ```
   cd sitemap-url-indexing
   ```

3. Install the required libraries:

   ```
   pip install -r requirements.txt
   ```

   Alternatively, you can install the libraries individually using:

   ```
   pip install requests beautifulsoup4 pandas google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client openpyxl tkinter
   ```

## Usage

1. Run the script:

   ```
   python sitemap_indexing.py
   ```

2. Follow the prompts to select the sitemap input method:
   - Option 1: Enter a single sitemap link
   - Option 2: Enter multiple sitemap links separated by commas

3. If you selected option 2, enter the sitemap links when prompted, separated by commas.

4. A file dialog will open. Navigate to and select your Google credentials JSON file.

5. The script will process the URLs from the sitemap(s), save the results to an Excel sheet, and display the progress and status in the terminal.

6. If duplicate URLs are found, the script will prompt you to choose whether to continue with processing duplicate URLs or not.

7. After processing the URLs, you will have the option to check the status of random URLs by entering them when prompted.

8. Once the processing is complete, a summary will be displayed in the terminal, showing the total URLs processed, successful submissions, failed submissions, the location of the saved Excel file, the current API quota, and the next available API usage time.

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgements

- [Requests](https://docs.python-requests.org/) - HTTP library for making requests to sitemaps and APIs
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) - Library for parsing XML and extracting URLs from sitemaps
- [pandas](https://pandas.pydata.org/) - Data manipulation library for handling and exporting data to Excel
- [Google API Client](https://github.com/googleapis/google-api-python-client) - Google API client library for Python
```
