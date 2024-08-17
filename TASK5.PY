import tkinter as tk
from tkinter import ttk
import requests

# API endpoint for exchange rates
EXCHANGE_RATE_API = "https://api.exchangerate-api.com/v4/latest/USD"

class CurrencyConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("USD Currency Converter")
        self.root.geometry("300x200")

        # Create input field for USD amount
        self.usd_amount_label = tk.Label(root, text="USD Amount:")
        self.usd_amount_label.pack()
        self.usd_amount_entry = tk.Entry(root, width=20)
        self.usd_amount_entry.pack()

        # Create dropdown menu for selecting target currency
        self.target_currency_label = tk.Label(root, text="Target Currency:")
        self.target_currency_label.pack()
        self.target_currency_var = tk.StringVar()
        self.target_currency_menu = ttk.Combobox(root, textvariable=self.target_currency_var)
        self.target_currency_menu['values'] = ['INR (Indian Rupee)', 'AED (UAE Dirham)', 'AUD (Australian Dollar)']
        self.target_currency_menu.current(0)
        self.target_currency_menu.pack()

        # Create button for performing conversion
        self.convert_button = tk.Button(root, text="Convert", command=self.convert_currency)
        self.convert_button.pack()

        # Create button for refreshing exchange rates
        self.refresh_button = tk.Button(root, text="Refresh Rates", command=self.refresh_exchange_rates)
        self.refresh_button.pack()

        # Create label to display conversion result
        self.result_label = tk.Label(root, text="")
        self.result_label.pack()

        # Fetch initial exchange rates
        self.exchange_rates = self.fetch_exchange_rates()

    def fetch_exchange_rates(self):
        response = requests.get(EXCHANGE_RATE_API)
        data = response.json()
        exchange_rates = {
            'INR': data['rates']['INR'],
            'AED': data['rates']['AED'],
            'AUD': data['rates']['AUD']
        }
        return exchange_rates

    def refresh_exchange_rates(self):
        self.exchange_rates = self.fetch_exchange_rates()
        self.result_label.config(text="Exchange rates refreshed!")

    def convert_currency(self):
        usd_amount = float(self.usd_amount_entry.get())
        target_currency = self.target_currency_var.get()
        if target_currency == 'INR (Indian Rupee)':
            exchange_rate = self.exchange_rates['INR']
        elif target_currency == 'AED (UAE Dirham)':
            exchange_rate = self.exchange_rates['AED']
        elif target_currency == 'AUD (Australian Dollar)':
            exchange_rate = self.exchange_rates['AUD']

        converted_amount = usd_amount * exchange_rate
        self.result_label.config(text=f"{usd_amount} USD = {converted_amount:.2f} {target_currency.split(' (')[0]}")

if __name__ == "__main__":
    root = tk.Tk()
    app = CurrencyConverterApp(root)
    root.mainloop()