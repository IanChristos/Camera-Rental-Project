
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

# CAMERA RENTAL MANAGEMENT SYSTEM #

cameras = [
    {"brand": "Canon", "model": "EOS R6 Mark II", "price": 65, "available": True},
    {"brand": "Canon", "model": "EOS R5", "price": 85, "available": True},
    {"brand": "Sony", "model": "A7 IV", "price": 70, "available": True},
    {"brand": "Sony", "model": "A7 III", "price": 50, "available": True},
    {"brand": "Sony", "model": "FX3", "price": 110, "available": True},
    {"brand": "Nikon", "model": "Z8", "price": 90, "available": True},
    {"brand": "Nikon", "model": "Z6 III", "price": 65, "available": True},
    {"brand": "Fujifilm", "model": "X-T5", "price": 55, "available": True},
    {"brand": "Panasonic", "model": "Lumix GH6", "price": 60, "available": True},
    {"brand": "GoPro", "model": "HERO13 Black", "price": 30, "available": True}
]

customers = []
rentals = []



# MAIN WINDOW
root = tk.Tk()
root.title("Camera Rental Management System")
root.geometry("1050x650")
root.minsize(850, 550)
root.configure(bg="#F1F5F9")



# STYLES
style = ttk.Style()
style.theme_use("clam")

style.configure(
    "Treeview",
    background="white",
    foreground="#1E293B",
    rowheight=35,
    fieldbackground="white",
    font=("Arial", 10)
)

style.configure(
    "Treeview.Heading",
    background="#E2E8F0",
    foreground="#1E293B",
    font=("Arial", 10, "bold")
)



# LAYOUT
sidebar = tk.Frame(root, bg="#172554", width=220)
sidebar.pack(side="left", fill="y")
sidebar.pack_propagate(False)

content = tk.Frame(root, bg="#F1F5F9")
content.pack(side="right", fill="both", expand=True)

# FUNCTIONS
def clear_content():
    for widget in content.winfo_children():
        widget.destroy()


def create_title(title, subtitle):
    tk.Label(
        content,
        text=title,
        font=("Arial", 23, "bold"),
        bg="#F1F5F9",
        fg="#172554"
    ).pack(anchor="w", padx=30, pady=(25, 5))

    tk.Label(
        content,
        text=subtitle,
        font=("Arial", 11),
        bg="#F1F5F9",
        fg="#64748B"
    ).pack(anchor="w", padx=30, pady=(0, 20))


def create_table(columns, headings):
    frame = tk.Frame(content, bg="white")
    frame.pack(fill="both", expand=True, padx=30, pady=10)

    table = ttk.Treeview(
        frame,
        columns=columns,
        show="headings"
    )

    for column, heading in zip(columns, headings):
        table.heading(column, text=heading)
        table.column(column, anchor="center", width=130)

    scrollbar = ttk.Scrollbar(
        frame,
        orient="vertical",
        command=table.yview
    )

    table.configure(yscrollcommand=scrollbar.set)

    table.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    return table


# DASHBOARD
def show_dashboard():
    clear_content()

    create_title(
        "Dashboard",
        "Welcome to Camera Rental Management System"
    )

    available = sum(c["available"] for c in cameras)
    rented = len(cameras) - available
    total_revenue = sum(r["total"] for r in rentals)

    cards = tk.Frame(content, bg="#F1F5F9")
    cards.pack(fill="x", padx=30, pady=20)

    information = [
        ("Total Cameras", len(cameras)),
        ("Available Cameras", available),
        ("Rented Cameras", rented),
        ("Total Revenue", f"£{total_revenue:.2f}")
    ]

    for title, value in information:
        card = tk.Frame(
            cards,
            bg="white",
            padx=15,
            pady=20
        )
        card.pack(side="left", expand=True, fill="x", padx=5)

        tk.Label(
            card,
            text=title,
            bg="white",
            fg="#64748B",
            font=("Arial", 10)
        ).pack()

        tk.Label(
            card,
            text=str(value),
            bg="white",
            fg="#172554",
            font=("Arial", 20, "bold")
        ).pack(pady=8)

    tk.Label(
        content,
        text="Quick Actions",
        bg="#F1F5F9",
        fg="#172554",
        font=("Arial", 16, "bold")
    ).pack(anchor="w", padx=35, pady=15)

    tk.Button(
        content,
        text="View Cameras",
        command=show_cameras,
        bg="#2563EB",
        fg="white",
        font=("Arial", 11, "bold"),
        padx=20,
        pady=10
    ).pack(anchor="w", padx=35)



# CAMERA INVENTORY
def show_cameras():
    clear_content()

    create_title(
        "Camera Inventory",
        "View all cameras and their availability"
    )

    table = create_table(
        ("brand", "model", "price", "status"),
        ("Brand", "Model", "Daily Price", "Status")
    )

    for camera in cameras:
        status = "Available" if camera["available"] else "Rented"

        table.insert(
            "",
            "end",
            values=(
                camera["brand"],
                camera["model"],
                f"£{camera['price']:.2f}",
                status
            )
        )


# CUSTOMER REGISTRATION
def register_customer():
    name = simpledialog.askstring(
        "Customer Registration",
        "Enter customer name:",
        parent=root
    )

    if not name or not name.strip():
        return

    phone = simpledialog.askstring(
        "Customer Registration",
        "Enter phone number:",
        parent=root
    )

    if not phone or not phone.strip():
        return

    customers.append({
        "name": name.strip(),
        "phone": phone.strip()
    })

    messagebox.showinfo(
        "Success",
        "Customer registered successfully!"
    )

    show_customers()


def show_customers():
    clear_content()

    create_title(
        "Customers",
        "Manage registered customers"
    )

    tk.Button(
        content,
        text="+ Register Customer",
        command=register_customer,
        bg="#2563EB",
        fg="white",
        font=("Arial", 10, "bold"),
        padx=15,
        pady=8
    ).pack(anchor="w", padx=30, pady=10)

    table = create_table(
        ("name", "phone"),
        ("Customer Name", "Phone Number")
    )

    for customer in customers:
        table.insert(
            "",
            "end",
            values=(customer["name"], customer["phone"])
        )



# RENT A CAMERA
def rent_camera():
    if not customers:
        messagebox.showwarning(
            "Warning",
            "Please register a customer first."
        )
        return

    available_cameras = [
        (i, camera)
        for i, camera in enumerate(cameras)
        if camera["available"]
    ]

    if not available_cameras:
        messagebox.showwarning(
            "Warning",
            "No cameras are currently available."
        )
        return

    customer_window = tk.Toplevel(root)
    customer_window.title("Rent a Camera")
    customer_window.geometry("400x350")
    customer_window.configure(bg="white")
    customer_window.transient(root)
    customer_window.grab_set()

    tk.Label(
        customer_window,
        text="New Camera Rental",
        font=("Arial", 18, "bold"),
        bg="white",
        fg="#172554"
    ).pack(pady=20)

    tk.Label(
        customer_window,
        text="Select Customer:",
        bg="white"
    ).pack()

    customer_var = tk.StringVar()

    customer_box = ttk.Combobox(
        customer_window,
        textvariable=customer_var,
        state="readonly",
        values=[
            f"{i + 1}. {c['name']}"
            for i, c in enumerate(customers)
        ]
    )
    customer_box.pack(pady=8)

    tk.Label(
        customer_window,
        text="Select Camera:",
        bg="white"
    ).pack()

    camera_var = tk.StringVar()

    camera_box = ttk.Combobox(
        customer_window,
        textvariable=camera_var,
        state="readonly",
        values=[
            f"{i + 1}. {c['brand']} {c['model']} - £{c['price']}/day"
            for i, c in available_cameras
        ]
    )
    camera_box.pack(pady=8)

    tk.Label(
        customer_window,
        text="Rental Days:",
        bg="white"
    ).pack()

    days_entry = tk.Entry(customer_window)
    days_entry.pack(pady=8)

    def confirm_rental():
        if not customer_var.get() or not camera_var.get():
            messagebox.showwarning(
                "Warning",
                "Please select a customer and camera."
            )
            return

        try:
            days = int(days_entry.get())

            if days <= 0:
                raise ValueError

        except ValueError:
            messagebox.showerror(
                "Error",
                "Please enter a valid number of days."
            )
            return

        customer_index = customer_box.current()
        camera_index = camera_box.current()

        original_camera_id, camera = available_cameras[camera_index]
        customer = customers[customer_index]

        total = camera["price"] * days

        rentals.append({
            "customer": customer["name"],
            "camera": camera["brand"] + " " + camera["model"],
            "camera_id": original_camera_id,
            "days": days,
            "total": total,
            "returned": False
        })

        camera["available"] = False

        messagebox.showinfo(
            "Rental Confirmed",
            f"Customer: {customer['name']}\n"
            f"Camera: {camera['model']}\n"
            f"Days: {days}\n"
            f"Total: £{total:.2f}"
        )

        customer_window.destroy()
        show_dashboard()

    tk.Button(
        customer_window,
        text="Confirm Rental",
        command=confirm_rental,
        bg="#16A34A",
        fg="white",
        font=("Arial", 11, "bold"),
        padx=20,
        pady=8
    ).pack(pady=15)


# RENTAL HISTORY
def show_rentals():
    clear_content()

    create_title(
        "Rental History",
        "View all active and completed rentals"
    )

    table = create_table(
        ("customer", "camera", "days", "total", "status"),
        ("Customer", "Camera", "Days", "Total", "Status")
    )

    for rental in rentals:
        status = "Returned" if rental["returned"] else "Active"

        table.insert(
            "",
            "end",
            values=(
                rental["customer"],
                rental["camera"],
                rental["days"],
                f"£{rental['total']:.2f}",
                status
            )
        )



# RETURN CAMERA
def return_camera():
    active_rentals = [
        rental for rental in rentals
        if not rental["returned"]
    ]

    if not active_rentals:
        messagebox.showinfo(
            "Information",
            "There are no active rentals."
        )
        return

    return_window = tk.Toplevel(root)
    return_window.title("Return Camera")
    return_window.geometry("450x300")
    return_window.configure(bg="white")
    return_window.transient(root)
    return_window.grab_set()

    tk.Label(
        return_window,
        text="Return Camera",
        font=("Arial", 18, "bold"),
        bg="white",
        fg="#172554"
    ).pack(pady=20)

    rental_var = tk.StringVar()

    rental_box = ttk.Combobox(
        return_window,
        textvariable=rental_var,
        state="readonly",
        values=[
            f"{i + 1}. {r['customer']} - {r['camera']}"
            for i, r in enumerate(active_rentals)
        ],
        width=45
    )
    rental_box.pack(pady=15)

    def confirm_return():
        index = rental_box.current()

        if index < 0:
            messagebox.showwarning(
                "Warning",
                "Please select a rental."
            )
            return

        rental = active_rentals[index]

        rental["returned"] = True
        cameras[rental["camera_id"]]["available"] = True

        messagebox.showinfo(
            "Success",
            "Camera returned successfully!"
        )

        return_window.destroy()
        show_dashboard()

    tk.Button(
        return_window,
        text="Confirm Return",
        command=confirm_return,
        bg="#16A34A",
        fg="white",
        font=("Arial", 11, "bold"),
        padx=20,
        pady=8
    ).pack(pady=15)


# SIDEBAR MENU
tk.Label(
    sidebar,
    text="CAMERA RENTAL",
    font=("Arial", 17, "bold"),
    bg="#172554",
    fg="white"
).pack(pady=35)

buttons = [
    ("Dashboard", show_dashboard),
    ("Camera Inventory", show_cameras),
    ("Customers", show_customers),
    ("Rent a Camera", rent_camera),
    ("Rental History", show_rentals),
    ("Return Camera", return_camera)
]

for text, command in buttons:
    tk.Button(
        sidebar,
        text=text,
        command=command,
        bg="#1E3A8A",
        fg="white",
        activebackground="#2563EB",
        activeforeground="white",
        relief="flat",
        font=("Arial", 11),
        anchor="w",
        padx=20,
        pady=12
    ).pack(fill="x", padx=12, pady=4)


tk.Label(
    sidebar,
    text="Version 1.0",
    bg="#172554",
    fg="#94A3B8",
    font=("Arial", 9)
).pack(side="bottom", pady=20)


# START APPLICATION
show_dashboard()

root.mainloop()
