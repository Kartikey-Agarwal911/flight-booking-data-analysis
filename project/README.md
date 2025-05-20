# Flight Booking Data Analysis Application

A full-stack application that enables users to query and visualize flight booking data using natural language.

## Features

- Interactive chat interface for natural language queries
- Real-time response handling with intermediate updates during processing
- Dynamic data visualization based on query type
- Support for various query complexities (basic, intermediate, advanced)
- Backend LLM-powered data processing

## Tech Stack

### Frontend
- React 18
- TypeScript
- Tailwind CSS for styling
- Highcharts for data visualization
- Lucide React for icons

### Backend
- FastAPI (Python)
- Pandas for data processing
- Simulated LLM processing (can be replaced with OpenAI/LangChain)

## Getting Started

### Prerequisites
- Node.js (v18 or higher)
- Python (v3.10 or higher)

### Installation

1. Clone the repository
2. Install frontend dependencies:

```bash
npm install
```

3. Install backend dependencies:

```bash
cd backend
pip install -r requirements.txt
```

### Running the Application

1. Start the backend server:

```bash
cd backend
python main.py
```

2. Start the frontend development server:

```bash
npm run dev
```

3. Open your browser and navigate to http://localhost:5173

## Sample Queries

The application can handle a variety of flight data queries, such as:

- Which airline has the most flights listed?
- What are the top three most frequented destinations?
- Number of bookings for American Airlines yesterday
- Average flight delay per airline
- Month with the highest number of bookings
- Display all transactions between March 1 and March 15
- Compare bookings for American Airlines and Delta for last week

## Implementation Notes

- The backend currently uses simulated flight data for demonstration purposes
- In a production environment, you would connect to a real database
- The LLM processing is simplified for this demo (rule-based matching)
- For production use, integrate with OpenAI or another LLM provider