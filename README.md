

---

# Bibliotheca Confluxor: Pythonic & Tkinter-Enhanced Librarium Management Interface

## Overview

Bibliotheca Confluxor is an advanced library management system developed using Python and Tkinter. Designed to streamline and simplify library operations, this application provides a comprehensive solution for managing books, users, and financial transactions. Leveraging SQLite for robust data storage, Bibliotheca Confluxor ensures efficient, reliable, and seamless management of a library's resources.

## Features

### Book Management
- **View Books:** Browse and view the entire catalog of books.
- **Add Books:** Add new books to the collection or update the quantity of existing ones.

### User Administration
- **Issue Books:** Issue books to users with automatic due date tracking.
- **Remove Users:** Remove users and manage the return of issued books.

### Owner's Dashboard
- **Monitor Users:** Track active users, their contact information, and issued books.

### Returned Books and Penalties
- **Manage Returns:** Handle returned books and calculate any applicable penalties.
- **Add Penalties:** Record financial penalties for late returns and facilitate payment collection.

### Wallet Management
- **Track Transactions:** Maintain a detailed ledger of all monetary transactions, categorized by payment type.
- **Withdraw Funds:** Consolidate and withdraw funds from the virtual wallet.

## Technologies Used
- **Frontend:** Tkinter for creating sophisticated graphical user interfaces.
- **Backend:** SQLite for seamless and lightweight data management.
- **Programming Language:** Python for its simplicity, versatility, and robustness.

## Installation and Usage

### Prerequisites
Ensure you have Python installed on your system. You can download it from [python.org](https://www.python.org/).

### Clone the Repository
```bash
git clone https://github.com/yourusername/BibliothecaConfluxor.git
```

### Navigate to the Project Directory
```bash
cd BibliothecaConfluxor
```

### Install Dependencies
Install the required dependencies using pip:
```bash
pip install -r requirements.txt
```

### Initialize the Database
Run the script to initialize the database:
```bash
python init_db.py
```

### Run the Application
Start the application with the following command:
```bash
python library_management.py
```

## How to Use

### Main Window
The main window provides buttons for accessing various functionalities:
- **View Books**
- **Add Books**
- **Users**
- **Remove Users**
- **Owner Section**
- **Incoming Payments**
- **Wallet**

### Viewing Books
Click on "View Books" to open a new window displaying all the books in the library.

### Adding Books
Click on "Add Books" to open a form where you can enter the book's name, author, and quantity. Submit the form to add the book to the library.

### Issuing Books to Users
Click on "Users" to open a form where you can enter the user's name, book name, author, and phone number. Submit the form to issue the book.

### Removing Users
Click on "Remove Users" to view all users with issued books. Click on a user to remove them and update the book's quantity.

### Owner's Section
Click on "Owner Section" to view a list of all active users and their issued books.

### Handling Returned Books and Penalties
Click on "Incoming Payments" to manage returned books and add any applicable penalties.

### Managing the Wallet
Click on "Wallet" to view all financial transactions and withdraw funds from the virtual wallet.

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request with your changes.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

