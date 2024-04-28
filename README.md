# Paramount+ Clone

This project is a clone of the Paramount+ streaming service, showcasing my development skills. It utilizes a Vue.js frontend and a Django backend, deployed using various AWS services such as AWS Amplify, App Runner, S3, VPC, Route 53, Secrets Manager, and RDS. The project is containerized using Docker. If moved to Elastic Containers on AWS, this could be a fully scalable streaming website (with some clean up).

## Live Demo

Check out the live demo of the Paramount+ clone at: [paramountminus.me](https://paramountminus.me)

## Project Repositories

The Paramount+ clone consists of two separate repositories for the frontend and backend:

- Frontend: [https://github.com/davidscottconrad/frontend-netflax](https://github.com/davidscottconrad/frontend-netflax)
- Backend: [https://github.com/davidscottconrad/django9](https://github.com/davidscottconrad/django9)

## Technologies Used

- Frontend:
  - Vue.js
  - HTML/CSS/JavaScript
- Backend:
  - Django
  - Python
- Database:
  - Amazon RDS
- Deployment:
  - AWS Amplify
  - AWS App Runner
  - AWS S3
  - AWS VPC
  - AWS Route 53
  - AWS Secrets Manager
- Containerization:
  - Docker

## Features

- Browse and search for movies and TV shows
- Stream content (I used open liscenced videos)
- Responsive and user-friendly interface

## Architecture

The Paramount+ clone follows a client-server architecture. The frontend is built with Vue.js, which communicates with the Django backend via API calls. The backend handles the business logic, data persistence, and authentication.

The application is deployed using various AWS services:

- AWS Amplify is used for hosting the frontend and managing the deployment pipeline.
- AWS App Runner is used to run the backend Django application.
- AWS S3 is used for storing static files and media content.
- AWS VPC provides a secure and isolated network environment.
- AWS Route 53 handles the domain routing and DNS management.
- AWS Secrets Manager securely stores sensitive information like database credentials.
- Amazon RDS is used as the database to store user information, movie/TV show details, and watchlists.

The entire application is containerized using Docker, ensuring a consistent and reproducible environment across different stages of development and deployment.

## Contact

For any inquiries or questions, feel free to reach out to me:

- [Resume](https://github.com/davidscottconrad/frontend-netflax/blob/main/public/Resume.pdf)
- Email: David.Scott.Conrad@gmail.com
- LinkedIn: [Your LinkedIn](https://linkedin.com/in/david-scott-conrad)
