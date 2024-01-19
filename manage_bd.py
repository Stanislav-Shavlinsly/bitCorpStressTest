import sqlite3
import os
from eth_keys import keys
# Function to create a SQLite database and the Users table
def create_database():
    # Establishing a connection to the SQLite database
    conn = sqlite3.connect('test_db.sqlite')
    cursor = conn.cursor()

    # Creating the Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users (
            id INTEGER PRIMARY KEY,
            address TEXT,
            private_key TEXT
        )
    ''')
    conn.commit()
    conn.close()


# Function to generate Ethereum-like addresses and keys
def generate_ethereum_addresses_and_keys(n):


    def generate_ethereum_wallet():
        # Генерация приватного ключа
        private_key = keys.PrivateKey(os.urandom(32))

        # Получение публичного ключа из приватного
        public_key = private_key.public_key

        # Получение адреса кошелька Ethereum
        address = public_key.to_checksum_address()
        print(address, private_key)
        return str(address), str(private_key)

    return [generate_ethereum_wallet() for _ in range(n)]


# Function to populate the Users table with generated addresses and keys
def populate_users_table():
    # Generate 10000 Ethereum-like addresses and keys
    data = generate_ethereum_addresses_and_keys(10000)

    # Connect to the SQLite database
    conn = sqlite3.connect('test_db.sqlite')
    cursor = conn.cursor()

    # Insert generated data into the Users table
    cursor.executemany('INSERT INTO Users (address, private_key) VALUES (?, ?)', data)
    conn.commit()
    conn.close()


def read_users_table():
    # Connect to the SQLite database
    conn = sqlite3.connect('test_db.sqlite')
    cursor = conn.cursor()

    # Query to select all data from the Users table
    cursor.execute('SELECT id, address, private_key FROM Users')
    rows = cursor.fetchall()

    # Close the connection
    conn.close()

    # Convert rows to a list of dictionaries
    users_list = [{"id": row[0], "address": row[1], "private_key": row[2]} for row in rows]

    return users_list

# Read the Users table and create a list of dictionaries

