# BookHive Mini Project

## Overview
BookHive is a mini bookstore management system that combines multiple subjects:
- **DBMS**: MariaDB database using XAMPP to manage users, books, rentals, and transactions.
- **AI Recommendations**: Personalized book recommendations for users.
- **DAA Algorithms**: Searching and sorting algorithms applied for book lookup and analytics.

This project demonstrates integration of database management, web development, and algorithmic concepts.

> ⚠️ **Note:** The project is still under development. New features and improvements will be added soon.

---

## Features
- User registration and login
- Browse books with details
- Rent and return books
- Track transactions
- Admin dashboard with analytics:
  - Top rented books
  - Least rented and sold books
  - Cheapest book
- AI-based book recommendations
- Fast searching using DAA algorithms

---

## Technologies Used
- **Frontend:** HTML, CSS, JavaScript
- **Backend:** PHP (XAMPP)
- **Database:** MariaDB (via XAMPP)
- **Algorithms:** DAA (searching/sorting)
- **AI:** Recommendation system (Python)

---

## Folder Structure

BookHive/
│
├─ README.md
├─ bookhive_db.sql           # Database export for recreating tables
├─ screenshots/              # Images showing tables, queries, and UI
├─ index.php                 # Main page
├─ css/
├─ js/
├─ php/
├─ python_ai/                # AI and algorithm scripts
└─ other project files...



---

## Database Setup (DBMS)

1. Start **XAMPP** → Apache and MariaDB.
2. Open **phpMyAdmin**.
3. Create the database:
    ```sql
       CREATE DATABASE bookhive;
       USE bookhive;

 4. Import the tables:
       Go to Import → Select bookhive_db.sql → Execute.
    Tables included:
                users
                books
                rentals
                transactions

    Example Query
               SELECT * FROM books WHERE rented_count > 10;

## How to Run Locally
Clone the repository:
        git clone https://github.com/KhusheeVashisht/BookHive.git
Place it in XAMPP's htdocs folder:
        C:\xampp\htdocs\BookHive
Start Apache and MariaDB in XAMPP.
        Import bookhive_db.sql in phpMyAdmin.
Open in browser:
        http://localhost/BookHive
Explore features:
    Register/Login
    Browse/Rent books
    View AI recommendations
    Admin analytics

## Screenshots
    screenshots/ folder contains images of:
    Database tables
    Queries run
    User interface
    
## Author

Khushee Vashisht
Email: 25mci10292@cuchd.in , khusheevashisht.hs.106.prag@gmail.com and khusheevashisht17@gmail.com

## ⚠️ Project is still in progress — new features and improvements will be added.


---
