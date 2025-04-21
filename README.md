# ALOHA

## Purpose
This project is a store management application designed to help store owners log hours worked, record expenses, and track closing tasks. The application features multiple screens and functionalities, including logging hours, managing expenses, and handling store closing procedures.

## Features

### 1. **Store Operations**
- **Log Expenses, Revenue, Invoices, Staff, Timehseet, Payroll and Withdrawals:**
  - Managers can review the store’s daily operations by entering and editing data.
- **Close Store:** 
  - Employees and Managers can finalize the store’s daily operations by entering data on the sales register, credit sales, and cash envelopes to close out the store for the day.

### 2. **User Authentication**
- **Login:** 
  - Users are required to log in with their credentials to access the store's management system.
- **Role-Based Interface:** 
  - The application presents different interfaces based on the user's role. For example, managers will have access to all features, while employees have limited access based on their role.

### 3. **Database Integration**
- **SQL Integration:** 
  - The system interacts with an SQL database to store and retrieve data.
- **SQL Assertions:** 
  - SQL assertions are used to ensure that only valid operations are performed in the database, preventing invalid data from being saved.
- **SQL Procedures and Triggers:** 
  - Procedures and triggers are used to efficiently handle data tasks like inputting and updating Expenses

### 4. **Graphical User Interface (GUI)**
- **User-Friendly Navigation:** 
  - The GUI is designed to be intuitive, allowing users to easily navigate through the different operations.
- **Consistent Layout:** 
  - All screens maintain a consistent layout with clean design, aligned components, and user-friendly interfaces that make operations straightforward.
- **Interactive Forms:** 
  - The forms within the GUI allow users to enter data with simple text inputs and dropdowns.

### 5. **Error Handling & Validation**
- **Input Validation:** 
  - Proper validation ensures that users input only valid data (e.g., numeric fields for sales totals and expenses) and prevents incorrect data from being entered.

## Installation

To get started with the ALOHA, follow the steps below.

### Prerequisites
- Python 3.x
- MySQL (or any other SQL database you plan to use)

### Install Dependencies

1. Clone the repository to your local machine:
    ```bash
    git clone https://github.com/tiaw999/ALOHA.git
    ```

2. Navigate into the project directory:
    ```bash
    cd ALOHA
    ```

3. Install the required Python dependencies:
    ```bash
    pip install -r requirements.txt
    ```

### Running the Application

1. Configure your credentials in db.py
2. Set up the database by running set_up.py

3. Run the main script to start the application:
    ```bash
    python main.py
    ```

## SQL Integration
The application requires MySQL. Make sure your SQL database is properly set up and connected.



