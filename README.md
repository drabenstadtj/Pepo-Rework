# Pepo Exchange - Developer Documentation

## Overview

**Pepo Exchange** is a simulated stock market platform built to provide users with a realistic trading environment. The project integrates a Flask-based backend (API) with MongoDB for data storage and an Express.js-based frontend using Pug for the UI.

The platform dynamically updates stock prices based on Google Trends data and runs scheduled background tasks using Celery and Redis to ensure real-time simulation. This project handles user authentication, stock transactions, and portfolio management.

---

## Table of Contents

1. [Project Architecture](#project-architecture)
2. [Setup](#setup)
    - [Backend](#backend-setup)
    - [Frontend](#frontend-setup)
    - [Environment Variables](#environment-variables)
    - [Docker Setup](#docker-setup)
3. [Development Workflow](#development-workflow)
    - [Backend Structure](#backend-structure)
    - [Frontend Structure](#frontend-structure)
    - [Celery Tasks](#celery-tasks)
    - [Error Handling and Logging](#error-handling-and-logging)
4. [Future Improvements](#future-improvements)

---

## Project Architecture

- **Backend (Flask)**:
  - Handles all business logic, user authentication, stock data, and transactions.
  - MongoDB is used to persist user data, stock information, and transactions.
  - JWT is used for user authentication.
  
- **Frontend (Express.js)**:
  - Pug templates for rendering pages.
  - Express.js handles routes and connects to the backend via Axios.
  
- **Background Tasks**:
  - Celery with Redis as the message broker handles scheduled tasks like updating stock prices using Google Trends data.

---

## Setup

### Backend Setup

1. **Navigate to the `backend` directory**:
   ` cd backend `

2. **Install dependencies**:
   ` pip install -r requirements.txt `

3. **Setup environment variables**:
   Create a `.env` file and configure the following variables:
   ``` env
   DATABASE_URI=mongodb://mongo:27017/gourdstocks
   SECRET_KEY=your_secret_key
   LOG_LEVEL=DEBUG
   ```

4. **Run the backend**:
   ` python run.py `

### Frontend Setup

1. **Navigate to the `frontend` directory**:
   ` cd frontend `

2. **Install frontend dependencies**:
   ` npm install `

3. **Setup environment variables**:
   Create a `.env` file and configure the following:
   ``` env
   CONFIG=development
   SECRET_KEY=your_secret_key
   SESSION_SECRET=your_session_secret
   SIGNUP_PASSCODE=your_signup_passcode
   ```

4. **Run the frontend**:
   ` npm start `

### Docker Setup

1. **Build and start the backend and frontend**:
   ` docker-compose up --build `

2. **Access**:
   - Backend API: ` http://localhost:5000 `
   - Frontend: ` http://localhost:3000 `

---

## Development Workflow

### Backend Structure

- **app/**: Contains the core business logic of the backend.
  - **routes/**: API route definitions (authentication, stocks, portfolio, transactions).
  - **services/**: All the services used to manage user data, transactions, stocks, etc.
  - **config.py**: Application configuration.
  - **run.py**: Main entry point for running the Flask app.

- **Logging**:
  - Logs are stored in the `logs/app.log` file, which captures important runtime information.

- **MongoDB**:
  - The database is structured to store users, stocks, portfolios, and transaction data.
  - The `DATABASE_URI` should be defined in `.env`.

### Frontend Structure

- **app.js**: Main entry point for the Express app.
- **config/**: Configuration and environment setup (pulls from `.env`).
- **middleware/**: Middleware functions for attaching tokens and checking user roles.
- **routes/**: Defines all the routes for the frontend (auth, portfolio, stocks, trade, etc.).
- **views/**: Pug templates for rendering the UI.
- **public/**: Contains static assets like CSS and images.

### Celery Tasks

Scheduled background tasks are handled using **Celery**:

- **Update Stock Prices**:
  - Fetches live interest data from Google Trends and updates stock prices hourly.
  - Implemented in `tasks.py` with a Celery Beat schedule configured in `celery_config.py`.
  
- **Task Scheduling**:
  - Stock prices are updated using Celery Beat and Redis, ensuring real-time price changes.
  - Configuration for Redis is in the `docker-compose.yml` and `.env`.

---

## Error Handling and Logging

- **Backend**:
  - The backend logs errors and relevant runtime info into `logs/app.log` using Python’s built-in `logging` library.

- **Frontend**:
  - The frontend uses `morgan` for logging HTTP requests and error handling middleware for catching issues.

- **JWT Error Handling**:
  - If a user's JWT token expires or is invalid, they are redirected to the login page.

---

## Future Improvements

- **Unit Tests**: Add comprehensive unit and integration tests for backend services and frontend components.
- **Rate Limiting**: Implement rate limiting on API routes to prevent abuse.
- **Enhanced UI**: Improve the user interface with additional real-time data and visual feedback for stock transactions.
- **Scalability**: Refactor the backend to support horizontal scaling, particularly for handling large datasets and high user traffic.
