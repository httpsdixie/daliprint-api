# DaliPrint API

A FastAPI-based backend system for managing print shop orders with automated cost calculation.

## Features

- **Automated Cost Calculation** - PHP 2/5/20 per page based on print type
- **Sequential Order IDs** - Format: 2026-000001
- **Duplicate Prevention** - Rejects identical pending orders
- **Order Status Management** - Pending, Completed, Cancelled
- **Queue Management** - View, update, and delete orders

## Quick Start

```bash
pip install -r requirements.txt
python main.py
```

- API: http://localhost:8000
- Docs: http://localhost:8000/docs

## Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/orders/` | Create new order |
| GET | `/orders/` | Get all orders |
| GET | `/orders/{id}` | Get specific order |
| PATCH | `/orders/{id}/status` | Update order status |
| DELETE | `/orders/{id}` | Delete order |

## Pricing

| Print Type | Rate |
|------------|------|
| Black & White | PHP 2.00/page |
| Colored | PHP 5.00/page |
| Photo Paper | PHP 20.00/page |

## Example

```bash
# Create order
curl -X POST "http://localhost:8000/orders/" \
  -F "customer_name=John" \
  -F "document_name=Resume.pdf" \
  -F "pages=10" \
  -F "print_type=Colored"

# Update status
curl -X PATCH "http://localhost:8000/orders/2026-000001/status" \
  -F "status=Completed"
```

**Version**: 1.0.0