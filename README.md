QuickCart is a microservices-based B2C quick commerce application inspired by modern instant delivery platforms. The application enables users to browse products, add items to cart, place orders, and track deliveries in real time.

This project is developed to demonstrate backend fundamentals, microservices architecture, Flutter mobile development, containerization, and deployment concepts.

The primary focus is on clean architecture, working APIs, and complete end-to-end flow rather than production-level scalability or advanced UI design.

🎯 Objectives

Build a minimal yet functional quick-commerce platform

Implement microservices architecture

Develop RESTful APIs using FastAPI

Create a Flutter mobile frontend

Containerize services using Docker

Deploy using Docker Compose and Kubernetes

Ensure complete user-to-delivery workflow

🏗 Architecture

The system is divided into independent microservices:

1️⃣ User Service

User registration

Login & authentication

User data management

2️⃣ Product Service

Product listing

Product details

Seed product data

3️⃣ Cart & Order Service

Add to cart

Create and manage orders

Order history

4️⃣ Delivery Service

Order status updates

Delivery tracking simulation

5️⃣ Flutter Mobile App

User interface

API integration

Order tracking screen

🛠 Tech Stack
Backend

Python (FastAPI)

MongoDB

REST APIs

Frontend

Flutter (Dart)

DevOps & Deployment

Docker

Docker Compose

Kubernetes

📂 Project Structure
quickcart/
├── user-service/
├── product-service/
├── cart-order-service/
├── delivery-service/
├── flutter-app/
├── kubernetes/
├── docker-compose.yml
└── README.md
🔄 Application Flow

User signs up or logs in

User browses products

User adds items to cart

User places an order

Delivery service updates order status

User tracks order in real time

🚀 Running the Project
Using Docker Compose
docker-compose up --build
Access Services

User Service → http://localhost:8001

Product Service → http://localhost:8002

Cart Service → http://localhost:8003

Delivery Service → http://localhost:8004

📚 Learning Outcomes

This project demonstrates:

Microservices architecture design

REST API development

Authentication handling

Database modeling

Flutter backend integration

Docker containerization

Kubernetes deployment basics

📌 Future Improvements

Payment gateway integration

Real-time notifications

Role-based authentication

API gateway implementation

CI/CD pipeline setup
