
# README

## Overview

This project implements a secure communication system using Python. It consists of a client-server application that ensures data integrity and confidentiality through encryption and hashing. The system employs elliptic curve cryptography (ECC) for encrypting messages and SSL/TLS for securing the communication channel.

## Components

1. **Client Application (`client.py`):**
   - Connects to the server using a secure SSL/TLS connection.
   - Encrypts user input messages using elliptic curve cryptography.
   - Hashes the messages with SHA-256 to ensure data integrity.
   - Sends encrypted messages and their hash codes to the server.
   - Receives and prints responses from the server.

2. **Server Application (`server.py`):**
   - Listens for incoming connections from clients.
   - Secures the connection using SSL/TLS.
   - Receives encrypted messages and their hash codes from the client.
   - Decrypts the messages using ECC.
   - Verifies the message integrity by comparing hash codes.
   - Sends responses back to the client.

3. **User Management (`user_management.py`):**
   - Provides functionalities for user registration and login.
   - Stores user credentials in an SQLite database.
   - Hashes passwords using SHA-256 for secure storage.
   - Supports administrative access for viewing user data.

4. **Encryption Module (`metin_şifreleme.py`):**
   - Implements elliptic curve cryptography for encrypting and decrypting messages.
   - Defines mathematical operations for ECC, including point addition and scalar multiplication.

## How It Works

### Client-Server Communication

1. **Client Initialization:**
   - The client establishes a connection to the server using the specified IP address and port.
   - It then wraps the socket with an SSL/TLS layer to secure the communication.

2. **Message Encryption:**
   - The client prompts the user for input.
   - It encrypts the message using elliptic curve cryptography.
   - The encrypted message and its SHA-256 hash are sent to the server.

3. **Server Processing:**
   - The server accepts incoming connections and wraps the socket with SSL/TLS.
   - It receives and decrypts the message.
   - The server verifies the message's hash against the received hash code to ensure integrity.
   - It sends a response back to the client confirming the acceptance of the data.

4. **User Management:**
   - Users can register and log in using the provided credentials.
   - Passwords are hashed before being stored in the database.
   - Admin users have additional access to view user data.

## Setup

1. **Generate SSL/TLS Certificates:**
   - Ensure you have `server_cert.pem` and `server_key.pem` for SSL/TLS encryption.

2. **Run the Server:**
   - Execute `server.py` to start the server and listen for client connections.

3. **Run the Client:**
   - Execute `client.py` to connect to the server and start sending encrypted messages.

4. **User Management:**
   - Use `user_management.py` to handle user registration and login.
