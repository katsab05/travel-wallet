# 🧳 Travel Wallet API

A FastAPI-based backend project designed to manage trip budgets, expenses, documents, and currency conversions. Built to demonstrate clean architecture, test-driven development, and async Python backend development aligned with PwC's Python Developer role.

---

## 🚀 Project Goal

The goal of this project is to simulate a professional-grade backend API service for travel budget management. It supports authenticated users to:
- Create trips
- Log expenses
- Upload travel documents
- Convert currencies using an external service
- Reset passwords via secure token workflows


## 🛠 Setup Instructions

### 🔧 Requirements
- Docker and Docker Compose
- Python 3.11 (for development outside Docker)

### 🐳 Quickstart with Docker

```bash
# Clone repo
git clone https://github.com/katsab05/travel-wallet.git
cd travel-wallet

# Build and run
docker-compose up --build

# Visit app (FastAPI)
http://localhost:8000/docs
