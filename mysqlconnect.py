import mysql.connector



db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',  # Replace with your XAMPP MySQL password if applicable
    'database': 'flask_auth_db'
}
# Connect to the MySQL database
def connect_db():
    connection = mysql.connector.connect(**db_config)
    return connection

# Function to create a table
def create_table(query):
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()
    cursor.close()
    connection.close()
    print("Table created successfully.")

# Function to insert data into a table
def insert_data(query, data):
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute(query, data)
    connection.commit()
    cursor.close()
    connection.close()
    print("Data inserted successfully.")

# Function to fetch data from the table
def fetch_data(query, params=None):
    connection = connect_db()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(query, params)
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return result

# Function to update data in the table
def update_data(query, data):
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute(query, data)
    connection.commit()
    cursor.close()
    connection.close()
    print("Data updated successfully.")

# Function to delete data from the table
def delete_data(query, params=None):
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute(query, params)
    connection.commit()
    cursor.close()
    connection.close()
    print("Data deleted successfully.")
