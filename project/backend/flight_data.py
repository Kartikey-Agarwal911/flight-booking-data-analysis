import json
import pandas as pd
from datetime import datetime, timedelta
import random
import numpy as np
from typing import Dict, List, Union, Optional

class FlightDataProcessor:
    AIRLINE_ID_TO_NAME = {
        1: 'American Airlines',
        2: 'Delta Air Lines',
        3: 'United Airlines',
        4: 'Southwest Airlines',
        5: 'JetBlue Airways',
        6: 'Alaska Airlines',
        7: 'Spirit Airlines',
        8: 'Frontier Airlines',
        9: 'Hawaiian Airlines',
        10: 'Allegiant Air',
        11: 'Sun Country Airlines',
        12: 'Silver Airways',
        13: 'Cape Air',
        14: 'Boutique Air',
        15: 'Southern Airways Express',
        16: 'Advanced Air',
        17: 'Key Lime Air',
        18: 'Contour Airlines',
        19: 'Other'
    }
    COLUMN_MAPPINGS = {
        'airlie_id': 'airline_id',
        'flght#': 'flight_number',
        'departure_dt': 'departure_dt',
        'arrival_dt': 'arrival_dt',
        'dep_time': 'departure_time',      # Add mapping for departure time if needed
        'arrivl_time': 'arrival_time',        # Add mapping for arrival time if needed
        'booking_cd': 'booking_code',
        'passngr_nm': 'passenger_name',
        'seat_no': 'seat_number',
        'class': 'flight_class',
        'fare': 'fare',
        'extras': 'extras',
        'loyalty_pts': 'loyalty_points',
        'status': 'status',
        'gate': 'gate',
        'terminal': 'terminal',
        'baggage_claim': 'baggage_claim',
        'duration_hrs': 'duration_hours',
        'layovers': 'layovers',
        'layover_locations': 'layover_locations',
        'aircraft_type': 'aircraft_type',
        'pilot': 'pilot',
        'cabin_crew': 'cabin_crew',
        'inflight_ent': 'inflight_entertainment',
        'meal_option': 'meal_option',
        'wifi': 'wifi_available',
        'window_seat': 'has_window_seat',
        'aisle_seat': 'has_aisle_seat',
        'emergency_exit_row': 'is_emergency_exit',
        'number_of_stops': 'number_of_stops',
        'reward_program_member': 'is_reward_member'
        # Add all other column mappings here based on your CSV file
    }

    def __init__(self):
        self.bookings_df = None
        self.failure_df = None
        self.initialized = False
        self.AIRLINE_ID_TO_NAME = FlightDataProcessor.AIRLINE_ID_TO_NAME # Make it accessible as an instance attribute

    def load_data(self, bookings_path: str, failures_path: str):
        """Load flight booking and failure data."""
        try:
            self._load_bookings(bookings_path)
            self._load_failures(failures_path)
            self._preprocess_data()
            self.initialized = True
            print("Flight and failure data loaded.")
        except Exception as e:
            print(f"Error loading data: {e}")
            raise

    def _load_bookings(self, bookings_path: str):
        """Load flight booking data from CSV."""
        try:
            self.bookings_df = pd.read_csv(bookings_path)
            self.bookings_df.rename(columns=COLUMN_MAPPINGS, inplace=True)  # Apply mappings here
            # Convert date columns to datetime
            self.bookings_df['departure_dt'] = pd.to_datetime(self.bookings_df['departure_dt'])
            self.bookings_df['arrival_dt'] = pd.to_datetime(self.bookings_df['arrival_dt'])

            self.bookings_df['airline_name'] = self.bookings_df['airline_id'].map(self.AIRLINE_ID_TO_NAME).fillna('Unknown')

            print(f"Loaded {len(self.bookings_df)} flight bookings")
        except Exception as e:
            print(f"Error loading booking data: {e}")
            self.bookings_df = None
            raise

    def _load_failures(self, failures_path: str):
        """Load flight failure data from CSV."""
        try:
            # Read the CSV, skipping header rows and handling potential issues
            self.failure_df = pd.read_csv(failures_path, skiprows=6)
            self.failure_df.rename(columns={'Date/Time Opened': 'opened_at',
                                            'Account Name': 'account_name',
                                            'Category': 'failure_category',
                                            'Subcategory': 'failure_subcategory',
                                            'Subject': 'failure_subject',
                                            'Case Number': 'case_number'}, inplace=True)
            if 'opened_at' in self.failure_df.columns:
                self.failure_df['opened_at'] = pd.to_datetime(self.failure_df['opened_at'])
            print(f"Loaded {len(self.failure_df)} failure reports.")
        except Exception as e:
            print(f"Error loading failure data: {e}")
            self.failure_df = None

    def _preprocess_data(self) -> None:
        """Clean and preprocess the loaded data."""
        if self.bookings_df is not None:
            date_columns = ['departure_dt', 'arrival_dt']
            for col in date_columns:
                if col in self.bookings_df.columns:
                    self.bookings_df[col] = pd.to_datetime(self.bookings_df[col])
            if 'delay_minutes' not in self.bookings_df.columns:
                self.bookings_df['delay_minutes'] = 0
            if 'fare' in self.bookings_df.columns:
                self.bookings_df['fare'] = self.bookings_df['fare'].fillna(self.bookings_df['fare'].median())

    # --- Booking Data Analysis Methods ---
    def get_airline_flight_counts(self) -> Dict[str, int]:
        if self.bookings_df is not None:
            return self.bookings_df['airline_name'].value_counts().to_dict()
        return {}

    def get_top_departure_dates(self, limit: int = 5) -> pd.Series:
        if self.bookings_df is not None:
            return self.bookings_df['departure_dt'].dt.date.value_counts().nlargest(limit)
        return pd.Series()

    def get_top_arrival_dates(self, limit: int = 5) -> pd.Series:
        if self.bookings_df is not None:
            return self.bookings_df['arrival_dt'].dt.date.value_counts().nlargest(limit)
        return pd.Series()

    def get_flight_class_distribution(self) -> pd.Series:
        if self.bookings_df is not None and 'flight_class' in self.bookings_df.columns:
            return self.bookings_df['flight_class'].value_counts()
        return pd.Series()

    def get_fare_statistics(self) -> Optional[pd.Series]:
        if self.bookings_df is not None and 'fare' in self.bookings_df.columns:
            return self.bookings_df['fare'].describe()
        return None

    def get_common_extras(self, limit: int = 5) -> pd.Series:
        if self.bookings_df is not None and 'extras' in self.bookings_df.columns:
            return self.bookings_df['extras'].value_counts().nlargest(limit)
        return pd.Series()

    def get_booking_status_counts(self) -> pd.Series:
        if self.bookings_df is not None and 'status' in self.bookings_df.columns:
            return self.bookings_df['status'].value_counts()
        return pd.Series()

    def get_frequent_gates(self, limit: int = 5) -> pd.Series:
        if self.bookings_df is not None and 'gate' in self.bookings_df.columns:
            return self.bookings_df['gate'].value_counts().nlargest(limit)
        return pd.Series()

    def get_frequent_terminals(self, limit: int = 5) -> pd.Series:
        if self.bookings_df is not None and 'terminal' in self.bookings_df.columns:
            return self.bookings_df['terminal'].value_counts().nlargest(limit)
        return pd.Series()

    def get_layover_counts(self) -> pd.Series:
        if self.bookings_df is not None and 'layovers' in self.bookings_df.columns:
            return self.bookings_df['layovers'].value_counts()
        return pd.Series()

    def get_frequent_layover_locations(self, limit: int = 5) -> pd.Series:
        if self.bookings_df is not None and 'layover_locations' in self.bookings_df.columns:
            return self.bookings_df['layover_locations'].fillna('None').value_counts().nlargest(limit)
        return pd.Series()

    def get_aircraft_type_counts(self, limit: int = 5) -> pd.Series:
        if self.bookings_df is not None and 'aircraft_type' in self.bookings_df.columns:
            return self.bookings_df['aircraft_type'].value_counts().nlargest(limit)
        return pd.Series()

    def get_reward_program_distribution(self) -> pd.Series:
        if self.bookings_df is not None and 'is_reward_member' in self.bookings_df.columns:
            return self.bookings_df['is_reward_member'].value_counts()
        return pd.Series()

    def get_average_fare_per_airline(self) -> pd.Series:
        if self.bookings_df is not None and 'fare' in self.bookings_df.columns and 'airline_id' in self.bookings_df.columns:
            return self.bookings_df.groupby('airline_id')['fare'].mean().round(2)
        return pd.Series()

    def get_average_duration_per_airline(self) -> pd.Series:
        if self.bookings_df is not None and 'duration_hrs' in self.bookings_df.columns and 'airline_id' in self.bookings_df.columns:
            return self.bookings_df.groupby('airline_id')['duration_hrs'].mean().round(2)
        return pd.Series()

    def get_aisle_seat_distribution(self) -> pd.Series:
        if self.bookings_df is not None and 'has_aisle_seat' in self.bookings_df.columns:
            return self.bookings_df['has_aisle_seat'].value_counts()
        return pd.Series()

    # --- Failure Data Analysis Methods ---
    def get_failure_counts_by_category(self) -> Optional[Dict[str, int]]:
        if self.failure_df is not None and 'failure_category' in self.failure_df.columns:
            return self.failure_df['failure_category'].value_counts().to_dict()
        return None

    def get_failure_trends_over_time(self) -> Optional[List[Dict[str, int]]]:
        if self.failure_df is not None and 'opened_at' in self.failure_df.columns:
            thirty_days_ago = datetime.now() - timedelta(days=30)
            recent_failures = self.failure_df[self.failure_df['opened_at'] >= thirty_days_ago]
            daily_counts = recent_failures.groupby(recent_failures['opened_at'].dt.date).size().to_dict()
            return [{'date': str(date), 'count': count} for date, count in daily_counts.items()]
        return None

    def get_failures_by_account(self) -> Optional[Dict[str, int]]:
        if self.failure_df is not None and 'account_name' in self.failure_df.columns:
            return self.failure_df['account_name'].value_counts().to_dict()
        return None

    def get_recent_failures(self, limit: int = 5) -> Optional[List[Dict[str, any]]]:
        if self.failure_df is not None:
            recent = self.failure_df.sort_values(by='opened_at', ascending=False).head(limit)
            return recent[['case_number', 'opened_at', 'failure_category', 'failure_subcategory', 'failure_subject', 'account_name']].to_dict('records')
        return None

# Create an instance of the processor
flight_data = FlightDataProcessor()

# File Explanation:
"""
This file implements the FlightDataProcessor class which handles all flight booking data operations.
Key features:
1. Data loading and preprocessing from the real CSV file
2. Uses a hardcoded mapping for airline names
3. Methods for various data analysis tasks based on the available columns:
    - Counts of airlines
    - Top departure and arrival dates (Bar Chart)
    - Distribution of flight classes (Pie Chart)
    - Descriptive statistics of fare (Text)
    - Most common extras (Bar Chart)
    - Counts of booking statuses (Bar Chart)
    - Most frequent gates and terminals (Bar Chart)
    - Counts of layovers (Bar Chart)
    - Most frequent layover locations (Bar Chart)
    - Counts of aircraft types (Bar Chart)
    - Distribution of reward program members (Pie Chart)
    - Average fare per airline (Bar Chart)
    - Average duration per airline (Bar Chart)
    - Distribution of aisle seat preferences (Pie Chart)
The class ensures data is properly loaded and preprocessed before any analysis is performed.
"""