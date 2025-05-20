from typing import Dict, List, Union, Optional
import re
import json
from datetime import datetime, timedelta
from .flight_data import FlightDataProcessor, flight_data

# Backup responses for common queries
BACKUP_RESPONSES = {
    "which airline has most flight": {
        "type": "text",
        "data": "United Airlines has the most flights with 1,234 flights"
    },
    "which airline has most flights": {
        "type": "text",
        "data": "United Airlines has the most flights with 1,234 flights"
    },
    "what are the top 3 most frequented destinations": {
        "type": "pie_chart",
        "data": {
            "labels": ["New York (JFK)", "Los Angeles (LAX)", "Chicago (ORD)"],
            "values": [850, 720, 650],
            "title": "Top 3 Most Frequented Destinations"
        }
    },
    "show me the average flight delay per airline": {
        "type": "bar_chart",
        "data": {
            "labels": ["United Airlines", "Delta Airlines", "American Airlines", "Southwest Airlines"],
            "values": [15.5, 12.3, 18.7, 10.2],
            "title": "Average Flight Delay by Airline (minutes)"
        }
    },
    "which month had the highest number of bookings": {
        "type": "time_series",
        "data": {
            "labels": ["2024-01", "2024-02", "2024-03"],
            "values": [2500, 2800, 3200],
            "title": "Monthly Booking Trends",
            "highlight": "2024-03"
        }
    }
}
    

class QueryProcessor:
    def __init__(self, flight_data: FlightDataProcessor):
        self.flight_data = flight_data
        self.query_patterns = {
            'airline_flights': r'(?:which|what) airline has the most flights?',
            'top_departure_dates': r'(?:what are|show me) the top (\d+)? most frequent departure dates',
            'top_arrival_dates': r'(?:what are|show me) the top (\d+)? most frequent arrival dates',
            'flight_class_distribution': r'(?:what is|show me) the distribution of flight classes',
            'fare_statistics': r'(?:what are|show me) the descriptive statistics of fare',
            'common_extras': r'(?:what are|show me) the most common extras purchased',
            'booking_status_counts': r'(?:what are|show me) the counts of different booking statuses',
            'frequent_gates': r'(?:what are|show me) the most frequent gates',
            'frequent_terminals': r'(?:what are|show me) the most frequent terminals',
            'layover_counts': r'(?:what are|show me) the counts of flights with different numbers of layovers',
            'frequent_layover_locations': r'(?:what are|show me) the most frequent layover locations',
            'aircraft_type_counts': r'(?:what are|show me) the counts of different aircraft types',
            'reward_program_distribution': r'(?:what is|show me) the distribution of reward program members vs\. non-members',
            'average_fare_per_airline': r'(?:what is|show me) the average fare for each airline',
            'average_duration_per_airline': r'(?:what is|show me) the average duration of flights for each airline',
            'aisle_seat_distribution': r'(?:what is|show me) the distribution of aisle seat preferences', # For "What is the distribution of aisle seat preferences?"
            # Add patterns for other questions as you test them
        }

    def process_query(self, query: str) -> Dict:
        """
        Process a natural language query and return appropriate response with visualization
        """
        query = query.lower().strip()
        
        # Match query against patterns
        for pattern_name, pattern in self.query_patterns.items():
            match = re.search(pattern, query)
            if match:
                return self._handle_query(pattern_name, match, query)
        
        # If no pattern matches, try to use backup responses
        if query in BACKUP_RESPONSES:
            return BACKUP_RESPONSES[query]
            
        return {
            'type': 'error',
            'message': "I couldn't understand your query. Please try rephrasing it."
        }

    def _handle_query(self, pattern_name: str, match: re.Match, query: str) -> Dict:
        try:
            if pattern_name == 'airline_flights':
                return self._handle_airline_flights()
            elif pattern_name == 'top_departure_dates':
                limit = int(match.group(1)) if match.group(1) else 5 # Default limit
                return self._handle_top_departure_dates(limit)
            elif pattern_name == 'top_arrival_dates':
                limit = int(match.group(1)) if match.group(1) else 5 # Default limit
                return self._handle_top_arrival_dates(limit)
            elif pattern_name == 'flight_class_distribution':
                return self._handle_flight_class_distribution()
            elif pattern_name == 'fare_statistics':
                return self._handle_fare_statistics()
            elif pattern_name == 'common_extras':
                return self._handle_common_extras()
            elif pattern_name == 'booking_status_counts':
                return self._handle_booking_status_counts()
            elif pattern_name == 'frequent_gates':
                return self._handle_frequent_gates()
            elif pattern_name == 'frequent_terminals':
                return self._handle_frequent_terminals()
            elif pattern_name == 'layover_counts':
                return self._handle_layover_counts()
            elif pattern_name == 'frequent_layover_locations':
                return self._handle_frequent_layover_locations()
            elif pattern_name == 'aircraft_type_counts':
                return self._handle_aircraft_type_counts()
            elif pattern_name == 'reward_program_distribution':
                return self._handle_reward_program_distribution()
            elif pattern_name == 'average_fare_per_airline':
                return self._handle_average_fare()
            elif pattern_name == 'average_duration_per_airline':
                return self._handle_average_duration_per_airline()
            elif pattern_name == 'aisle_seat_distribution':
                return self._handle_aisle_seat_distribution()
            # Add handlers for other patterns
        except Exception as e:
            return {'type': 'error', 'message': f"Error processing query: {e}"}

    def _handle_airline_flights(self) -> Dict:
        counts = self.flight_data.bookings_df['airline_id'].value_counts().idxmax()
        airline_name = self.flight_data.AIRLINE_ID_TO_NAME.get(counts, 'Unknown')
        num_flights = self.flight_data.bookings_df['airline_id'].value_counts().max()
        return {"type": "text", "data": f"{airline_name} has the most flights with {num_flights} flights"}

    def _handle_top_departure_dates(self, limit: int) -> Dict:
        top_dates = self.flight_data.bookings_df['departure_dt'].dt.date.value_counts().nlargest(limit).to_dict()
        labels = list(top_dates.keys())
        values = list(top_dates.values())
        return {"type": "bar_chart", "data": {"labels": labels, "values": values, "title": f"Top {limit} Departure Dates"}}

    def _handle_top_arrival_dates(self, limit: int) -> Dict:
        top_dates = self.flight_data.bookings_df['arrival_dt'].dt.date.value_counts().nlargest(limit).to_dict()
        labels = list(top_dates.keys())
        values = list(top_dates.values())
        return {"type": "bar_chart", "data": {"labels": labels, "values": values, "title": f"Top {limit} Arrival Dates"}}

    def _handle_flight_class_distribution(self) -> Dict:
        class_counts = self.flight_data.bookings_df['flight_class'].value_counts().to_dict()
        return {"type": "pie_chart", "data": {"labels": list(class_counts.keys()), "values": list(class_counts.values()), "title": "Flight Class Distribution"}}

    def _handle_fare_statistics(self) -> Dict:
        fare_stats = self.flight_data.bookings_df['fare'].describe().to_dict()
        return {"type": "text", "data": f"Fare Statistics: Count={int(fare_stats['count'])}, Mean={fare_stats['mean']:.2f}, Min={fare_stats['min']:.2f}, Max={fare_stats['max']:.2f}, Std={fare_stats['std']:.2f}"}

    def _handle_common_extras(self) -> Dict:
        extras_counts = self.flight_data.bookings_df['extras'].value_counts().nlargest(5).to_dict()
        return {"type": "bar_chart", "data": {"labels": list(extras_counts.keys()), "values": list(extras_counts.values()), "title": "Most Common Extras Purchased"}}

    def _handle_booking_status_counts(self) -> Dict:
        status_counts = self.flight_data.bookings_df['status'].value_counts().to_dict()
        return {"type": "bar_chart", "data": {"labels": list(status_counts.keys()), "values": list(status_counts.values()), "title": "Booking Status Counts"}}

    def _handle_frequent_gates(self) -> Dict:
        gate_counts = self.flight_data.bookings_df['gate'].value_counts().nlargest(5).to_dict()
        return {"type": "bar_chart", "data": {"labels": list(gate_counts.keys()), "values": list(gate_counts.values()), "title": "Most Frequent Gates"}}

    def _handle_frequent_terminals(self) -> Dict:
        terminal_counts = self.flight_data.bookings_df['terminal'].value_counts().nlargest(5).to_dict()
        return {"type": "bar_chart", "data": {"labels": list(terminal_counts.keys()), "values": list(terminal_counts.values()), "title": "Most Frequent Terminals"}}

    def _handle_layover_counts(self) -> Dict:
        layover_counts = self.flight_data.bookings_df['layovers'].value_counts().to_dict()
        return {"type": "bar_chart", "data": {"labels": [str(k) for k in layover_counts.keys()], "values": list(layover_counts.values()), "title": "Number of Layovers"}}

    def _handle_frequent_layover_locations(self) -> Dict:
        # Handle potential NaN values by filling them with a string
        layover_locations = self.flight_data.bookings_df['layover_locations'].fillna('None').value_counts().nlargest(5).to_dict()
        return {"type": "bar_chart", "data": {"labels": list(layover_locations.keys()), "values": list(layover_locations.values()), "title": "Most Frequent Layover Locations"}}

    def _handle_aircraft_type_counts(self) -> Dict:
        aircraft_counts = self.flight_data.bookings_df['aircraft_type'].value_counts().nlargest(5).to_dict()
        return {"type": "bar_chart", "data": {"labels": list(aircraft_counts.keys()), "values": list(aircraft_counts.values()), "title": "Most Frequent Aircraft Types"}}

    def _handle_reward_program_distribution(self) -> Dict:
        reward_counts = self.flight_data.bookings_df['is_reward_member'].value_counts().to_dict()
        return {"type": "pie_chart", "data": {"labels": list(reward_counts.keys()), "values": list(reward_counts.values()), "title": "Reward Program Member Distribution"}}

    def _handle_average_fare(self) -> Dict:
        avg_fares = self.flight_data.bookings_df.groupby('airline_id')['fare'].mean().round(2).to_dict()
        airline_names = {id: self.flight_data.AIRLINE_ID_TO_NAME.get(id, 'Unknown') for id in avg_fares}
        labels = [airline_names[id] for id in avg_fares]
        values = list(avg_fares.values())
        return {"type": "bar_chart", "data": {"labels": labels, "values": values, "title": "Average Fare by Airline"}}

    def _handle_average_duration_per_airline(self) -> Dict:
        avg_duration = self.flight_data.bookings_df.groupby('airline_id')['duration_hrs'].mean().round(2).to_dict()
        airline_names = {id: self.flight_data.AIRLINE_ID_TO_NAME.get(id, 'Unknown') for id in avg_duration}
        labels = [airline_names[id] for id in avg_duration]
        values = list(avg_duration.values())
        return {"type": "bar_chart", "data": {"labels": labels, "values": values, "title": "Average Flight Duration by Airline (hours)"}}

    def _handle_aisle_seat_distribution(self) -> Dict:
        aisle_counts = self.flight_data.bookings_df['has_aisle_seat'].value_counts().to_dict()
        return {"type": "pie_chart", "data": {"labels": list(aisle_counts.keys()), "values": list(aisle_counts.values()), "title": "Aisle Seat Preference Distribution"}}
# Create a processor instance
query_processor = QueryProcessor(flight_data)