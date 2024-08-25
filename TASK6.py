import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as messagebox
import mysql.connector
import datetime

# MySQL Database connection
try:
    conn = mysql.connector.connect(
        host='localhost', 
        port=3306, 
        user='root',  
        password='Medapalli@8199'
    )
except mysql.connector.Error as err:
    print(f"Error connecting to MySQL: {err}")
    exit(1)

cursor = conn.cursor()

# Create database if not exists
cursor.execute('CREATE DATABASE IF NOT EXISTS billing_db')

# Select the database
conn.database = 'billing_db'

# Create tables if not exists
cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255),
        price FLOAT
    )
''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS customers (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255),
        address VARCHAR(255),
        phone VARCHAR(20)
    )
''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS transactions (
        id INT AUTO_INCREMENT PRIMARY KEY,
        customer_id INT,
        product_id INT,
        quantity INT,
        total FLOAT,
        date DATETIME,
        FOREIGN KEY (customer_id) REFERENCES customers(id),
        FOREIGN KEY (product_id) REFERENCES products(id)
    )
''')
conn.commit()

class BillingApp:
    def __init__(self, root):
        self.root = root
        self.root.title('Billing Software')
        self.root.geometry('800x600')

        # Create tabs
        self.tabs = ttk.Notebook(self.root)
        self.tabs.pack(fill='both', expand=True)

        # Create frames for each tab
        self.product_frame = ttk.Frame(self.tabs)
        self.customer_frame = ttk.Frame(self.tabs)
        self.billing_frame = ttk.Frame(self.tabs)
        self.invoice_frame = ttk.Frame(self.tabs)

        # Add frames to tabs
        self.tabs.add(self.product_frame, text='Products')
        self.tabs.add(self.customer_frame, text='Customers')
        self.tabs.add(self.billing_frame, text='Billing')
        self.tabs.add(self.invoice_frame, text='Invoice')

        # Product frame
        self.product_label = ttk.Label(self.product_frame, text='Product Name:')
        self.product_label.pack(pady=(10, 0))
        self.product_entry = ttk.Entry(self.product_frame, width=30)
        self.product_entry.pack(pady=(0, 10))
        self.price_label = ttk.Label(self.product_frame, text='Price:')
        self.price_label.pack()
        self.price_entry = ttk.Entry(self.product_frame, width=30)
        self.price_entry.pack(pady=(0, 10))
        self.add_product_button = ttk.Button(self.product_frame, text='Add Product', command=self.add_product)
        self.add_product_button.pack()

        # Customer frame
        self.customer_label = ttk.Label(self.customer_frame, text='Customer Name:')
        self.customer_label.pack(pady=(10, 0))
        self.customer_entry = ttk.Entry(self.customer_frame, width=30)
        self.customer_entry.pack(pady=(0, 10))
        self.address_label = ttk.Label(self.customer_frame, text='Address:')
        self.address_label.pack()
        self.address_entry = ttk.Entry(self.customer_frame, width=30)
        self.address_entry.pack(pady=(0, 10))
        self.phone_label = ttk.Label(self.customer_frame, text='Phone:')
        self.phone_label.pack()
        self.phone_entry = ttk.Entry(self.customer_frame, width=30)
        self.phone_entry.pack(pady=(0, 10))
        self.add_customer_button = ttk.Button(self.customer_frame, text='Add Customer', command=self.add_customer)
        self.add_customer_button.pack()

        # Billing frame
        self.customer_id_label = ttk.Label(self.billing_frame, text='Customer ID:')
        self.customer_id_label.pack(pady=(10, 0))
        self.customer_id_entry = ttk.Entry(self.billing_frame, width=30)
        self.customer_id_entry.pack(pady=(0, 10))
        self.product_id_label = ttk.Label(self.billing_frame, text='Product ID:')
        self.product_id_label.pack()
        self.product_id_entry = ttk.Entry(self.billing_frame, width=30)
        self.product_id_entry.pack(pady=(0, 10))
        self.quantity_label = ttk.Label(self.billing_frame, text='Quantity:')
        self.quantity_label.pack()
        self.quantity_entry = ttk.Entry(self.billing_frame, width=30)
        self.quantity_entry.pack(pady=(0, 10))
        self.bill_button = ttk.Button(self.billing_frame, text='Generate Bill', command=self.generate_bill)
        self.bill_button.pack()

        # Invoice frame
        self.invoice_text = tk.Text(self.invoice_frame, width=80, height=20)
        self.invoice_text.pack(pady=(10, 10))

    def add_product(self):
        name = self.product_entry.get().strip()
        price_str = self.price_entry.get().strip()
        if not name or not price_str:
            messagebox.showerror("Input Error", "Please provide both product name and price.")
            return
        try:
            price = float(price_str)
        except ValueError:
            messagebox.showerror("Invalid Input", "Price must be a number.")
            return
        try:
            cursor.execute('INSERT INTO products (name, price) VALUES (%s, %s)', (name, price))
            conn.commit()
            self.product_entry.delete(0, 'end')
            self.price_entry.delete(0, 'end')
            messagebox.showinfo("Success", "Product added successfully.")
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", str(err))

    def add_customer(self):
        name = self.customer_entry.get().strip()
        address = self.address_entry.get().strip()
        phone = self.phone_entry.get().strip()
        if not name or not address or not phone:
            messagebox.showerror("Input Error", "Please provide name, address, and phone.")
            return
        try:
            cursor.execute('INSERT INTO customers (name, address, phone) VALUES (%s, %s, %s)', (name, address, phone))
            conn.commit()
            self.customer_entry.delete(0, 'end')
            self.address_entry.delete(0, 'end')
            self.phone_entry.delete(0, 'end')
            messagebox.showinfo("Success", "Customer added successfully.")
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", str(err))

    def generate_bill(self):
        customer_id_str = self.customer_id_entry.get().strip()
        product_id_str = self.product_id_entry.get().strip()
        quantity_str = self.quantity_entry.get().strip()

        if not customer_id_str or not product_id_str or not quantity_str:
            messagebox.showerror("Input Error", "Please provide Customer ID, Product ID, and Quantity.")
            return

        try:
            customer_id = int(customer_id_str)
        except ValueError:
            messagebox.showerror("Invalid Input", "Customer ID must be an integer.")
            return
        try:
            product_id = int(product_id_str)
        except ValueError:
            messagebox.showerror("Invalid Input", "Product ID must be an integer.")
            return
        try:
            quantity = int(quantity_str)
            if quantity <= 0:
                messagebox.showerror("Invalid Input", "Quantity must be a positive integer.")
                return
        except ValueError:
            messagebox.showerror("Invalid Input", "Quantity must be an integer.")
            return

        # Check if customer exists
        try:
            cursor.execute('SELECT name FROM customers WHERE id=%s', (customer_id,))
            customer = cursor.fetchone()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", str(err))
            return

        if customer is None:
            messagebox.showerror("Error", f"No customer found with ID {customer_id}.")
            return

        # Check if product exists and get price
        try:
            cursor.execute('SELECT name, price FROM products WHERE id=%s', (product_id,))
            product = cursor.fetchone()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", str(err))
            return

        if product is None:
            messagebox.showerror("Error", f"No product found with ID {product_id}.")
            return

        product_name, price = product
        total = price * quantity
        date = datetime.datetime.now()

        try:
            cursor.execute('INSERT INTO transactions (customer_id, product_id, quantity, total, date) VALUES (%s, %s, %s, %s, %s)', 
                           (customer_id, product_id, quantity, total, date))
            conn.commit()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", str(err))
            return

        invoice = (
            f"Customer: {customer[0]} (ID: {customer_id})\n"
            f"Product: {product_name} (ID: {product_id})\n"
            f"Quantity: {quantity}\n"
            f"Unit Price: {price}\n"
            f"Total: {total}\n"
            f"Date: {date.strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        )
        self.invoice_text.insert('end', invoice)
        self.customer_id_entry.delete(0, 'end')
        self.product_id_entry.delete(0, 'end')
        self.quantity_entry.delete(0, 'end')
        messagebox.showinfo("Success", "Bill generated successfully.")

if __name__ == '__main__':
    root = tk.Tk()
    app = BillingApp(root)
    root.mainloop()
