# Flight Booking Data Analysis Project

## Overview

This project is a web application designed to provide insights into flight booking data through an interactive chat interface.  Instead of navigating through tables or complex reports, users can ask questions in natural language and receive concise answers, sometimes accompanied by helpful visualizations.

This application was developed for an assignment, and this document explains how it works, where it's deployed, and how to use it.

## Key Features

* **Natural Language Chat Interface:** The core of the application is a chat interface.  You can type questions about flight data, such as "Which airline has the most flights?" or "Show me the top departure dates."
* **Data-Driven Responses:** The application's backend processes your questions and retrieves the relevant information from the flight data.
* **Textual Answers:** Many questions are answered with clear, straightforward text.
* **Visualizations:** For some questions, the application will generate charts (like bar charts) to help you quickly understand trends or patterns in the data.
* **Backend (FastAPI):** The application uses a Python-based backend, built with FastAPI.  This handles the data processing and query logic.
* **Frontend (React):** The user interface you interact with in your browser is built with React.  It's responsible for the chat interface and displaying the results.

## How it Works (Simplified)

1.  You type a question in the chat interface.
2.  The React frontend sends your question to the FastAPI backend.
3.  The FastAPI backend analyzes your question, retrieves the data, and prepares a response (either text or data for a chart).
4.  The FastAPI backend sends the response back to the React frontend.
5.  The React frontend displays the response to you.  If it's chart data, it will render the chart.

## Technologies Used

* **Backend:**
    * Python
    * FastAPI (for the web API)
    * Pandas (for data analysis)
* **Frontend:**
    * React (for the user interface)
    * JavaScript
    * HTML
    * CSS (Tailwind CSS for styling)
* **Testing:**
    * pytest (for backend testing)
    * react-testing-library (for frontend testing)

## Where to Find the Code and Application

* **GitHub Repository:** The complete source code for this project is available on GitHub: [https://github.com/Kartikey-Agarwal911/flight-booking-data-analysis](https://github.com/Kartikey-Agarwal911/flight-booking-data-analysis)
* **Live Application:** You can use the application directly in your browser at this address: [https://flight-booking-data-a-git-43c2ab-kartikey-agarwal911-s-projects.vercel.app?\_vercel\_share=g2JyTd1hLTs4PDthPlFAineHXbXBGE4I](https://flight-booking-data-a-git-43c2ab-kartikey-agarwal911-s-projects.vercel.app?_vercel_share=g2JyTd1hLTs4PDthPlFAineHXbXBGE4I)

## How to Use the Application (For the Reviewer)

Here's how you can interact with the application:

1.  **Open the Application:** Go to this URL in your web browser: [https://flight-booking-data-a-git-43c2ab-kartikey-agarwal911-s-projects.vercel.app?\_vercel\_share=g2JyTd1hLTs4PDthPlFAineHXbXBGE4I](https://flight-booking-data-a-git-43c2ab-kartikey-agarwal911-s-projects.vercel.app?_vercel_share=g2JyTd1hLTs4PDthPlFAineHXbXBGE4I)
2.  **Use the Chat Interface:**
    * You'll see a chat window with a welcome message and some example questions.
    * Type your own question in the input box at the bottom.
    * Click the "Ask" button (or press Enter).
    * The application will respond in the chat window.
    * If the answer is a simple text response, it will appear directly.
    * If the answer is best shown as a chart, you'll see a message like "[Visualization Available Below]", and the chart will be displayed.

## Example Questions to Try

Here are some questions you can ask to see the application in action:

* "Which airline has the most flights?"
* "What are the top 2 departure dates?"
* "Show me the flight class distribution."

## For the Assignment Reviewer

Thank you for taking the time to review this project.

* The application is deployed and ready to use at the Vercel link provided above.
* The complete code is on GitHub, so you can examine the implementation.
* The application allows users to ask questions about flight data in a conversational way.
* The application provides both textual and visual responses.

I hope this project demonstrates a good understanding of the technologies involved and provides a useful way to interact with flight data. If you have any questions, please feel free to ask.
