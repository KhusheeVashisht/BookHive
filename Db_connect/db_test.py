import mysql.connector

def create_connection():
    """Create and return a MySQL connection to the BookHive database."""
    connection = mysql.connector.connect(
        host="localhost",
        user="root",        # default user for XAMPP
        password="",        # leave empty unless you set one
        database="bookhive_db"
    )
    return connection
