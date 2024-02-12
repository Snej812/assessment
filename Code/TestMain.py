import unittest
from unittest.mock import patch, MagicMock
from main import fetch_articles, write_to_csv, aggregate_data_to_csv, load_remaining_calls, save_last_fetch_time_and_remaining_calls, wait_for_next_call
from datetime import datetime
import os
import csv
import config

class TestMainFunctions(unittest.TestCase):

    def test_fetch_articles(self):
        # Mock response from the API
        mock_response = {
            'response': {
                'status': 'ok',
                'results': [
                    {'id': '1', 'webPublicationDate': '2024-02-11T08:00:00Z', 'pillarName': 'Politics'},
                    {'id': '2', 'webPublicationDate': '2024-02-10T08:00:00Z', 'pillarName': 'World'},
                    {'id': '3', 'webPublicationDate': '2024-02-09T08:00:00Z', 'pillarName': 'Opinion'}
                ]
            }
        }

        with patch('requests.get') as mock_get:
            mock_get.return_value.json.return_value = mock_response
            articles = fetch_articles(1)

        self.assertEqual(len(articles), 3)
        self.assertEqual(articles[0]['id'], '1')
        self.assertEqual(articles[1]['id'], '2')
        self.assertEqual(articles[2]['id'], '3')

    def test_write_to_csv(self):
        # Mock articles data
        articles = [
            {'id': '1', 'webPublicationDate': '2024-02-11T08:00:00Z', 'pillarName': 'Politics'},
            {'id': '2', 'webPublicationDate': '2024-02-10T08:00:00Z', 'pillarName': 'World'},
            {'id': '3', 'webPublicationDate': '2024-02-09T08:00:00Z', 'pillarName': 'Opinion'}
        ]

        temp_csv_file = 'test/temp_articles.csv'

        # Clear the temporary CSV file
        with open(temp_csv_file, 'w'):
            pass

        # Write articles to a temporary CSV file
        write_to_csv(articles,temp_csv_file)

        # Read the temporary CSV file
        with open(temp_csv_file, 'r') as file:
            reader = csv.DictReader(file)
            written_articles = list(reader)

        self.assertEqual(len(written_articles), 3)
        self.assertEqual(written_articles[0]['id'], '1')
        self.assertEqual(written_articles[1]['id'], '2')
        self.assertEqual(written_articles[2]['id'], '3')

    def test_aggregate_data_to_csv(self):
        # Mock article dates and pillars
        article_dates_and_pillars = [
            (datetime(2024, 2, 11), 'Politics'),
            (datetime(2024, 2, 10), 'World'),
            (datetime(2024, 2, 9), 'Opinion')
        ]

        temp_csv_file = 'test/temp_aggregated_data.csv'

        # Clear the temporary CSV file
        with open(temp_csv_file, 'w'):
            pass

        # Aggregate data to a temporary CSV file
        aggregate_data_to_csv(article_dates_and_pillars,temp_csv_file)

        # Read the temporary CSV file
        with open(temp_csv_file, 'r') as file:
            reader = csv.DictReader(file)
            aggregated_data = list(reader)

        self.assertEqual(len(aggregated_data), 3)
        self.assertEqual(aggregated_data[0]['Month'], '2024-02')
        self.assertEqual(aggregated_data[1]['Month'], '2024-02')
        self.assertEqual(aggregated_data[2]['Month'], '2024-02')

    def test_load_remaining_calls(self):
        # Mock state file
        with open(config.STATE_FILE, 'w') as file:
            file.write(f"{datetime.now()}\n")
            file.write("100\n")

        remaining_calls = load_remaining_calls()

        self.assertEqual(remaining_calls, 100)

        # Clear the state file
        with open(config.STATE_FILE, 'w'):
            pass

    def test_save_last_fetch_time_and_remaining_calls(self):
        # Mock remaining calls
        remaining_calls = 50

        # Save last fetch time and remaining calls
        save_last_fetch_time_and_remaining_calls(remaining_calls)

        # Read the state file
        with open(config.STATE_FILE, 'r') as file:
            lines = file.readlines()
            last_fetch_time = lines[0].strip()
            saved_remaining_calls = int(lines[1].strip())

        # Clear the state file
        with open(config.STATE_FILE, 'w'):
            pass

        self.assertIsInstance(last_fetch_time, str)
        self.assertEqual(saved_remaining_calls, 50)

    def test_wait_for_next_call(self):
        # Mock the time.sleep function
        start_time = datetime.now()
        wait_for_next_call()
        end_time = datetime.now()
        execution_time = (end_time - start_time).total_seconds()
        self.assertGreaterEqual(execution_time, 1)

if __name__ == '__main__':
    unittest.main()