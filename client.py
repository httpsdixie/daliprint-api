#!/usr/bin/env python3
"""
DaliPrint Terminal Client
A command-line interface for interacting with the DaliPrint API.

Usage:
    python client.py view                                          - List all orders
    python client.py search <order_id>                             - Search order by ID
    python client.py order <customer> <document> <pages> <type>   - Create a new order
    python client.py status <order_id> <status>                    - Update order status
    python client.py delete <order_id>                             - Delete an order

Print Types: "Black & White", "Colored", "Photo Paper"
Statuses:    "Pending", "Completed", "Cancelled"
"""

import sys
import requests

BASE_URL = "http://127.0.0.1:8000"


def view():
    """List all orders from the API."""
    print("\n=== List of Orders ===")
    response = requests.get(f"{BASE_URL}/orders/")

    if response.status_code == 200:
        orders = response.json()
        if not orders:
            print("No orders found.")
            return
        for idx, order in enumerate(orders):
            print(f"\n[{idx}] Order ID   : {order['order_id']}")
            print(f"     Customer   : {order['customer_name']}")
            print(f"     Document   : {order['document_name']}")
            print(f"     Print Type : {order['print_type']}")
            print(f"     Pages      : {order['pages']}")
            print(f"     Total Cost : PHP {order['total_cost']:.2f}")
            print(f"     Status     : {order['status']}")
    else:
        print(f"Fetch error: {response.status_code}")


def search(args):
    """Search for a specific order by ID."""
    if len(args) < 3:
        print("Usage: python client.py search <order_id>")
        return

    order_id = args[2]
    print(f"\n=== Search Order: {order_id} ===")
    response = requests.get(f"{BASE_URL}/orders/{order_id}")

    if response.status_code == 200:
        order = response.json()
        print(f"Order ID   : {order['order_id']}")
        print(f"Customer   : {order['customer_name']}")
        print(f"Document   : {order['document_name']}")
        print(f"Print Type : {order['print_type']}")
        print(f"Pages      : {order['pages']}")
        print(f"Total Cost : PHP {order['total_cost']:.2f}")
        print(f"Status     : {order['status']}")
    elif response.status_code == 404:
        print("Not found.")
    else:
        print(f"Error: {response.json().get('detail', 'Unknown error')}")


def order(args):
    """Create a new print order."""
    if len(args) < 6:
        print('Usage: python client.py order <customer_name> <document_name> <pages> <print_type>')
        print('Print types: "Black & White", "Colored", "Photo Paper"')
        return

    customer_name = args[2]
    document_name = args[3]
    pages         = args[4]
    print_type    = args[5]

    try:
        pages = int(pages)
    except ValueError:
        print("Invalid pages: must be a number.")
        return

    data = {
        "customer_name": customer_name,
        "document_name": document_name,
        "pages":         pages,
        "print_type":    print_type,
    }

    response = requests.post(f"{BASE_URL}/orders/", data=data)

    if response.status_code == 201:
        result = response.json()
        print("\nOrder completed!")
        print(f"Order ID   : {result['order_id']}")
        print(f"Customer   : {result['customer_name']}")
        print(f"Document   : {result['document_name']}")
        print(f"Print Type : {result['print_type']}")
        print(f"Pages      : {result['pages']}")
        print(f"Total Cost : PHP {result['total_cost']:.2f}")
        print(f"Status     : {result['status']}")
    else:
        print(f"Order not processed: {response.json().get('detail', 'Unknown error')}")


def status(args):
    """Update the status of an existing order."""
    if len(args) < 4:
        print("Usage: python client.py status <order_id> <status>")
        print("Statuses: Pending, Completed, Cancelled")
        return

    order_id   = args[2]
    new_status = args[3]

    response = requests.patch(f"{BASE_URL}/orders/{order_id}/status", data={"status": new_status})

    if response.status_code == 200:
        result = response.json()
        print(f"Order {order_id} status updated to: {result['status']}")
    elif response.status_code == 404:
        print("Order not found.")
    else:
        print(f"Error: {response.json().get('detail', 'Unknown error')}")


def delete(args):
    """Delete an order by ID."""
    if len(args) < 3:
        print("Usage: python client.py delete <order_id>")
        return

    order_id = args[2]
    response = requests.delete(f"{BASE_URL}/orders/{order_id}")

    if response.status_code == 200:
        print(f"Order {order_id} deleted successfully.")
    elif response.status_code == 404:
        print("Order not found.")
    else:
        print(f"Error: {response.json().get('detail', 'Unknown error')}")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return

    command = sys.argv[1]

    if command == "view":
        view()
    elif command == "order":
        order(sys.argv)
    elif command == "search":
        search(sys.argv)
    elif command == "status":
        status(sys.argv)
    elif command == "delete":
        delete(sys.argv)
    else:
        print(f"Invalid command: '{command}'")
        print(__doc__)


if __name__ == "__main__":
    main()
