# DaliPrint API

A FastAPI-based backend system for managing print shop orders with automated cost calculation. Designed for local printing businesses to streamline order management and eliminate manual calculation errors.

## 🎯 Project Overview

DaliPrint API solves the operational challenges of manual print shop workflows:
- **Eliminates Manual Recording**: Digital order entry instead of paper logs
- **Prevents Calculation Errors**: Automated cost computation based on print type and page count
- **Organizes Queue Management**: Maintains a fair "first-come, first-served" order system
- **Enables Instant Retrieval**: Attendants can pull up order details instantly

## 📋 Key Features

✅ **In-Memory Storage** - No external database required  
✅ **Automated Cost Calculation** - Real-time pricing based on print type  
✅ **UUID Order IDs** - Unique identifier generation for each order  
✅ **Error Validation** - Input validation with descriptive error messages  
✅ **RESTful API** - Clean, intuitive endpoints  
✅ **Interactive API Docs** - Built-in Swagger UI and ReDoc  

## 🚀 Quick Start

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

### Installation

1. **Clone/Navigate to project directory:**
   ```bash
   cd c:\Users\nvnmr\OneDrive\Desktop\z
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

**Start the server:**
```bash
python main.py
```

The API will be available at:
- **API Base URL**: `http://localhost:8000`
- **Swagger UI Docs**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## 📚 API Endpoints

### 1. Create New Order
**POST** `/orders/`

Creates a new print order with automated cost calculation.

**Request Body:**
```json
{
  "customer_name": "John Doe",
  "document_name": "Resume.pdf",
  "pages": 5,
  "print_type": "Black & White"
}
```

**Response (201 Created):**
```json
{
  "order_id": "550e8400-e29b-41d4-a716-446655440000",
  "customer_name": "John Doe",
  "document_name": "Resume.pdf",
  "pages": 5,
  "print_type": "Black & White",
  "total_cost": 10.0,
  "status": "Pending"
}
```

### 2. Retrieve All Orders
**GET** `/orders/`

Returns a list of all orders currently in the system.

**Response (200 OK):**
```json
[
  {
    "order_id": "550e8400-e29b-41d4-a716-446655440000",
    "customer_name": "John Doe",
    "document_name": "Resume.pdf",
    "pages": 5,
    "print_type": "Black & White",
    "total_cost": 10.0,
    "status": "Pending"
  },
  {
    "order_id": "660e8400-e29b-41d4-a716-446655440001",
    "customer_name": "Jane Smith",
    "document_name": "Brochure.pdf",
    "pages": 100,
    "print_type": "Colored",
    "total_cost": 500.0,
    "status": "Pending"
  }
]
```

### 3. Retrieve Specific Order
**GET** `/orders/{order_id}`

Retrieves details of a specific order by ID.

**Response (200 OK):**
```json
{
  "order_id": "550e8400-e29b-41d4-a716-446655440000",
  "customer_name": "John Doe",
  "document_name": "Resume.pdf",
  "pages": 5,
  "print_type": "Black & White",
  "total_cost": 10.0,
  "status": "Pending"
}
```

**Error (404 Not Found):**
```json
{
  "detail": "Order with ID invalid-id not found"
}
```

## 💰 Pricing Rates

| Print Type | Rate | Formula |
|:--|:--|:--|
| Black & White | PHP 2.00/page | `pages × 2.00` |
| Colored | PHP 5.00/page | `pages × 5.00` |
| Photo Paper | PHP 20.00/page | `pages × 20.00` |

### Pricing Examples
- 5 pages, Black & White → PHP 10.00
- 10 pages, Colored → PHP 50.00
- 2 pages, Photo Paper → PHP 40.00

## 🧪 Testing with cURL

### Create an Order
```bash
curl -X POST "http://localhost:8000/orders/" \
  -H "Content-Type: application/json" \
  -d '{
    "customer_name": "Maria Santos",
    "document_name": "Thesis.pdf",
    "pages": 150,
    "print_type": "Black & White"
  }'
```

### Get All Orders
```bash
curl "http://localhost:8000/orders/"
```

### Get Specific Order
```bash
curl "http://localhost:8000/orders/550e8400-e29b-41d4-a716-446655440000"
```

## 📁 Project Structure

```
z/
├── main.py                 # FastAPI application (all logic in one file)
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## 🔧 Data Model

### Order Object

| Field | Type | Description |
|:--|:--|:--|
| `order_id` | string (UUID) | Unique identifier (auto-generated) |
| `customer_name` | string | Name of the customer placing the order |
| `document_name` | string | Name of the document being printed |
| `pages` | integer | Number of pages to print |
| `print_type` | string | Type of print (Black & White, Colored, Photo Paper) |
| `total_cost` | float | Total cost in PHP (auto-calculated) |
| `status` | string | Current status (default: "Pending") |

## ⚠️ Error Handling

The API returns appropriate HTTP status codes:

- **200 OK** - Successful GET request
- **201 Created** - Order successfully created
- **400 Bad Request** - Invalid print_type provided
- **404 Not Found** - Order ID does not exist

## 🎯 Use Cases

### Scenario 1: Peak Hour Order Entry
**Attendant**: "Add an order for Maria, printing 'Thesis.pdf', 150 pages, Black & White"
```bash
curl -X POST "http://localhost:8000/orders/" \
  -H "Content-Type: application/json" \
  -d '{
    "customer_name": "Maria",
    "document_name": "Thesis.pdf",
    "pages": 150,
    "print_type": "Black & White"
  }'
```
**System**: Automatically calculates PHP 300.00 and queues the order instantly.

### Scenario 2: Price Verification
**Customer**: "How much will 20 colored pages cost?"
```bash
# POST the order
curl -X POST "http://localhost:8000/orders/" \
  -H "Content-Type: application/json" \
  -d '{
    "customer_name": "Customer",
    "document_name": "Pages.pdf",
    "pages": 20,
    "print_type": "Colored"
  }'
```
**System**: Responds with total_cost of PHP 100.00.

### Scenario 3: Order Status Tracking
**Attendant**: "Check all pending orders"
```bash
curl "http://localhost:8000/orders/"
```
**System**: Returns complete queue of all active orders.

## 🛠️ Development Notes

- **Framework**: FastAPI (modern, fast, production-ready)
- **Server**: Uvicorn (ASGI server)
- **Data Validation**: Pydantic models with automatic validation
- **Storage**: In-memory dictionaries (resets on server restart)
- **API Documentation**: Auto-generated interactive docs at `/docs`

## 📝 Future Enhancements

Potential features for future iterations:
- Order cancellation endpoint
- Update order status (Moving from "Pending" → "Printing" → "Completed")
- Order statistics and reporting
- Discount system for bulk orders
- Customer history tracking
- Database persistence (SQLite, PostgreSQL)
- Authentication and role-based access control
- Order printing timeline tracking

## 📞 Support

For questions or issues, refer to the inline code comments in [main.py](main.py) or the API documentation at `http://localhost:8000/docs`.

---

**Version**: 1.0.0  
**Last Updated**: March 2026  
**License**: MIT
