# Delivery Application

This is a delivery application that connects buyers, sellers, and dispatchers. It gives back control to the sellers and provides easy access for buyers to purchase products.

## Features

- **User Authentication:** Secure login and registration for users.
- **Category Management:** Create, retrieve, update, and delete product categories.
- **Product Management:** Create, retrieve, update, delete, and manage products.
- **Order Management:** Place, track, and manage orders.
- **Payment Processing:** Handle payments, update payment status, and retrieve payment details.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/dominic-source/Home_Deliverer.git
    cd delivery_app
    ```
2. Set up a virtual environment:
    - ensure you are in the root directory of this repository
    ```bash
    python -m venv venv
    source venv/bin/activate
    ```
3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4. Set up the database:
    - Setup Redis server
    - Confirm redis status
        ```bash
        redis-cli PING
        ```
        It should output *PONG*
    - Setup mysql server
        ```bash
        sudo service mysql start
        ```
    - Confirm status of the mysql
        ```bash
        sudo service mysql status
        ```
    - Initialize the database migration:
        ```bash
        flask db init
        flask db migrate
        flask db upgrade
        ```
5. Create a new terminal and run consumer.py
    ```bash
        python -m flask_server.consumer
    ```

## Usage

1. Run the application:
    ```bash
    python -m flask_server.app
    ```
2. Access the application:
    - Open your web browser and navigate to http://127.0.0.2:5000.

## API Endpoints

### User API Endpoints

This module is used for user authentication and management. It includes the following endpoints:

#### User Registration

- **URL:** `/api/v1/user/register`
- **Method:** `POST`
- **Auth required:** No
- **Data Params:**
    - `username` (str): The desired username for the new user.
    - `password` (str): The desired password for the new user.
    - `email` (str): The email address of the new user.
    - `first_name` (str): The first name of the new user.
    - `last_name` (str): The last name of the new user.
    - `phone_number` (str): The phone number of the new user.
    - `role` (str): The role of the new user (e.g., 'buyer', 'seller', 'dispatcher').
- **Success Response:** 
    - `201 Created`:  `{"username": "username", "creation_date": "YYYY-MM-DD", "id": 123}`
- **Error Response:**
    - `400 Bad Request`:  `{"error": "Username already exists"}` or `{"error": "Invalid email format"}`
    - `500 Internal Server Error`:  `{"error": "An internal error occurred"}`

#### User Login

- **URL:** `/api/v1/user/login`
- **Method:** `POST`
- **Auth required:** No
- **Data Params:**
    - `username` (str): The username of the user.
    - `password` (str): The password of the user.
- **Success Response:**
    - `200 OK`:  `{"message": "Login successful", "token": "your_access_token"}`
- **Error Response:**
    - `401 Unauthorized`:  `{"error": "Invalid credentials"}`
    - `500 Internal Server Error`:  `{"error": "An internal error occurred"}`

#### User Logout

- **URL:** `/api/v1/user/logout`
- **Method:** `POST`
- **Auth required:** Yes
- **Data Params:** None
- **Success Response:**
    - `200 OK`:  `{"message": "Logout successful"}`
- **Error Response:**
    - `401 Unauthorized`:  `{"error": "Unauthorized"}`
    - `500 Internal Server Error`:  `{"error": "An internal error occurred"}`

#### Get User

- **URL:** `/api/v1/user/<int:id>`
- **Method:** `GET`
- **Auth required:** Yes
- **Data Params:** None
- **Success Response:**
    - `200 OK`:  `{"id": 123, "username": "username", "email": "email@example.com", "first_name": "First", "last_name": "Last", "phone_number": "1234567890", "role": "buyer", "creation_date": "YYYY-MM-DD"}`
- **Error Response:**
    - `401 Unauthorized`:  `{"error": "Unauthorized"}`
    - `404 Not Found`:  `{"error": "User not found"}`
    - `500 Internal Server Error`:  `{"error": "An internal error occurred"}`

#### Get All Users

- **URL:** `/api/v1/users`
- **Method:** `GET`
- **Auth required:** Yes
- **Data Params:** None
- **Success Response:**
    - `200 OK`:  `[{"id": 123, "username": "username", "email": "email@example.com", "first_name": "First", "last_name": "Last", "phone_number": "1234567890", "role": "buyer", "creation_date": "YYYY-MM-DD"}, ...]`
- **Error Response:**
    - `401 Unauthorized`:  `{"error": "Unauthorized"}`
    - `404 Not Found`:  `{"error": "No users found"}`
    - `500 Internal Server Error`:  `{"error": "An internal error occurred"}`

#### Update User

- **URL:** `/api/v1/user/<int:id>`
- **Method:** `PUT`
- **Auth required:** Yes
- **Data Params:**
    - `email` (str): The updated email address.
    - `first_name` (str): The updated first name.
    - `last_name` (str): The updated last name.
    - `phone_number` (str): The updated phone number.
- **Success Response:**
    - `200 OK`:  `{"message": "User updated successfully"}`
- **Error Response:**
    - `401 Unauthorized`:  `{"error": "Unauthorized"}`
    - `404 Not Found`:  `{"error": "User not found"}`
    - `500 Internal Server Error`:  `{"error": "An internal error occurred"}`

#### Update User Password

- **URL:** `/api/v1/user/password/<int:id>`
- **Method:** `PUT`
- **Auth required:** Yes
- **Data Params:**
    - `old_password` (str): The user's current password.
    - `new_password` (str): The new password.
- **Success Response:**
    - `200 OK`:  `{"message": "Password updated successfully"}`
- **Error Response:**
    - `401 Unauthorized`:  `{"error": "Unauthorized"}`
    - `404 Not Found`:  `{"error": "User not found"}`
    - `400 Bad Request`:  `{"error": "Incorrect old password"}`
    - `500 Internal Server Error`:  `{"error": "An internal error occurred"}`

#### Forgot Password

- **URL:** `/api/v1/user/password/forgot`
- **Method:** `POST`
- **Auth required:** No
- **Data Params:**
    - `email` (str): The user's email address.
- **Success Response:**
    - `200 OK`:  `{"message": "Password reset email sent"}`
- **Error Response:**
    - `404 Not Found`:  `{"error": "User not found"}`
    - `500 Internal Server Error`:  `{"error": "An internal error occurred"}`

### Payment API Endpoints

This document describes the API endpoints available in the `payment.py` module.

#### Update Payment

- **URL:** `/api/v1/payment/<int:id>`
- **Method:** `PUT`
- **Auth required:** Yes
- **Arguments:** `id` (int) - The ID of the payment to update.
- **Data Params:** `status` (str) - The new status of the payment.
- **Success Response:** `{'message': 'Payment has been updated successfully'}` with status code 200.
- **Error Response:** Various, including 401 Unauthorized and 500 Internal Server Error.

#### Create Payment

- **URL:** `/api/v1/payment`
- **Method:** `POST`
- **Auth required:** Yes
- **Data Params:** 
  - `payment_method` (str) - The method of payment.
  - `seller_amount` (float) - The amount to be paid to the seller.
  - `dispatcher_amount` (float) - The amount to be paid to the dispatcher.
  - `currency` (str) - The currency of the payment.
  - `order_id` (int) - The ID of the order the payment is for.
- **Success Response:** `{'message': 'Payment has been created successfully'}` with status code 201.
- **Error Response:** Various, including 401 Unauthorized and 500 Internal Server Error.

#### Get Payments

- **URL:** `/api/v1/payments/<int:order_id>`
- **Method:** `GET`
- **Auth required:** Yes
- **Arguments:** `order_id` (int) - The ID of the order to retrieve payments for.
- **Success Response:** A list of payment data with status code 200.
- **Error Response:** Various, including 401 Unauthorized and 500 Internal Server Error.

### Product API Endpoints

This module is used to manage the product. It provides several endpoints for creating, retrieving, updating, and deleting products.

#### Get Products by Category

- **URL:** `/api/v1/products/categories/<int:id>`
- **Method:** `GET`
- **Auth required:** No
- **Data Params:** None
- **Success Response:**
    - `200 OK`:  `[{"name": "Product Name 1"}, {"name": "Product Name 2"}, ...]`
- **Error Response:**
    - `400 Bad Request`:  `{"error": "Category ID is required"}`
    - `404 Not Found`:  `{"error": "Category not found"}`
    - `500 Internal Server Error`:  `{"error": "An internal error occurred"}`

#### Get Products by Category

- **URL:** `/api/v1/products/categories/<int:id>`
- **Method:** `GET`
- **Auth required:** Yes
- **Data Params:** None
- **Success Response:**
    - `200 OK`:  `[{"name": "Product Name 1"}, {"name": "Product Name 2"}, ...]`
- **Error Response:**
    - `400 Bad Request`:  `{"error": "Category ID is required"}`
    - `404 Not Found`:  `{"error": "Category not found"}` or `{"error": "No products found in this category"}`
    - `500 Internal Server Error`:  `{"error": "An internal error occurred"}`

#### Get Products by User

- **URL:** `/api/v1/products/users`
- **Method:** `GET`
- **Auth required:** Yes
- **Data Params:** None
- **Success Response:**
    - `200 OK`:  `[{"id": 123, "name": "Product Name", "description": "Product Description", "price": 100.00, "currency": "USD", "category_id": 456, "quantity": 10, "owner_username": "Seller Username", "creation_date": "YYYY-MM-DD", "last_update_time": "YYYY-MM-DD"}, ...]`
- **Error Response:**
    - `401 Unauthorized`:  `{"error": "Unauthorized"}`
    - `404 Not Found`:  `{"error": "No products found for this user"}`
    - `500 Internal Server Error`:  `{"error": "An internal error occurred"}`

#### Update Product

- **URL:** `/api/v1/product/<int:id>`
- **Method:** `PUT`
- **Auth required:** Yes
- **Data Params:**
    - `name` (str, optional): The updated name of the product.
    - `description` (str, optional): The updated description of the product.
    - `price` (float, optional): The updated price of the product.
    - `currency` (str, optional): The updated currency of the product.
    - `category_id` (int, optional): The updated category ID of the product.
    - `quantity` (int, optional): The updated quantity of the product.
- **Success Response:**
    - `200 OK`:  `{"message": "Product updated successfully"}`
- **Error Response:**
    - `400 Bad Request`:  `{"error": "Product ID is required"}`
    - `401 Unauthorized`:  `{"error": "Unauthorized"}`
    - `404 Not Found`:  `{"error": "Product not found"}`
    - `500 Internal Server Error`:  `{"error": "An internal error occurred"}`

#### Get All Products

- **URL:** `/api/v1/products`
- **Method:** `GET`
- **Auth required:** No
- **Data Params:** None
- **Success Response:**
    - `200 OK`:  `[{"id": 123, "name": "Product Name", "description": "Product Description", "price": 100.00, "currency": "USD", "category_id": 456, "quantity": 10, "owner_username": "Seller Username", "creation_date": "YYYY-MM-DD", "last_update_time": "YYYY-MM-DD"}, ...]`
- **Error Response:**
    - `404 Not Found`:  `{"error": "No products found"}`
    - `500 Internal Server Error`:  `{"error": "An internal error occurred"}`

#### Get Product

- **URL:** `/api/v1/product/<int:id>`
- **Method:** `GET`
- **Auth required:** No
- **Data Params:** None
- **Success Response:**
    - `200 OK`:  `{"id": 123, "name": "Product Name", "description": "Product Description", "price": 100.00, "currency": "USD", "category_id": 456, "quantity": 10, "owner_username": "Seller Username", "creation_date": "YYYY-MM-DD", "last_update_time": "YYYY-MM-DD"}`
- **Error Response:**
    - `400 Bad Request`:  `{"error": "Product ID is required"}`
    - `404 Not Found`:  `{"error": "Product not found"}`
    - `500 Internal Server Error`:  `{"error": "An internal error occurred"}`

#### Create Product

- **URL:** `/api/v1/product`
- **Method:** `POST`
- **Auth required:** Yes
- **Data Params:**
    - `name` (str): The name of the product.
    - `description` (str): The description of the product.
    - `price` (float): The price of the product.
    - `currency` (str): The currency of the product.
    - `category_id` (int): The ID of the category the product belongs to.
    - `quantity` (int): The quantity of the product.
- **Success Response:**
    - `201 Created`:  `{"id": 123, "name": "Product Name", "owner_username": "Seller Username"}`
- **Error Response:**
    - `400 Bad Request`:  `{"error": "Missing required parameters"}`
    - `401 Unauthorized`:  `{"error": "Unauthorized"}`
    - `404 Not Found`:  `{"error": "Category not found"}`
    - `500 Internal Server Error`:  `{"error": "An internal error occurred"}`

#### Delete Product

- **URL:** `/api/v1/product/<int:id>`
- **Method:** `DELETE`
- **Auth required:** Yes
- **Data Params:** None
- **Success Response:**
    - `200 OK`:  `{"message": "Product deleted successfully"}`
- **Error Response:**
    - `400 Bad Request`:  `{"error": "Product ID is required"}`
    - `401 Unauthorized`:  `{"error": "Unauthorized"}`
    - `404 Not Found`:  `{"error": "Product not found"}`
    - `500 Internal Server Error`:  `{"error": "An internal error occurred"}`

### Category API Endpoints

This module is used to manage categories in the application. It provides endpoints for creating, deleting, retrieving a single category, and retrieving all categories.

#### Delete Category

- **URL:** `/api/v1/category/<int:id>`
- **Method:** `DELETE`
- **Auth required:** Yes (Admin)
- **Data Params:** None
- **Success Response:**
    - `200 OK`:  `{"message": "Category deleted successfully"}`
- **Error Response:**
    - `400 Bad Request`:  `{"error": "Category ID is required"}`
    - `404 Not Found`:  `{"error": "Category not found"}`
    - `500 Internal Server Error`:  `{"error": "An internal error occurred"}`

#### Create Category

- **URL:** `/api/v1/category`
- **Method:** `POST`
- **Auth required:** Yes (Admin)
- **Data Params:**
    - `name` (str): The name of the category to create.
- **Success Response:**
    - `201 Created`:  `{"name": "Category Name", "id": 123}`
- **Error Response:**
    - `400 Bad Request`:  `{"error": "Category name must be provided"}`
    - `500 Internal Server Error`:  `{"error": "An internal error occurred"}`

#### Get All Categories

- **URL:** `/api/v1/categories`
- **Method:** `GET`
- **Auth required:** Yes
- **Data Params:** None
- **Success Response:**
    - `200 OK`:  `[{"id": 123, "name": "Category Name"}, ...]`
- **Error Response:**
    - `404 Not Found`:  `{"error": "No categories found"}`
    - `500 Internal Server Error`:  `{"error": "An internal error occurred"}`

#### Get Category

- **URL:** `/api/v1/category/<int:id>`
- **Method:** `GET`
- **Auth required:** Yes
- **Data Params:** None
- **Success Response:**
    - `200 OK`:  `{"id": 123, "name": "Category Name"}`
- **Error Response:**
    - `400 Bad Request`:  `{"error": "Category ID is required"}`
    - `404 Not Found`:  `{"error": "Category not found"}`
    - `500 Internal Server Error`:  `{"error": "An internal error occurred"}`


### Order API Endpoints

This module is used to manage orders in the application. It provides endpoints for creating, retrieving, updating, and deleting orders.

#### Create Order

- **URL:** `/api/v1/order`
- **Method:** `POST`
- **Auth required:** Yes
- **Data Params:**
    - `seller_id` (int): The ID of the seller fulfilling the order.
    - `dispatcher_id` (int): The ID of the dispatcher assigned to the order.
    - `delivery_address` (str): The delivery address of the order.
    - `orderitems` (list): A list of dictionaries, each containing:
        - `product_id` (int): The ID of the product being ordered.
        - `quantity` (int): The quantity of the product being ordered.
- **Success Response:** 
    - `201 Created`:  `{"order_id": 123}`
- **Error Response:**
    - `401 Unauthorized`:  `{"error": "This route requires you use json"}` or `{"error": "Seller not found"}` or `{"error": "Dispatcher not found"}` or `{"error": "Product not found"}`
    - `500 Internal Server Error`:  `{"error": "An internal error occurred!"}`

#### Get All Orders (Admin Only)

- **URL:** `/api/v1/all_orders`
- **Method:** `GET`
- **Auth required:** Yes (Admin)
- **Data Params:** None
- **Success Response:**
    - `200 OK`:  `[{"id": 123, "product_name": "Product Name", "buyer_username": "Buyer Username", "seller_username": "Seller Username", "dispatcher_username": "Dispatcher Username", "status": "pending", "total_amount": 100.00, "currency": "USD", "delivery_address": "123 Main St", "creation_date": "YYYY-MM-DD", "last_update_time": "YYYY-MM-DD"}, ...]`
- **Error Response:**
    - `401 Unauthorized`:  `{"error": "Unauthorized"}`
    - `500 Internal Server Error`:  `{"error": "An internal error occurred!"}`

#### Get My Orders

- **URL:** `/api/v1/my_orders`
- **Method:** `GET`
- **Auth required:** Yes
- **Data Params:**
    - `seller` (str, optional): If 'true', returns orders where the user is the seller.
    - `buyer` (str, optional): If 'true', returns orders where the user is the buyer.
    - `dispatcher` (str, optional): If 'true', returns orders where the user is the dispatcher.
- **Success Response:**
    - `200 OK`:  `{"buyer": [{"id": 123, "product_name": "Product Name", "buyer_username": "Buyer Username", "seller_username": "Seller Username", "dispatcher_username": "Dispatcher Username", "status": "pending", "total_amount": 100.00, "currency": "USD", "delivery_address": "123 Main St", "creation_date": "YYYY-MM-DD", "last_update_time": "YYYY-MM-DD"}, ...], "seller": [...], "dispatcher": [...]}`
- **Error Response:**
    - `401 Unauthorized`:  `{"error": "Unauthorized"}`
    - `500 Internal Server Error`:  `{"error": "An internal error occurred!"}`

#### Get Order Items

- **URL:** `/api/v1/order_items/<id>`
- **Method:** `GET`
- **Auth required:** Yes (Buyer, Seller, or Dispatcher)
- **Data Params:** None
- **Success Response:**
    - `200 OK`:  `[{"id": 123, "product_id": 456, "quantity": 2}, ...]`
- **Error Response:**
    - `400 Bad Request`:  `{"error": "Valid order ID is required"}`
    - `404 Not Found`:  `{"error": "Order not found"}`
    - `500 Internal Server Error`:  `{"error": "An internal error occurred!"}`

#### Get Order

- **URL:** `/api/v1/order/<int:id>`
- **Method:** `GET`
- **Auth required:** Yes (Buyer, Seller, or Dispatcher)
- **Data Params:** None
- **Success Response:**
    - `200 OK`:  `{"id": 123, "product_name": "Product Name", "buyer_username": "Buyer Username", "seller_username": "Seller Username", "dispatcher_username": "Dispatcher Username", "status": "pending", "total_amount": 100.00, "currency": "USD", "delivery_address": "123 Main St", "creation_date": "YYYY-MM-DD", "last_update_time": "YYYY-MM-DD"}`
- **Error Response:**
    - `401 Unauthorized`:  `{"error": "Unauthorized"}`
    - `404 Not Found`:  `{"error": "Order not found"}`
    - `500 Internal Server Error`:  `{"error": "An internal error occurred!"}`

#### Update Order Items

- **URL:** `/api/v1/order/<int:order_id>`
- **Method:** `PUT`
- **Auth required:** Yes (Buyer or Seller)
- **Data Params:**
    - `orderitems` (list): A list of dictionaries, each containing:
        - `id` (int): The ID of the order item.
        - `quantity` (int): The new quantity of the order item.
- **Success Response:**
    - `200 OK`:  `{"message": "Order item was updated successfully"}`
- **Error Response:**
    - `400 Bad Request`:  `{"error": "Order ID is required"}` or `{"error": "This route requires JSON input"}` or `{"error": "Order item not found"}` or `{"error": "Order item does not belong to this order"}`
    - `403 Forbidden`:  `{"error": "Unauthorized transaction"}` or `{"error": "Order has already been paid"}`
    - `404 Not Found`:  `{"error": "Order not found"}`
    - `415 Unsupported Media Type`:  `{"error": "This route requires JSON input"}`
    - `500 Internal Server Error`:  `{"error": "An internal error occurred"}`

#### Update Order Address

- **URL:** `/api/v1/order`
- **Method:** `PUT`
- **Auth required:** Yes (Buyer)
- **Data Params:**
    - `order_id` (int): The ID of the order to update.
    - `delivery_address` (str, optional): The new delivery address of the order.
- **Success Response:**
    - `200 OK`:  `{"message": "Order updated successfully"}`
- **Error Response:**
    - `400 Bad Request`:  `{"error": "Valid order ID is required"}`
    - `403 Forbidden`:  `{"error": "Unauthorized transaction"}`
    - `404 Not Found`:  `{"error": "Order not found"}`
    - `500 Internal Server Error`:  `{"error": "An internal error occurred"}`

#### Delete Order Item

- **URL:** `/api/v1/order/<int:order_id>/<int:orderitem_id>`
- **Method:** `DELETE`
- **Auth required:** Yes (Buyer or Seller)
- **Data Params:** None
- **Success Response:**
    - `200 OK`:  `{"message": "Order item was deleted successfully"}`
- **Error Response:**
    - `400 Bad Request`:  `{"error": "Order ID is required"}` or `{"error": "Order item ID is required"}` or `{"error": "Order item does not belong to this order"}`
    - `403 Forbidden`:  `{"error": "Unauthorized transaction"}` or `{"error": "Order has already been paid"}` or `{"error": "Order is in process of payment"}`
    - `404 Not Found`:  `{"error": "Order not found"}` or `{"error": "Order item not found"}`
    - `500 Internal Server Error`:  `{"error": "An internal error occurred"}`

#### Delete Order

- **URL:** `/api/v1/order/<int:order_id>`
- **Method:** `DELETE`
- **Auth required:** Yes (Buyer or Seller)
- **Data Params:** None
- **Success Response:**
    - `200 OK`:  `{"message": "Order was deleted successfully"}`
- **Error Response:**
    - `400 Bad Request`:  `{"error": "Order ID is required"}`
    - `403 Forbidden`:  `{"error": "Unauthorized transaction"}` or `{"error": "Order has already been paid"}` or `{"error": "Order is in process of payment"}`
    - `404 Not Found`:  `{"error": "Order not found"}`
    - `500 Internal Server Error`:  `{"error": "An internal error occurred"}`

### Please consult [Postman collection][def] documentation for further information.

## Helper Functions

### Decorators

- **Admin Route:** Ensures only admins can access certain routes.
- **Protected Route:** Ensures routes are protected and require user login.

### Utility Functions

- **Generate Orders:** Generates a list of order dictionaries from order objects.

## Logging

Logs are stored in consumer.log with detailed information for debugging and tracking.


[def]: https://cloudy-moon-908583.postman.co/workspace/My-Workspace~4f4a4cc1-9615-410e-853e-d6b06888db33/api/30b69cb8-0e6c-4978-b53e-994e8e891313/collection/12957307-3e2a472e-6662-4031-b4f9-96b8ad8b5c4a?branch=master