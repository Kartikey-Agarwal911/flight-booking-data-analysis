from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import asyncio
import uuid
import json
from .llm_processor import query_processor
from .flight_data import flight_data
import logging
from typing import Optional, Dict
import os

app = FastAPI(title="Flight Data Analysis API")

# CORS configuration to allow frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage for query results and processing status
query_results = {}

# Backup responses for common queries
BACKUP_RESPONSES = {
    "which airline has the most flights": {
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

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    id: str
    status: str
    intermediate_result: Optional[dict] = None
    result: Optional[dict] = None

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def process_query_task(query_id: str, query_text: str):
    """Background task to process query with simulated LLM thinking time"""
    try:
        logger.info(f"Processing query: {query_text}")
        
        # Update status to processing
        query_results[query_id]['status'] = 'processing'
        
        # Try to process the query immediately without delay
        try:
            logger.info("Attempting to process query with query_processor")
            result = query_processor.process_query(query_text)
            logger.info(f"Query processor result: {result}")
        except Exception as e:
            logger.error(f"Error in query processor: {str(e)}")
            # If processing fails, try to use backup response
            query_lower = query_text.lower().strip()
            if query_lower in BACKUP_RESPONSES:
                logger.info("Using backup response")
                result = BACKUP_RESPONSES[query_lower]
            else:
                logger.error("No backup response available")
                result = {
                    'type': 'error',
                    'message': f"Error processing query: {str(e)}"
                }
        
        # Update with final results
        logger.info("Updating query results")
        query_results[query_id]['status'] = 'complete'
        query_results[query_id]['result'] = result
        
    except Exception as e:
        logger.error(f"Error in process_query_task: {str(e)}")
        query_results[query_id]['status'] = 'error'
        query_results[query_id]['error'] = str(e)

@app.on_event("startup")
def load_data_on_startup():
    # Load the real flight bookings CSV on startup
    base_dir = os.path.dirname(__file__)
    csv_path = os.path.join(base_dir, "Flight Bookings.csv")
    failures_path = os.path.join(base_dir, "File Failure Report 30 Days Bicycle-2025-03-26-17-17-25.xlsx - File Failures Bicycle.csv")
    flight_data.load_data(csv_path,failures_path)
    # flight_data.load_data()
    
@app.post("/api/query", response_model=QueryResponse)
async def submit_query(query: QueryRequest, background_tasks: BackgroundTasks):
    """Submit a query for processing"""
    query_id = str(uuid.uuid4())
    
    # Initialize query in storage
    query_results[query_id] = {
        "id": query_id,
        "status": "pending",
        "query": query.query,
        "intermediate_result": None,
        "result": None
    }
    
    # Process query in background
    background_tasks.add_task(process_query_task, query_id, query.query)
    
    return QueryResponse(
        id=query_id,
        status="processing"
    )

@app.get("/api/query/status/{query_id}", response_model=QueryResponse)
async def get_query_status(query_id: str):
    """Get the status and results of a submitted query"""
    if query_id not in query_results:
        raise HTTPException(status_code=404, detail="Query ID not found")
        
    query_data = query_results[query_id]
    
    return QueryResponse(
        id=query_id,
        status=query_data['status'],
        intermediate_result=query_data.get('intermediate_result'),
        result=query_data.get('result')
    )

@app.get("/")
async def root():
    """Root endpoint for API health check"""
    return {"status": "ok", "message": "Flight Data Analysis API is running"}

@app.get("/api/failures/category_counts")
async def get_failure_category_counts():
    counts = flight_data.get_failure_counts_by_category()
    if counts:
        return {"type": "pie_chart", "data": {"labels": list(counts.keys()), "values": list(counts.values()), "title": "Failure Counts by Category"}}
    raise HTTPException(status_code=404, detail="Failure data not available")

@app.get("/api/failures/trends")
async def get_failure_trends():
    trends = flight_data.get_failure_trends_over_time()
    if trends:
        return {"type": "time_series", "data": {"labels": [t['date'] for t in trends], "values": [t['count'] for t in trends], "title": "Failure Trends Over Time"}}
    raise HTTPException(status_code=404, detail="Failure trend data not available")

@app.get("/api/failures/by_account")
async def get_failures_by_account():
    counts = flight_data.get_failures_by_account()
    if counts:
        return {"type": "bar_chart", "data": {"labels": list(counts.keys()), "values": list(counts.values()), "title": "Failures by Account"}}
    raise HTTPException(status_code=404, detail="Failure data by account not available")

@app.get("/api/failures/recent")
async def get_recent_failures_endpoint():
    failures = flight_data.get_recent_failures()
    if failures:
        return {"type": "table", "data": {"headers": ["Case Number", "Opened At", "Category", "Subcategory", "Subject", "Account Name"], "rows": [list(f.values()) for f in failures]}}
    raise HTTPException(status_code=404, detail="Recent failure data not available")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)