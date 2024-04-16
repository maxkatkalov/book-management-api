# Book Management API 

Book Management API  was created for the purpose of testing coding skills for VRB Tech company.

## Table of Contents

- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [DB scheme](https://monosnap.com/file/rLG56LIZWY1h6Rsa29PjaRvvL2Jrqc)
- [Online demo](#online-demo)
- [User permissions](#user-permissions)

## Getting Started

These instruction will help you get a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Python 3 must be installed on your machine.
- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

### Online demo

- You can access the online project demo [here](http://54.175.70.18/).


- For exploring the API endpoints, access the documentation:

  - [Swagger](http://54.175.70.18/docs/)
  - [Redoc](http://54.175.70.18/redoc/)

### Installation

1. Clone the repository:

   ```shell
   git clone -b develop https://github.com/maxkatkalov/book-management-api.git

2. Navigate to the cloned repository:

   ```shell
   cd book-management-api

3. Create a .env file and configure the environment variables required by your project. You can use the provided .env.example as a starting point.

   ```shell
   cp .env.example .env

4. Start the Docker daemon on your machine. Build and start the Docker containers:

   ```shell
   docker-compose up --build
   
6. Access the application in your web browser at http://127.0.0.1/

7. Usage exeamples:

Authors
- Retrieve All Authors
  - URL: /authors/
  - Method: GET
  - Description: Retrieve a list of all authors. 
  - Example Request/Response:
    - GET /authors/ HTTP/1.1:
     - [
    {
      "first_name": "string",
      "last_name": "string",
      "id": 0
    }
    ]

- Create Author
  - URL: /authors/
  - Method: POST
  - Description: Create a new author.
  - Example Request/Response:
    - POST /authors/ HTTP/1.1
    - {
  "first_name": "Alice",
  "last_name": "Johnson"
}
- Retrieve Author by ID
  - URL: /authors/{author_id}/
  - Method: GET
  - Description: Retrieve details of a specific author by ID.
  - Example Request/Response:
    - GET /authors/3/ HTTP/1.1
    - {
  "id": 3,
  "first_name": "Alice",
  "last_name": "Johnson",
}
- Update Author
  - URL: /authors/{author_id}/
  - Method: PUT
  - Description: Update details of an existing author by ID.
  - Example Request/Response:
    - PUT /authors/3/ HTTP/1.1
    - {
  "first_name": "Alice",
  "last_name": "Smith"
}
- Delete Author
  - URL: /authors/{author_id}/
  - Method: DELETE
  - Description: Delete an author by ID.
  - Example Request/Response:
    - DELETE /authors/3/ HTTP/1.1
    - {
  "message": "Author deleted successfully"
}

Books:

- Retrieve All Books
  - URL: /books/
  - Method: GET
  - Description: Retrieve a list of all books or filter by title, publish date, or author ID.
  - Query Parameters:
  - title (optional): Filter books by title.
  - publish_date (optional): Filter books by publish date (YYYY-MM-DD format).
  - author_id (optional): Filter books by author ID.
  - Example Request/Response:
    - GET /books/?title=Sample Book&publish_date=2022-01-01&author_id=1 HTTP/1.1
    - [
{
"title": "string",
"description": "string",
"publish_date": "2019-08-24",
"author_id": 0,
"ISBN": "string",
"id": 0
}
]

- Create Book
  - URL: /books/
  - Method: POST
  - Description: Create a new book.
  - Request Body:
  - title: Title of the book.
  - author_id: ID of the author.
  - publish_date: Publish date of the book (YYYY-MM-DD format).
  - Example Request/Response:
    - POST /books/ HTTP/1.1
    - {
  "title": "New Book",
  "author_id": 2,
  "publish_date": "2023-05-15"
}
- Retrieve Single Book by ID
  - URL: /books/{book_id}/
  - Method: GET
  - Description: Retrieve details of a specific book by ID.
  - Example Request/Response:
    - GET /books/2/ HTTP/1.1
    - {
  "id": 2,
  "title": "New Book",
  "author_id": 2,
  "publish_date": "2023-05-15"
}

- Update Book
  - URL: /books/{book_id}/
  - Method: PUT
  - Description: Update details of an existing book by ID.
  - Request Body:
  - title (optional): New title of the book.
  - publish_date (optional): New publish date of the book (YYYY-MM-DD format).
  - Example Request/Response:
    - PUT /books/2/ HTTP/1.1
    - {
  "id": 2,
  "title": "Updated Book Title",
  "author_id": 2,
  "publish_date": "2023-05-15"
}
- Delete Book
  - URL: /books/{book_id}/
  - Method: DELETE
  - Description: Delete a book by ID.
  - Example Request/Response:
    - DELETE /books/2/ HTTP/1.1
    - {
  "message": "Book deleted successfully"
}
