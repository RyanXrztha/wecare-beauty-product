# WeCare Beauty — Store Management System

A command-line inventory and point-of-sale (POS) system for managing a beauty product store. Built with Python, it handles product inventory, sales transactions, restocking, and automatic bill generation.

---

## 📋 Table of Contents
- [Features](#features)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Sample Output](#sample-output)
- [Known Limitations](#known-limitations)
- [Future Improvements](#future-improvements)

---

## ✨ Features

- 📦 **Inventory Management** — Add, view, and track beauty products with name, brand, quantity, cost price, and country of origin
- 🛒 **Point of Sale** — Process customer purchases with automatic pricing (cost × 2)
- 🎁 **Promotions** — Automatic "Buy 3 Get 1 Free" applied at checkout
- 🚚 **Shipping Option** — Optional $20 shipping fee at checkout
- 🔄 **Restocking** — Restock existing products and update inventory instantly
- 🧾 **Bill Generation** — Automatically saves purchase, restock, and new item bills as `.txt` files
- 💾 **Persistent Storage** — All product data saved to a local file (`StoreFile.txt`)

---

## 🗂 Project Structure

```
wecare-beauty-product/
│
├── main.py            # Entry point — main menu loop
├── operations.py      # Core business logic (buy, add, restock, display)
├── read.py            # Loads product data from StoreFile.txt
├── write.py           # Saves product data and generates bill files
├── StoreFile.txt      # Product database (comma-separated)
└── README.md
```

### How the modules connect

```
main.py
  └── calls operations.py  (display, buyGoods, addGoods, fillGoods)
        └── uses read.py   (load products into memory)
        └── uses write.py  (save products, generate bills)
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.x — Download from [python.org](https://www.python.org/downloads/)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/RyanXrztha/wecare-beauty-product.git
cd wecare-beauty-product
```

2. Create an empty `StoreFile.txt` if it doesn't exist:
```bash
touch StoreFile.txt   # Mac/Linux
type nul > StoreFile.txt   # Windows
```

3. Run the program:
```bash
python main.py
```

---

## 🖥 Usage

When you run the program, you'll see the main menu:

```
1. View Products
2. Buy Products
3. Add New Product
4. Restock Product
5. Exit

Enter your choice:
```

### Menu Options

| Option | Description |
|--------|-------------|
| 1 | View all products in a formatted table |
| 2 | Process a customer purchase with cart and bill |
| 3 | Add a brand new product to inventory |
| 4 | Restock an existing product's quantity |
| 5 | Exit the program |

### Data Format (`StoreFile.txt`)

Products are stored as comma-separated values:
```
ProductName,Brand,Quantity,CostPrice,Origin
ClearGlow Serum,Neutrogena,50,15.0,USA
HydraBoost Cream,Cetaphil,30,12.5,France
```

### Bill Files

Every transaction automatically generates a `.txt` bill file named by timestamp (e.g. `142305142305.txt`), saved in the project folder.

---

## 📌 Known Limitations

- **File-based storage** — Uses a plain text file instead of a database; not suitable for concurrent users
- **No authentication** — Anyone with access can run the program
- **Commas in product names** — Could break CSV parsing since commas are used as delimiters
- **Selling price fixed at 2×** — Markup percentage is hardcoded and not configurable

---

## 🔮 Future Improvements

- [ ] Replace `StoreFile.txt` with SQLite database for reliability
- [ ] Add user login and role-based access (admin vs cashier)
- [ ] Build a web interface using Flask
- [ ] Add search and filter for products
- [ ] Generate PDF bills instead of `.txt` files
- [ ] Add sales reporting and analytics

---

## 👤 Author

**Ryan** — [github.com/RyanXrztha](https://github.com/RyanXrztha)

For questions or feedback, contact: aryanshrestha189@gmail.com
