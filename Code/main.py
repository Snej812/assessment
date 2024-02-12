import requests
import csv
from datetime import datetime
import os
import time
import config
import logging

# Configure logging
logging.basicConfig(filename='fetch_articles.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def fetch_articles(page_number):
    """
    Fetch articles from the API.

    Args:
        page_number (int): The page number of articles to fetch.

    Returns:
        list: List of articles fetched from the API.
    """
    params = {
        'api-key': config.API_KEY,
        'q': 'elections OR Brexit',
        'order-by': 'newest',  # Start reading from the least timestamp
        'show-fields': ','.join(config.FIELDNAMES),  # Specify the fields to retrieve
        'page-size': config.PAGE_SIZE,
        'page': page_number
    }
    try:
        response = requests.get(config.API_URL, params=params)
        response_data = response.json().get('response', {})
        return response_data.get('results', [])
    except Exception as e:
        logging.warning(e)
        return None

def write_to_csv(articles,path):
    """
    Write articles to a CSV file.

    Args:
        articles (list): List of articles to write to the CSV file.
    """
    with open(path, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=config.FIELDNAMES, extrasaction='ignore')
        if os.stat(path).st_size == 0:
            writer.writeheader()  # Write header only if the file is empty
        writer.writerows(articles)

def aggregate_data_to_csv(article_dates_and_pillars,path):
    """
    Aggregate article data and write to a CSV file.

    Args:
        article_dates_and_pillars (list): List of tuples containing article dates and pillar names.
    """
    monthly_aggregates = {}
    for article_date, pillar in article_dates_and_pillars:
        month_year = article_date.strftime('%Y-%m')
        if month_year not in monthly_aggregates:
            monthly_aggregates[month_year] = {}
        if pillar not in monthly_aggregates[month_year]:
            monthly_aggregates[month_year][pillar] = 0
        monthly_aggregates[month_year][pillar] += 1

    with open(path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Month', 'pillarName', 'ArticleCount']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, extrasaction='ignore')
        writer.writeheader()  # Write header
        for month_year, pillar_counts in monthly_aggregates.items():
            for pillar, count in pillar_counts.items():
                writer.writerow({'Month': month_year, 'pillarName': pillar, 'ArticleCount': count})

def load_remaining_calls():
    """
    Load the remaining API calls from the state file.
    If the state file doesn't exist, return the default number of calls per day.

    Returns:
        int: The remaining API calls.
    """
    if not os.path.exists(config.STATE_FILE):
        return config.CALLS_PER_DAY
    with open(config.STATE_FILE, 'r') as file:
        last_fetch_time = file.readline().strip()
        if last_fetch_time:
            remaining_calls = int(file.readline().strip())
            last_fetch_time = datetime.strptime(last_fetch_time, '%Y-%m-%d %H:%M:%S.%f')
            if last_fetch_time.date() < datetime.now().date():
                remaining_calls = config.CALLS_PER_DAY
            return remaining_calls
    return config.CALLS_PER_DAY

def save_last_fetch_time_and_remaining_calls(remaining_calls):
    """
    Save the current time and remaining API calls to the state file.

    Args:
        remaining_calls (int): The remaining API calls.
    """
    with open(config.STATE_FILE, 'w') as file:
        file.write(f"{datetime.now()}\n")  # Save current time
        file.write(f"{remaining_calls}\n")  # Save remaining calls

def wait_for_next_call():
    """
    Wait for the next API call to avoid exceeding the rate limit.
    """
    time.sleep(1)

if __name__ == "__main__":
    article_dates_and_pillars = []
    page_number = 1

    while True:
        remaining_calls = load_remaining_calls()  # Load remaining API calls from the state file

        if remaining_calls <= 0:
            logging.info("Daily API limit reached. Please try again tomorrow.")
            print("Daily API limit reached. Please try again tomorrow.")
            break
        
        articles = fetch_articles(page_number)
        
        if not articles:
            logging.info("No new articles")
            print("No new articles")
            break
        
        logging.info("Generating Article CSV file")
        for article in articles:
            article_date = datetime.strptime(article['webPublicationDate'], '%Y-%m-%dT%H:%M:%SZ')
            pillar_name = article.get('pillarName', 'Unknown')  # Default to 'Unknown' if 'pillarName' is missing
            article_dates_and_pillars.append((article_date, pillar_name))

        # Save the articles into CSV file
        write_to_csv(articles,config.CSV_FILE)
        page_number += 1
        remaining_calls -= 1

        # Save remaining API calls to the state file
        save_last_fetch_time_and_remaining_calls(remaining_calls)

        # Wait for 1 Second
        wait_for_next_call()
    
    # Generate aggregated CSV file and Saving into CSV file
    logging.info("Generating aggregated CSV file")
    aggregate_data_to_csv(article_dates_and_pillars,config.AGGREGATED_CSV_FILE)

    logging.info("Script execution completed.")
