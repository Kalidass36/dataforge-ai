# 🚀 DataForge AI

## AI-Powered Data Intelligence Platform

DataForge is an AI-powered data intelligence platform that allows users to query structured databases using natural language.

Instead of manually writing SQL queries, users can ask questions in plain English and DataForge converts them into SQL, validates the generated query, executes it against the database, and presents the results through an interactive dashboard.

---

## 🎯 Problem

Data teams often spend significant time:

- Understanding database schemas
- Writing SQL queries
- Debugging SQL errors
- Checking data quality
- Understanding unfamiliar datasets

DataForge automates several of these tasks using AI.

---

## 💡 Solution

DataForge provides:

- Automatic schema discovery
- Natural Language → SQL
- SQL validation
- Query execution
- Pipeline debugging
- Data quality monitoring
- AI-generated data catalog
- LangGraph-based agent workflow
- FastAPI backend
- Streamlit dashboard
- Automated testing
- Docker support

---

## 🏗️ Architecture

User
↓
Streamlit Dashboard
↓
FastAPI
↓
LangGraph Agent
↓
Natural Language → SQL
↓
SQL Validation
↓
SQLite Database
↓
Query Results

---

## 🛠️ Tech Stack

- Python
- SQLAlchemy
- SQLite
- FastAPI
- Streamlit
- LangGraph
- Ollama
- Pydantic
- Pytest
- Docker

---

## ✨ Features

### 1. Schema Intelligence

Automatically discovers database tables and columns.

### 2. Natural Language SQL

Users can ask questions such as:

"Show me the top 5 customers by spending."

DataForge generates SQL automatically.

### 3. SQL Validation

Generated SQL is checked before execution.

### 4. Pipeline Debugging

The system identifies errors and attempts to provide useful corrections.

### 5. Data Quality Monitoring

Checks for common data quality problems.

### 6. AI Data Catalog

Creates an understandable catalog of available data.

### 7. LangGraph Agent

Coordinates the different AI/data processing steps.

### 8. FastAPI

Provides programmatic API access.

### 9. Streamlit

Provides an interactive user interface.

### 10. Testing

Automated tests validate important application components.

---

## 🚀 Example

User:

Show me the top 5 customers by spending

DataForge:

Natural language
→ AI interpretation
→ SQL generation
→ SQL validation
→ Database execution
→ Results

---

## 📁 Project Structure

```text
dataforge/
│
├── app/
│   ├── api/
│   ├── catalog/
│   ├── quality/
│   ├── ui/
│   └── ...
│
├── data/
│
├── tests/
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── pytest.ini
└── README.md
