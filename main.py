"""
DaliPrint API - Local Print Shop Order Management System
A FastAPI backend application for managing print orders with automated cost calculation.
"""

from enum import Enum
from fastapi import FastAPI, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict


# ============================================================================
# ENUMS
# ============================================================================

class PrintType(str, Enum):
    """Print type options for the dropdown."""
    BLACK_WHITE = "Black & White"
    COLORED = "Colored"
    PHOTO_PAPER = "Photo Paper"


class OrderStatus(str, Enum):
    """Order status options."""
    PENDING = "Pending"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"

# Initialize FastAPI application
app = FastAPI(
    title="DaliPrint API",
    description="Print Shop Order Management System",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================================
# IN-MEMORY DATABASE
# ============================================================================
# Using a dictionary to store orders: {order_id: order_data}
orders_db: Dict[str, dict] = {}
order_counter = 1


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def generate_order_id() -> str:
    """Generate a sequential order ID like 2025-000001."""
    global order_counter
    from datetime import datetime
    year = datetime.now().year
    order_id = f"{year}-{order_counter:06d}"
    order_counter += 1
    return order_id

# ============================================================================
# PYDANTIC MODELS
# ============================================================================

class Order(BaseModel):
    """Order model with all required fields."""
    order_id: str
    customer_name: str
    document_name: str
    pages: int
    print_type: str
    total_cost: float
    status: str = "Pending"


class OrderRequest(BaseModel):
    """Request model for creating a new order (excludes auto-generated fields)."""
    customer_name: str
    document_name: str
    pages: int
    print_type: PrintType


# ============================================================================
# PRICING CONFIGURATION
# ============================================================================
PRICING_RATES = {
    "Black & White": 2.00,  # PHP per page
    "Colored": 5.00,        # PHP per page
    "Photo Paper": 20.00    # PHP per page
}


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def calculate_cost(print_type: str, pages: int) -> float:
    """
    Calculate the total cost based on print type and number of pages.
    
    Args:
        print_type: Type of printing (must be a key in PRICING_RATES)
        pages: Number of pages to print
        
    Returns:
        float: Total cost in PHP
        
    Raises:
        ValueError: If print_type is not valid
    """
    if print_type not in PRICING_RATES:
        raise ValueError(f"Invalid print type: {print_type}")
    return PRICING_RATES[print_type] * pages


# ============================================================================
# ENDPOINTS
# ============================================================================

@app.post("/orders/", response_model=Order, status_code=201)
def create_order(
    customer_name: str = Form(...),
    document_name: str = Form(...),
    pages: int = Form(...),
    print_type: PrintType = Form(...)
):
    """
    Create a new print order.
    
    - Accepts: customer_name, document_name, pages, print_type
    - Automatically generates: order_id (UUID), total_cost
    - Sets default status: "Pending"
    - Stores the order in the in-memory database
    
    Args:
        order_request: OrderRequest containing order details
        
    Returns:
        Order: The created order with all details
        
    Raises:
        HTTPException 400: If print_type is invalid
    """
    # Validate print_type
    print_type_value = print_type.value if isinstance(print_type, PrintType) else print_type
    if print_type_value not in PRICING_RATES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid print type. Must be one of: {', '.join(PRICING_RATES.keys())}"
        )
    
    # Check for duplicate order
    for existing in orders_db.values():
        if (existing["customer_name"] == customer_name and
            existing["document_name"] == document_name and
            existing["pages"] == pages and
            existing["print_type"] == print_type_value and
            existing["status"] == "Pending"):
            raise HTTPException(
                status_code=400,
                detail="Duplicate pending order already exists"
            )
    
    # Generate unique order_id (sequential format: 2025-000001)
    order_id = generate_order_id()
    
    # Calculate total cost using business logic
    total_cost = calculate_cost(print_type_value, pages)
    
    # Create the order object
    order = {
        "order_id": order_id,
        "customer_name": customer_name,
        "document_name": document_name,
        "pages": pages,
        "print_type": print_type,
        "total_cost": total_cost,
        "status": "Pending"
    }
    
    # Store in in-memory database
    orders_db[order_id] = order
    
    return order


@app.get("/orders/", response_model=List[Order])
def get_all_orders():
    """
    Retrieve all orders currently in the system.
    
    Returns:
        List[Order]: A list of all created orders
    """
    return list(orders_db.values())


@app.get("/orders/{order_id}", response_model=Order)
def get_order(order_id: str):
    """
    Retrieve a specific order by its ID.
    
    Args:
        order_id: The unique identifier of the order (UUID)
        
    Returns:
        Order: The order details
        
    Raises:
        HTTPException 404: If the order_id does not exist
    """
    if order_id not in orders_db:
        raise HTTPException(
            status_code=404,
            detail=f"Order with ID {order_id} not found"
        )
    
    return orders_db[order_id]


@app.patch("/orders/{order_id}/status", response_model=Order)
def update_order_status(order_id: str, status: OrderStatus = Form(...)):
    """
    Update the status of an order.
    
    Args:
        order_id: The unique identifier of the order
        status: New status (Pending, Completed, Cancelled)
        
    Returns:
        Order: The updated order
        
    Raises:
        HTTPException 404: If the order_id does not exist
    """
    if order_id not in orders_db:
        raise HTTPException(
            status_code=404,
            detail=f"Order with ID {order_id} not found"
        )
    
    orders_db[order_id]["status"] = status.value
    return orders_db[order_id]


@app.delete("/orders/{order_id}")
def delete_order(order_id: str):
    """
    Delete an order from the queue.
    
    Args:
        order_id: The unique identifier of the order
        
    Returns:
        dict: Success message
        
    Raises:
        HTTPException 404: If the order_id does not exist
    """
    if order_id not in orders_db:
        raise HTTPException(
            status_code=404,
            detail=f"Order with ID {order_id} not found"
        )
    
    del orders_db[order_id]
    return {"message": f"Order {order_id} deleted successfully"}


@app.get("/")
def root():
    """Root endpoint - returns welcome message."""
    return {"message": "Welcome to DaliPrint API! Please navigate to /docs to view and test the endpoints."}


# ============================================================================
# ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    
    # Run the FastAPI application on localhost:8000
    # Access API documentation at: http://localhost:8000/docs (Swagger UI)
    # Alternative API docs:          http://localhost:8000/redoc (ReDoc)
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
