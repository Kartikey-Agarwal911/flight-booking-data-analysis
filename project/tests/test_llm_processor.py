import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
import pandas as pd  # Import pandas
from backend.llm_processor import QueryProcessor
from backend.flight_data import FlightDataProcessor
from unittest.mock import MagicMock

def test_process_airline_flights_query():
    mock_flight_data = MagicMock(spec=FlightDataProcessor)
    mock_flight_data.get_airline_flight_counts.return_value = {'American Airlines': 2, 'Delta Air Lines': 2, 'Southwest Airlines': 1}
    processor = QueryProcessor(mock_flight_data)
    result = processor.process_query("Which airline has the most flights?")
    assert result['type'] == 'text'
    assert "American Airlines" in result['data'] or "Delta Air Lines" in result['data'] # Handle ties

def test_process_top_departure_dates_query():
    mock_flight_data = MagicMock(spec=FlightDataProcessor)
    mock_flight_data.get_top_departure_dates.return_value = pd.Series({pd.to_datetime('2025-05-25').date(): 2, pd.to_datetime('2025-05-26').date(): 1})
    processor = QueryProcessor(mock_flight_data)
    result = processor.process_query("What are the top 2 most frequent departure dates?")
    assert result['type'] == 'bar_chart'
    assert len(result['data']['labels']) == 2
    assert result['data']['title'].startswith("Top 2 Departure Dates")

def test_process_unrecognized_query():
    mock_flight_data = MagicMock(spec=FlightDataProcessor)
    processor = QueryProcessor(mock_flight_data)
    result = processor.process_query("Tell me something random.")
    assert result['type'] == 'text'
    assert "Sorry, I don't understand" in result['data']