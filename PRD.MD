DaliPrint API 

1. Project Overview
The DaliPrint API is an automated digital management system built as the backend brain for a local printing business. Developed using FastAPI and Python, this system operates as a purely in-memory solution to manage the workflow of printing tasks—from initial order reception to final cost calculation. Imagine a local print shop during a busy afternoon rush. A line of customers is waiting, and the shop attendant is struggling to keep track of names, file types, and page counts using a manual paper log. In this high-pressure environment, the attendant often makes mistakes in counting or calculating prices. DaliPrint solves this by providing a terminal-based API where the attendant inputs order details as Key:Value pairs. The system then automatically organizes the queue and computes the exact price, allowing the shop to function smoothly and professionally without the need for a physical database or paper records.

2. Problem Statement
The client faces critical operational challenges because their current manual workflow is inefficient:
Manual Recording: Recording orders by hand is slow and creates bottlenecks during peak hours.
Calculation Errors: Manually computing prices for various print types (Black & White vs. Colored) leads to frequent math mistakes and lost revenue.
Lost or Duplicated Orders: Without a digital queue, physical notes are easily lost, and files are sometimes printed twice by mistake, wasting expensive resources.

3. Objectives
The goal of this API is to digitize the business logic to ensure accuracy and efficiency:
Accept Printing Orders: Provide a structured way to record customer names and document requirements digitally.
Automated Cost Computation: Eliminate human error by calculating totals based on these fixed rates: Black & White: PHP 2.00/page, Colored: PHP 5.00/page,Photo Paper: PHP 20.00/page
Queue Management: Maintain an organized list of all active orders to ensure a fair "first-come, first-served" service.
Information Retrieval: Allow the attendant to pull up specific order details and prices instantly to finalize transactions.

4. Users
The system serves three distinct roles:
The Owner: The business stakeholder who needs accurate cost tracking to prevent financial loss and ensure the shop remains profitable.
The Attendant: The operator who interacts with the API terminal to manage the queue and verify pricing so they can focus on printing tasks.
The Customer: The individual who provides the order data (name and file details) to be officially queued, ensuring their request is processed accurately and in order.
