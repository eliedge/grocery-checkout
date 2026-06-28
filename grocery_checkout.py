import tkinter as tk
from tkinter import messagebox

# -----------------------------
# (KEEP YOUR PRODUCT CLASSES + LOGIC EXACTLY THE SAME)
# -----------------------------

class Product:
    def __init__(self, name, price):
        self._name = name
        self._price = price
        self._category = "General"

    def final_price(self):
        return self._price

    def __str__(self):
        return f"{self._name} - ${self.final_price():.2f}"


class FoodProduct(Product):
    def __init__(self, name, price):
        super().__init__(name, price)
        self._category = "Food"


class BeverageProduct(Product):
    def __init__(self, name, price):
        super().__init__(name, price)
        self._category = "Beverage"

    def final_price(self):
        return self._price * 1.05


class SnackProduct(Product):
    def __init__(self, name, price):
        super().__init__(name, price)
        self._category = "Snack"

    def final_price(self):
        return self._price * 1.08


PRODUCTS = {
    "Food": {"Bread": 2.00, "Rice": 1.50, "Pasta": 1.20, "Apples": 0.80, "Eggs": 3.00},
    "Beverage": {"Water": 1.00, "Juice": 3.00, "Soda": 2.50, "Coffee": 4.00, "Tea": 2.00},
    "Snack": {"Chips": 1.50, "Cookies": 2.20, "Chocolate": 1.80, "Nuts": 3.50, "Popcorn": 1.25}
}

basket = []


def money(v):
    return f"${v:.2f}"


def total():
    return sum(i.final_price() for i in basket)


def refresh():
    listbox.delete(0, tk.END)
    for item in basket:
        listbox.insert(tk.END, str(item))
    total_label.config(text=f"Total: {money(total())}")


def add_item():
    cat = category_var.get()
    item = product_var.get()

    if not cat or not item:
        messagebox.showwarning("Missing", "Pick category and product")
        return

    price = PRODUCTS[cat][item]

    if cat == "Food":
        basket.append(FoodProduct(item, price))
    elif cat == "Beverage":
        basket.append(BeverageProduct(item, price))
    else:
        basket.append(SnackProduct(item, price))

    refresh()


def update_products(*args):
    menu = product_menu["menu"]
    menu.delete(0, "end")

    cat = category_var.get()
    if cat in PRODUCTS:
        for p in PRODUCTS[cat]:
            menu.add_command(label=p, command=tk._setit(product_var, p))
        product_var.set("")


def checkout():
    if not basket:
        messagebox.showinfo("Receipt", "Basket is empty")
        return

    receipt = "🧾 RECEIPT\n\n"
    for i in basket:
        receipt += str(i) + "\n"
    receipt += f"\nTOTAL: {money(total())}"

    messagebox.showinfo("Checkout", receipt)


def clear():
    basket.clear()
    refresh()


# -----------------------------
# UI SETUP (MODERN LOOK)
# -----------------------------

window = tk.Tk()
window.title("🛒 Grocery Checkout")
window.geometry("520x650")
window.configure(bg="#1e1e2f")

font_title = ("Arial", 18, "bold")
font_text = ("Arial", 12)

# TITLE
tk.Label(
    window,
    text="Grocery Checkout",
    font=font_title,
    bg="#1e1e2f",
    fg="white"
).pack(pady=10)

# FRAME: SELECTION
frame_top = tk.Frame(window, bg="#2a2a40", padx=15, pady=15)
frame_top.pack(pady=10, fill="x", padx=20)

tk.Label(frame_top, text="Category", bg="#2a2a40", fg="white").pack()
category_var = tk.StringVar()
category_menu = tk.OptionMenu(frame_top, category_var, *PRODUCTS.keys())
category_menu.pack()

category_var.trace("w", update_products)

tk.Label(frame_top, text="Product", bg="#2a2a40", fg="white").pack(pady=(10, 0))
product_var = tk.StringVar()
product_menu = tk.OptionMenu(frame_top, product_var, "")
product_menu.pack()

tk.Button(
    frame_top,
    text="Add to Basket",
    command=add_item,
    bg="#4CAF50",
    fg="white",
    font=font_text,
    width=20
).pack(pady=10)

# FRAME: BASKET
frame_mid = tk.Frame(window, bg="#2a2a40", padx=15, pady=15)
frame_mid.pack(pady=10, fill="both", expand=True, padx=20)

tk.Label(frame_mid, text="Basket", bg="#2a2a40", fg="white").pack()

listbox = tk.Listbox(frame_mid, width=50, height=12)
listbox.pack(pady=10)

total_label = tk.Label(
    frame_mid,
    text="Total: $0.00",
    font=("Arial", 14, "bold"),
    bg="#2a2a40",
    fg="white"
)
total_label.pack()

# FRAME: BUTTONS
frame_bottom = tk.Frame(window, bg="#1e1e2f")
frame_bottom.pack(pady=15)

tk.Button(frame_bottom, text="Checkout", command=checkout, width=15, bg="#2196F3", fg="white").grid(row=0, column=0, padx=10)
tk.Button(frame_bottom, text="Clear", command=clear, width=15, bg="#f44336", fg="white").grid(row=0, column=1, padx=10)

window.mainloop()