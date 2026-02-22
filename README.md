# Blinkit Clone - Quick Commerce Application

## 📋 Overview
A minimal quick-commerce application similar to Blinkit built with microservices architecture.

## 🏗️ Architecture
The application consists of 4 microservices:
1. **User Service** - Handles user registration, login, and profile
2. **Product Catalog Service** - Manages products and categories
3. **Cart and Order Service** - Handles shopping cart and orders
4. **Delivery Service** - Manages order delivery status

## 🔧 Technology Stack
- **Backend**: Python, FastAPI
- **Frontend**: Flutter
- **Database**: MongoDB
- **Containerization**: Docker
- **Orchestration**: Kubernetes (minikube)
- **Communication**: REST APIs

## 📦 Services and Ports
| Service | Port | Description |
|---------|------|-------------|
| User Service | 8001 | Authentication |
| Product Service | 8002 | Product catalog |
| Cart-Order Service | 8003 | Cart and orders |
| Delivery Service | 8004 | Delivery tracking |

## 🚀 How to Run

### Prerequisites
- Docker Desktop
- Python 3.9+
- Flutter
- MongoDB Compass (optional)

### Using Docker Compose (Local Development)
```bash
# Clone the repository
git clone <repository-url>
cd blinkit-clone

# Start all services
docker-compose up -d

# Seed product data
cd product-service
python seed_data.py

# Run Flutter app
cd flutter-app
flutter pub get
flutter run