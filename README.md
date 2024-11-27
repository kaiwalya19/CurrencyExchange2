Created by:    Kaiwalya Kshirsagar
Date:          26-11-2024
LinkedIn:      https://www.linkedin.com/in/kaiwalyakshirsagar/

This project is a backend system for managing currency exchange rates. It provides APIs for CRUD operations, currency conversion, and historical rate management, with asynchronous task handling using Celery.

---

## **Features**
- **Currency Management**: CRUD operations for currencies.
- **Exchange Rate Management**: Fetch and manage exchange rates dynamically.
- **Currency Conversion**: Real-time conversion with caching support.
- **Historical Rate Management**: Fetch historical exchange rates using external APIs.
- **Asynchronous Processing**: Celery integration for background tasks.
- **Dockerized Deployment**: Run the project with Docker Compose.

---

## **Setup Instructions**

### **Using Docker**
1. Build and start the services:
   ```bash
   docker-compose up --build
Access the application:

App: http://localhost:8000
Admin: http://localhost:8000/admin

API Endpoints
Endpoint	HTTP Method	Description
/api/currency/	GET	List all currencies.
/api/currency/	POST	Create a new currency.
/api/currency/<int:pk>/	GET	Retrieve details of a specific currency by ID.
/api/currency/<int:pk>/	PUT/PATCH	Update a specific currency by ID.
/api/currency/<int:pk>/	DELETE	Delete a specific currency by ID.
/api/exchange-rate/	GET	Fetch exchange rates by source currency and date range.
/api/convert/	GET	Convert an amount between two currencies.

Example Requests
Fetch Exchange Rates

http
Copy code
GET /api/exchange-rate/?source_currency=USD&date_from=2023-01-01&date_to=2024-11-30
Convert Currency

http
Copy code
GET /api/convert/?source_currency=USD&target_currency=EUR&amount=100


File Structure and Functions
Core Application Files


File	Purpose
models.py	      Defines database models (Currency and CurrencyExchangeRate).
serializers.py	   Serializes models into JSON and validates API inputs.
views.py	         Implements API endpoints for currency management, exchange rate retrieval, and conversion.
urls.py	         Maps URLs to views for routing.
tasks.py	         Defines asynchronous tasks for fetching historical rates.
adapters.py	      Handles integration with external APIs (e.g., CurrencyBeacon) for exchange rate data.
admin.py	         Customizes the admin interface for managing currencies and exchange rates.
celery.py	      Configures Celery for task queue handling.


Supporting Files
File	                                 Purpose
.gitignore	                           Specifies files and directories to ignore in version control.
Dockerfile	                           Defines the environment for running the Django app in Docker.
docker-compose.yml	                  Orchestrates multiple services, including the Django app, Redis, and Celery workers.
manage.py	                           Entry point for running Django commands.
README.md	                           Documentation for setup, usage, and project details.
Currency.postman_collection.json       Postman collection to test APIs

Environment Variables
Variable	               Description
CURRENCYBEACON_API_KEY	API key for the CurrencyBeacon provider.
SECRET_KEY	            Django secret key for encryption.


