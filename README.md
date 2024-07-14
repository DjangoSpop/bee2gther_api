api # API Endpoints Summary

## Users
- POST /api/users/register/ - Register a new user
- POST /api/users/login/ - User login
- GET /api/users/profile/ - Get user profile
- PUT /api/users/profile/ - Update user profile

## Products
- GET /api/products/ - List all products
- POST /api/products/ - Create a new product (seller only)
- GET /api/products/{id}/ - Retrieve a specific product
- PUT /api/products/{id}/ - Update a product (seller only)
- PATCH /api/products/{id}/ - Partially update a product (seller only)
- DELETE /api/products/{id}/ - Delete a product (seller only)

## Group Buys`
- GET /api/group-buys/ - List all group buys
- POST /api/group-buys/ - Create a new group buy
- GET /api/group-buys/{id}/ - Retrieve a specific group buy
- PUT /api/group-buys/{id}/ - Update a group buy
- PATCH /api/group-buys/{id}/ - Partially update a group buy
- DELETE /api/group-buys/{id}/ - Delete a group buy
- POST /api/group-buys/{id}/join/ - Join a group buy
GET /api/groupbuys/: List all group buys
POST /api/groupbuys/: Create a new group buy
GET /api/groupbuys/{id}/: Retrieve a specific group buy
PUT /api/groupbuys/{id}/: Update a specific group buy
DELETE /api/groupbuys/{id}/: Delete a specific group buy
POST /api/groupbuys/{id}/join/: Join a specific group buy
GET /api/groupbuys/{id}/participants/: List participants of a specific group buy

## Orders
- GET /api/orders/ - List user's orders
- POST /api/orders/ - Create a new order
- GET /api/orders/{id}/ - Retrieve a specific order
- PUT /api/orders/{id}/ - Update an order
- PATCH /api/orders/{id}/ - Partially update an order
- DELETE /api/orders/{id}/ - Delete an order# bee2gther_api

