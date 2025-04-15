# BookManager API

This is a **Book Management API** built with **Flask** and **MySQL**. The API allows users to perform CRUD operations on books, manage checkouts/check-ins, and search for books based on metadata like title, author, and genre.

## Features

- **CRUD Operations**: Add, edit, delete, and list books.
- **Check-in/Check-out**: Mark books as checked out or checked in.
- **Search**: Find books by title, author, ISBN, and genre.
- **Authentication**: Single Sign-On (SSO) authentication with multiple user roles and permissions (basic user and admin).

## Requirements

- Python 3.x
- Flask
- Flask-SQLAlchemy
- PyMySQL
- Fuzzywuzzy (for smart search)
- Python-Levenshtein (for performance)

## Setup

1. Clone this repository:

   ```bash
   git clone https://github.com/hanan-aref03/bookmanager.git
   ```
