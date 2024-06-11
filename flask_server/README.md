# Delivery Application

This is a delivery application that connects buyers, sellers, and dispatchers. It gives back control to the sellers and provides easy access for buyers to purchase products.

## Features

- **User Authentication:** Secure login and registration for users.
- **Category Management:** Create, retrieve, update, and delete product categories.
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
    python3 -m venv venv
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

This module is used for user authentication and management. It includes the following functions:

- **get_user():** GET /api/v1/user/<int:id>
    - Retrieve the basic information of a user. Returns a JSON response containing the user's information and status code if the retrieval is successful, or an error message and status code if the retrieval fails.
- **get_users():** GET /api/v1/users
    - Retrieve all users of the software. Returns a JSON response containing a list of users and status code if the retrieval is successful, or an error message and status code if the retrieval fails.
- **update_password():** PUT /api/v1/user/password/<int:id>
    - Update a user's password. Returns a JSON response containing a success message and status code if the password update is successful, or an error message and status code if the password update fails.
- **forgot_password():** POST /api/v1/user/password/forgot
    - Generate a token for a user who forgot their password. Returns a JSON response containing a success message and status code if the token is generated successfully, or an error message and status code if the token generation fails.
- **update_user():** PUT /api/v1/user/<int:id>
    - Update a user's information. Returns a JSON response containing a success message and status code if the update is successful, or an error message and status code if the update fails.
- **logout_user():** POST /api/v1/user/logout
    - Log out a user. Returns a success message and status code if the logout is successful, or an error message and status code if the logout fails.
- **login_user():** POST /api/v1/user/login
    - Log in a user. Returns a success message and status code if the login is successful, or an error message and status code if the login fails.
- **register():** POST /api/v1/user/register
    - Register a new user. Returns a JSON response containing the new user's username, creation date, and ID, or an error message, and a status code.


### Payment API Endpoints

This document describes the API endpoints available in the `payment.py` module.

#### Update Payment

- **URL:** `/payment/<int:id>`
- **Method:** `PUT`
- **Auth required:** Yes
- **Arguments:** `id` (int) - The ID of the payment to update.
- **Data Params:** `status` (str) - The new status of the payment.
- **Success Response:** `{'message': 'Payment has been updated successfully'}` with status code 200.
- **Error Response:** Various, including 401 Unauthorized and 500 Internal Server Error.

#### Create Payment

- **URL:** `/payment`
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

- **URL:** `/payments/<int:order_id>`
- **Method:** `GET`
- **Auth required:** Yes
- **Arguments:** `order_id` (int) - The ID of the order to retrieve payments for.
- **Success Response:** A list of payment data with status code 200.
- **Error Response:** Various, including 401 Unauthorized and 500 Internal Server Error.

### Product API Endpoints

This module is used to manage the product. It provides several endpoints for creating, retrieving, updating, and deleting products.


#### GET /products/categories/<int:id>

This endpoint retrieves all unique product names in a specific category.

- **Parameters**: `id` (int) - The ID of the category.
- **Returns**: A JSON response containing the product names or an error message, and a status code.
- **Errors**: 400 (Bad Request) if the category ID is not provided, 404 (Not Found) if no products exist in the category, 500 (Internal Server Error) if an internal error occurs.

#### GET /products/users

This endpoint retrieves all products associated with the current user.

- **Returns**: A JSON response containing the product data or an error message, and a status code.
- **Errors**: 404 (Not Found) if the user does not exist or has no products, 500 (Internal Server Error) if an internal error occurs.

#### PUT /product/<int:id>

This endpoint updates a product by its ID.

- **Parameters**: `id` (int) - The ID of the product to update.
- **Returns**: A JSON response containing the updated product data or an error message, and a status code.
- **Errors**: 400 (Bad Request) if the product ID is not provided, 404 (Not Found) if the product does not exist, 500 (Internal Server Error) if an internal error occurs.

#### GET /products

This endpoint retrieves all products.

- **Returns**: A JSON response containing the product data or an error message, and a status code.
- **Errors**: 404 (Not Found) if no products exist, 500 (Internal Server Error) if an internal error occurs.

#### GET /product/<int:id>

This endpoint retrieves a product by its ID.

- **Parameters**: `id` (int) - The ID of the product to retrieve.
- **Returns**: A JSON response containing the product data or an error message, and a status code.
- **Errors**: 400 (Bad Request) if the product ID is not provided, 404 (Not Found) if the product does not exist, 500 (Internal Server Error) if an internal error occurs.

#### POST /product

This endpoint creates a product.

- **Parameters**: `name` (str) - The name of the product, `description` (str) - The description of the product, `price` (float) - The price of the product, `currency` (str) - The currency of the product, `category_id` (int) - The ID of the category the product belongs to, `quantity` (int) - The quantity of the product.
- **Returns**: A JSON response containing the product ID, name, and owner's username, or an error message, and a status code.
- **Errors**: 401 (Unauthorized) if an error occurs during creation, 500 (Internal Server Error) if an internal error occurs.

#### DELETE /product/<int:id>

This endpoint deletes a product.

- **Parameters**: `id` (int) - The ID of the product to delete.
- **Returns**: A JSON response containing a success message or an error message, and a status code.
- **Errors**: 401 (Unauthorized) if the product ID is not provided or the product does not exist, 500 (Internal Server Error) if an error occurs during deletion.




### Category API Endpoints

This module is used to manage categories in the application. It provides endpoints for creating, deleting, retrieving a single category, and retrieving all categories.


#### DELETE /category/<int:id>

This endpoint deletes a category.

- **Parameters**: `id` (int) - The ID of the category to delete.
- **Returns**: A JSON response containing a success message or an error message, and a status code.
- **Errors**: 
  - 400 (Bad Request) if the category ID is not provided,
  - 404 (Not Found) if the category does not exist,
  - 500 (Internal Server Error) if an error occurs during deletion.

#### POST /category

This endpoint creates a category.

- **Parameters**: `name` (str) - The name of the category to create.
- **Returns**: A JSON response containing the name and ID of the created category, or an error message, and a status code.
- **Errors**: 
  - 400 (Bad Request) if the category name is not provided,
  - 500 (Internal Server Error) if an error occurs during creation.

#### GET /categories

This endpoint retrieves all categories.

- **Returns**: A JSON response containing a list of categories or an error message, and a status code.
- **Errors**: 
  - 404 (Not Found) if no categories exist,
  - 500 (Internal Server Error) if an error occurs during retrieval.

#### GET /category/<int:id>

This endpoint retrieves a particular category by its ID.

- **Parameters**: `id` (int) - The ID of the category to retrieve.
- **Returns**: A JSON response containing the category data or an error message, and a status code.
- **Errors**: 
  - 400 (Bad Request) if the category ID is not provided,
  - 404 (Not Found) if the category does not exist,
  - 500 (Internal Server Error) if an error occurs during retrieval.


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