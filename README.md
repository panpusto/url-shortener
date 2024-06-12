# URL shortener API

This app is based on FastAPI framework. It allows users to create short URL for provideded full url address, track how many times this short url was clicked and to delete it. At this stage of development API is allowed for any user.

## Contents

- [Main technologies](#main-technologies)
- [Features implemented](#features-implemented)
- [URLs](#urls)
- [Features to implement](#features-to-implement)

## **Main technologies**

- FastAPI
- PostgreSQL
- Docker
- docker-compose
- pytest

## **Features implemented**

- creating shortened urls
- tracking the number of visits on the website from the created link using admin's secret key
- deleting created link using admin's secret key

## **URLs**

- http://localhost:8000/urls - <span style="color:green">POST</span> - send target url to create shortened link
- http://localhost:8000/{url_key} - <span style="color:blue">GET</span> - redirect to target url by created shortened url
- http://localhost:8000/admin/{secret_key} - <span style="color:blue">GET</span> - receive admin info about created shortened url
- http://localhost:8000/admin/{secret_key} - <span style="color:red">DELETE</span> -
- http://localhost:8000/docs - <span style="color:blue">GET</span> - API documentation

## **Features to implement**

- generating QR codes for provided link
- sending email with shortened link, admin info link and generated QR code to user
- creating UI with React
- user registration and authentication via JSON Web Token
