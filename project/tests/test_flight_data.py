import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
import pandas as pd
from backend.flight_data import FlightDataProcessor
from unittest.mock import patch

# Sample data for testing
SAMPLE_BOOKINGS_DATA = {
    'airlie_id': [1, 2, 1, 4, 2],
    'departure_dt': ['2025-05-25', '2025-05-26', '2025-05-25', '2025-05-27', '2025-05-26'],
    'arrival_dt': ['2025-05-25', '2025-05-26', '2025-05-25', '2025-05-27', '2025-05-26'],
    'class': ['economy', 'business', 'economy', 'first', 'business'],
    'fare': [100, 200, 120, 300, 250],
    'extras': ['wifi', 'meal', 'none', 'wifi,meal', 'none'],
    'status': ['confirmed', 'confirmed', 'cancelled', 'confirmed', 'pending'],
    'gate': ['A1', 'B2', 'A1', 'C3', 'B2'],
    'terminal': ['1', '2', '1', '3', '2'],
    'layovers': [0, 1, 0, 2, 1],
    'layover_locations': [None, 'JFK', None, 'LAX,ORD', 'DFW'],
    'aircraft_type': ['737', 'A320', '737', '777', 'A330'],
    'reward_program_member': [True, False, True, False, True],
    'duration_hrs': [2.5, 4.0, 2.7, 5.2, 3.8]
}
SAMPLE_FAILURES_DATA = {
    'Date/Time Opened': ['2025-05-20 10:00:00', '2025-05-19 12:00:00'],
    'Account Name': ['Alpha Corp', 'Beta Inc'],
    'Category': ['System Error', 'Network Issue'],
    'Subcategory': ['Database', 'Connectivity'],
    'Subject': ['Login Failure', 'Intermittent Outage'],
    'Case Number': ['CASE001', 'CASE002']
}

@pytest.fixture
def flight_data_processor():
    processor = FlightDataProcessor()
    # Simulate loading and preprocessing for bookings
    processor.bookings_df = pd.DataFrame(SAMPLE_BOOKINGS_DATA)
    processor.bookings_df.rename(columns=FlightDataProcessor.COLUMN_MAPPINGS, inplace=True)
    processor.bookings_df['airline_name'] = processor.bookings_df['airline_id'].map(FlightDataProcessor.AIRLINE_ID_TO_NAME).fillna('Unknown')
    processor._preprocess_data()
    # Simulate loading for failures
    processor.failure_df = pd.DataFrame(SAMPLE_FAILURES_DATA)
    processor.failure_df.rename(columns={'Date/Time Opened': 'opened_at',
                                            'Account Name': 'account_name',
                                            'Category': 'failure_category',
                                            'Subcategory': 'failure_subcategory',
                                            'Subject': 'failure_subject',
                                            'Case Number': 'case_number'}, inplace=True)
    if 'opened_at' in processor.failure_df.columns:
        processor.failure_df['opened_at'] = pd.to_datetime(processor.failure_df['opened_at'])
    return processor

def test_get_airline_flight_counts(flight_data_processor):
    counts = flight_data_processor.get_airline_flight_counts()
    assert isinstance(counts, dict)
    assert 'American Airlines' in counts
    assert counts['American Airlines'] == 2

def test_get_top_departure_dates(flight_data_processor):
    top_dates = flight_data_processor.get_top_departure_dates(limit=2)
    assert isinstance(top_dates, pd.Series)
    assert len(top_dates) == 2
    assert pd.to_datetime('2025-05-25').date() in top_dates.index

def test_get_flight_class_distribution(flight_data_processor):
    distribution = flight_data_processor.get_flight_class_distribution()
    assert isinstance(distribution, pd.Series)
    assert 'economy' in distribution.index
    assert distribution['economy'] == 2

def test_get_average_fare_per_airline(flight_data_processor):
    avg_fares = flight_data_processor.get_average_fare_per_airline()
    assert isinstance(avg_fares, pd.Series)
    assert 1 in avg_fares.index
    # Expected average for airline ID 1 (American Airlines): (100 + 120) / 2 = 110.0
    assert avg_fares[1] == 110.0

def test_get_failure_counts_by_category(flight_data_processor):
    counts = flight_data_processor.get_failure_counts_by_category()
    assert isinstance(counts, dict)
    assert 'System Error' in counts
    assert counts['System Error'] == 1