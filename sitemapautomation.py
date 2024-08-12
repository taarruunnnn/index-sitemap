import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urlparse
import time
from datetime import datetime
from google.oauth2 import service_account
from googleapiclient.discovery import build
import os
import tkinter as tk
from tkinter import filedialog
from datetime import timedelta

def fetch_sitemap_urls(sitemap_url):
    response = requests.get(sitemap_url)
    soup = BeautifulSoup(response.text, 'xml')
    urls = [loc.text for loc in soup.find_all('loc')]
    return urls

def submit_to_indexing_api(url, credentials):
    try:
        indexing_service = build('indexing', 'v3', credentials=credentials)
        request = indexing_service.urlNotifications().publish(
            body={'url': url, 'type': 'URL_UPDATED'}
        )
        response = request.execute()
        return 'Success'
    except Exception as e:
        return f'Failed: {str(e)}'

def remove_duplicates(urls):
    df = pd.DataFrame(urls, columns=['url'])
    df['domain'] = df['url'].apply(lambda x: urlparse(x).netloc)
    df.drop_duplicates(subset='url', inplace=True)
    return df['url'].tolist()

def load_processed_urls():
    try:
        df = pd.read_excel('processed_urls.xlsx')
        return set(df['url'].tolist())
    except FileNotFoundError:
        return set()

def save_processed_urls(urls, statuses):
    df = pd.DataFrame({'url': urls, 'status': statuses})
    df.to_excel('processed_urls.xlsx', index=False)

def get_sitemap_links():
    sitemap_links = []
    while True:
        print('Enter sitemap links (comma-separated) or press Enter to finish:')
        sitemap_input = input().strip()
        if sitemap_input == '':
            break
        sitemap_links.extend(sitemap_input.split(','))
    return [link.strip() for link in sitemap_links]

def get_credentials_file():
    root = tk.Tk()
    root.withdraw()
    credentials_file = filedialog.askopenfilename(title='Select Google Credentials JSON File',
                                                  filetypes=[('JSON Files', '*.json')])
    return credentials_file

def get_url_status(url, credentials):
    return submit_to_indexing_api(url, credentials)

def main():
    print('Select sitemap input method:')
    print('1. Enter a single sitemap link')
    print('2. Enter multiple sitemap links')
    choice = input('Enter your choice (1 or 2): ')

    if choice == '1':
        sitemap_url = input('Enter the sitemap link: ')
        sitemap_urls = [sitemap_url]
    elif choice == '2':
        sitemap_urls = get_sitemap_links()
    else:
        print('Invalid choice. Exiting.')
        return

    credentials_file = get_credentials_file()
    if not credentials_file:
        print('No credentials file selected. Exiting.')
        return

    credentials = service_account.Credentials.from_service_account_file(credentials_file)

    all_urls = []
    for sitemap_url in sitemap_urls:
        urls = fetch_sitemap_urls(sitemap_url)
        all_urls.extend(urls)

    processed_urls = load_processed_urls()
    unique_urls = remove_duplicates(all_urls)
    new_urls = [url for url in unique_urls if url not in processed_urls]
    duplicate_urls = [url for url in unique_urls if url in processed_urls]

    if duplicate_urls:
        print(f'Found {len(duplicate_urls)} duplicate URLs:')
        for url in duplicate_urls:
            print(url)
        proceed = input('Do you want to proceed with processing duplicate URLs? (y/n): ')
        if proceed.lower() != 'y':
            new_urls = [url for url in new_urls if url not in duplicate_urls]

    total_urls = len(new_urls)
    print(f'Number of new URLs to be processed: {total_urls}')

    submitted_urls = []
    submitted_statuses = []
    start_time = time.time()

    for i, url in enumerate(new_urls, start=1):
        print(f'Processing URL ({i}/{total_urls}): {url}')
        status = get_url_status(url, credentials)
        submitted_urls.append(url)
        submitted_statuses.append(status)
        print(f'URL: {url}, Status: {status}')
        time.sleep(1)  # Delay to avoid overloading the API

    save_processed_urls(submitted_urls, submitted_statuses)

    end_time = time.time()
    processing_time = end_time - start_time

    print(f'\nProcessed URLs saved to: processed_urls.xlsx')
    print(f'Total processing time: {processing_time:.2f} seconds')

    while True:
        check_url = input('\nEnter a URL to check its status (or press Enter to skip): ')
        if check_url == '':
            break
        status = get_url_status(check_url, credentials)
        print(f'URL: {check_url}, Status: {status}')

    print('\nSummary:')
    print(f'Total URLs processed: {total_urls}')
    print(f'Successful submissions: {submitted_statuses.count("Success")}')
    print(f'Failed submissions: {submitted_statuses.count("Failed")}')

    # Get API quota information (replace with actual API quota retrieval code)
    remaining_quota = 1000
    reset_time = datetime.now() + timedelta(hours=24)

    print(f'\nAPI Quota:')
    print(f'Remaining quota: {remaining_quota}')
    print(f'Quota reset time: {reset_time}')

if __name__ == '__main__':
    main()