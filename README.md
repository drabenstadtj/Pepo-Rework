# Pepo Exchange

## Overview

**Pepo Exchange** is a simulated stock market platform that allows users to experience a realistic trading environment. The platform integrates a Flask-based backend for handling core logic, MongoDB for data storage, and an Express.js-based frontend with Pug for rendering the user interface. Stock prices are dynamically updated based on live data fetched from Google Trends, providing a simulated stock market experience.

---

## Table of Contents

1. [Project Architecture](#project-architecture)
2. [Features](#features)
3. [Backend](#backend)
    - [Backend Endpoints](#backend-endpoints)
4. [Frontend](#frontend)
    - [Frontend Routes](#frontend-routes)
5. [Setting Up the Project](#setting-up-the-project)
6. [Docker Setup](#docker-setup)
7. [Scheduled Tasks](#scheduled-tasks)
8. [Error Handling and Logging](#error-handling-and-logging)

---

## Project Architecture

Pepo Exchange consists of two major components:

- **Backend**: A Flask application that handles user authentication, portfolio management, transaction processing, and stock updates. MongoDB is used for storing user data, stock information, and transactions.
- **Frontend**: An Express.js application using Pug templates for rendering. It communicates with the backend through API calls and provides the interface for users to interact with the platform.

---

## Features

- **User Authentication**: JWT-based login and registration, with session management.
- **Portfolio Management**: Users can view and manage their stock portfolios.
- **Transaction Handling**: Buy and sell stocks, with real-time price updates.
- **Live Stock Prices**: Stock prices are updated periodically based on Google Trends data.
- **Leaderboard**: Users are ranked based on their net worth.
- **Scheduled Tasks**: Stock prices are updated every hour using Celery and Redis for scheduling.

---

## Backend

The backend is built with Flask and follows a service-oriented architecture, where each feature (such as user authentication, stocks, or transactions) is handled by a separate service. The Flask application is organized into routes, services, and utility modules.

### Backend Endpoints

#### Authentication

| HTTP Method | Endpoint          | Description                                       |
|-------------|-------------------|---------------------------------------------------|
| POST        | /auth/register     | Registers a new user.                            |
| POST        | /auth/verify_credentials | Verifies user credentials and issues a JWT.  |
| GET         | /auth/get_user_id  | Retrieves a user's ID based on the username.      |

#### Portfolio

| HTTP Method | Endpoint               | Description                            |
|-------------|------------------------|----------------------------------------|
| GET         | /portfolio/stocks       | Fetches the user's portfolio.          |
| GET         | /portfolio/balance      | Fetches the user's balance.            |
| GET         | /portfolio/assets_value | Fetches the total value of user's assets. |

#### Stocks

| HTTP Method | Endpoint               | Description                                    |
|-------------|------------------------|------------------------------------------------|
| GET         | /stocks/               | Fetches all available stocks.                  |
| GET         | /stocks/:symbol        | Fetches the current price of a specific stock. |

#### Transactions

| HTTP Method | Endpoint               | Description                                    |
|-------------|------------------------|------------------------------------------------|
| POST        | /transactions/buy      | Buys a stock.                                  |
| POST        | /transactions/sell     | Sells a stock.                                 |
| GET         | /transactions/         | Fetches all transactions for the authenticated user. |

---

## Frontend

The frontend is an Express.js application that serves as the user interface for Pepo Exchange. It uses Pug templates for rendering HTML pages and communicates with the backend via API calls to fetch stock data, manage user portfolios, and execute transactions.

### Frontend Routes

#### Authentication

| HTTP Method | Route       | Description |
|-------------|-------------|-------------|
| GET         | /auth/signup   | Render the signup page. |
| POST        | /auth/signup   | Handle signup requests. |
| GET         | /auth/signin   | Render the signin page. |
| POST        | /auth/signin   | Handle signin requests. |
| GET         | /auth/logout   | Log the user out and clear the session. |

#### Main Pages

| HTTP Method | Route       | Description |
|-------------|-------------|-------------|
| GET         | /           | Render the homepage (requires login). |
| GET         | /about      | Render the about page (requires login). |

#### Portfolio

| HTTP Method | Route       | Description |
|-------------|-------------|-------------|
| GET         | /portfolio/balance      | Fetch the user's balance. |
| GET         | /portfolio/assets_value | Fetch the user's total assets value. |
| GET         | /portfolio/stocks       | Fetch the user's portfolio stocks. |

#### Stocks

| HTTP Method | Route       | Description |
|-------------|-------------|-------------|
| GET         | /stocks     | Fetch all available stocks and render the stocks page. |

#### Trading

| HTTP Method | Route       | Description |
|-------------|-------------|-------------|
| GET         | /trade      | Render the trade page, fetch portfolio and balance data. |

#### Leaderboard

| HTTP Method | Route       | Description |
|-------------|-------------|-------------|
| GET         | /leaderboard | Render the leaderboard page. |

---

## Setting Up the Project

### Backend

1. Navigate to the backend/ directory.
   ` cd backend `

2. Install the dependencies:
   ` pip install -r requirements.txt `

3. Set up environment variables by creating a .env file:
   ` ` env
   DATABASE_URI=mongodb://mongo:27017/gourdstocks
   SECRET_KEY=your_secret_key
   LOG_LEVEL=DEBUG
   ` `

4. Run the backend:
   ` python run.py `

### Frontend

1. Navigate to the frontend/ directory:
   ` cd frontend `

2. Install the dependencies:
   ` npm install `

3. Set up environment variables in .env:
   ` ` env
   CONFIG=development
   SECRET_KEY=your_secret_key
   SESSION_SECRET=your_session_secret
   SIGNUP_PASSCODE=your_signup_passcode
   ` `

4. Run the frontend:
   ` npm start `

---

## Docker Setup

Both the backend and frontend are Dockerized, making it easy to set up and run the project in containers.

1. **Build and Start the Backend and Frontend Containers**:
   ` docker-compose up --build `

2. **Access the Application**:
   - Backend API: ` http://localhost:5000 `
   - Frontend: ` http://localhost:3000 `

---

## Scheduled Tasks

The backend uses Celery with Redis as the message broker to schedule periodic tasks like updating stock prices every hour.

- **Updating Stock Prices**: The stock prices are updated based on the live data fetched from Google Trends, which simulates real-time market changes.

---

## Error Handling and Logging

Both the frontend and backend log errors using morgan and logging respectively.

- **Backend Logs**: Stored in /logs/app.log.
- **Frontend Logs**: Displayed in the console using morgan.

Error messages and stack traces are printed to the logs, making it easy to debug issues.

---
