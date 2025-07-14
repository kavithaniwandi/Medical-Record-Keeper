import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

# Login credentials
USERNAME = "admin"
PASSWORD = "care123"

class CaremintApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Caremint - Medical Record Keeper")
        self.root.geometry("800x600")

        # Load original background image
        self.original_bg = Image.open("background.jpg")

        # Create canvas to hold background image
        self.canvas = tk.Canvas(self.root, highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Initially create resized image and display it
        self.bg_image = ImageTk.PhotoImage(self.original_bg.resize((800, 600)))
        self.bg_img_id = self.canvas.create_image(0, 0, anchor="nw", image=self.bg_image)

        # Bind window resize event to resize background
        self.root.bind("<Configure>", self.resize_background)

        # Create a frame on the canvas to hold all UI widgets
        self.frame = tk.Frame(self.canvas, bg="#ffffff", bd=0)
        self.frame_id = self.canvas.create_window(0, 0, anchor="nw", window=self.frame)

        self.records = []
        self.login_screen()

    def resize_background(self, event):
        if event.width > 0 and event.height > 0:
            resized = self.original_bg.resize((event.width, event.height), Image.ANTIALIAS)
            self.bg_image = ImageTk.PhotoImage(resized)
            self.canvas.itemconfig(self.bg_img_id, image=self.bg_image)

            frame_width = self.frame.winfo_reqwidth()
            frame_height = self.frame.winfo_reqheight()
            x = (event.width - frame_width) // 2
            y = (event.height - frame_height) // 2
            self.canvas.coords(self.frame_id, x, y)

    def clear_frame(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

    def login_screen(self):
        self.clear_frame()

        tk.Label(self.frame, text="Login to Caremint", font=("Arial", 16), bg="#ffffff").pack(pady=20)

        tk.Label(self.frame, text="Username", bg="#ffffff").pack()
        self.username_entry = tk.Entry(self.frame)
        self.username_entry.pack()

        tk.Label(self.frame, text="Password", bg="#ffffff").pack()
        self.password_entry = tk.Entry(self.frame, show="*")
        self.password_entry.pack()

        tk.Button(self.frame, text="Login", command=self.check_login).pack(pady=20)

    def check_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username == USERNAME and password == PASSWORD:
            self.main_menu()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

    def main_menu(self):
        self.clear_frame()

        tk.Label(self.frame, text="Caremint - Main Menu", font=("Arial", 16), bg="#ffffff").pack(pady=20)

        tk.Button(self.frame, text="Add Record", width=20, command=self.add_record_screen).pack(pady=5)
        tk.Button(self.frame, text="View Records", width=20, command=self.view_records_screen).pack(pady=5)
        tk.Button(self.frame, text="Search Records", width=20, command=self.search_records_screen).pack(pady=5)
        tk.Button(self.frame, text="Exit", width=20, command=self.root.quit).pack(pady=5)

    def add_record_screen(self):
        self.clear_frame()

        tk.Label(self.frame, text="Add Medical Record", font=("Arial", 14), bg="#ffffff").pack(pady=15)

        self.entry_fields = {}

        for field in ["Date (YYYY-MM-DD)", "Type", "Description", "Doctor"]:
            tk.Label(self.frame, text=field, bg="#ffffff").pack()
            entry = tk.Entry(self.frame)
            entry.pack()
            self.entry_fields[field] = entry

        tk.Button(self.frame, text="Save Record", command=self.save_record).pack(pady=10)
        tk.Button(self.frame, text="Back", command=self.main_menu).pack()

    def save_record(self):
        record = {
            "date": self.entry_fields["Date (YYYY-MM-DD)"].get(),
            "type": self.entry_fields["Type"].get(),
            "description": self.entry_fields["Description"].get(),
            "doctor": self.entry_fields["Doctor"].get()
        }

        self.records.append(record)
        messagebox.showinfo("Success", "✅ Record saved successfully!")
        self.main_menu()

    def view_records_screen(self):
        self.clear_frame()

        tk.Label(self.frame, text="View Medical Records", font=("Arial", 14), bg="#ffffff").pack(pady=10)

        if not self.records:
            tk.Label(self.frame, text="No records found.", bg="#ffffff").pack()
        else:
            container = tk.Frame(self.frame, bg="#ffffff")
            container.pack(fill=tk.BOTH, expand=True)

            canvas = tk.Canvas(container, bg="#ffffff", highlightthickness=0)
            scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
            scrollable_frame = tk.Frame(canvas, bg="#ffffff")

            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )

            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)

            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")

            for i, record in enumerate(self.records, 1):
                text = (f"{i}. Date: {record['date']}, Type: {record['type']}\n"
                        f"   Description: {record['description']}\n"
                        f"   Doctor: {record['doctor']}")
                label = tk.Label(scrollable_frame, text=text, justify="left", anchor="w",
                                 padx=10, pady=5, bd=1, relief="solid", bg="#f9f9f9")
                label.pack(fill="x", padx=5, pady=2)

        tk.Button(self.frame, text="Back", command=self.main_menu).pack(pady=10)

    def search_records_screen(self):
        self.clear_frame()

        tk.Label(self.frame, text="Search Medical Records", font=("Arial", 14), bg="#ffffff").pack(pady=10)

        tk.Label(self.frame, text="Enter keyword (Type or Description):", bg="#ffffff").pack()
        self.search_entry = tk.Entry(self.frame)
        self.search_entry.pack(pady=5)

        tk.Button(self.frame, text="Search", command=self.perform_search).pack(pady=5)
        tk.Button(self.frame, text="Back", command=self.main_menu).pack(pady=5)

    def perform_search(self):
        keyword = self.search_entry.get().strip().lower()
        if not keyword:
            messagebox.showwarning("Input Needed", "Please enter a keyword to search.")
            return

        results = [r for r in self.records if keyword in r['type'].lower() or keyword in r['description'].lower()]

        self.clear_frame()
        tk.Label(self.frame, text=f"Search Results for '{keyword}'", font=("Arial", 14), bg="#ffffff").pack(pady=10)

        if not results:
            tk.Label(self.frame, text="No matching records found.", bg="#ffffff").pack()
        else:
            for i, record in enumerate(results, 1):
                text = (f"{i}. Date: {record['date']}, Type: {record['type']}\n"
                        f"   Description: {record['description']}\n"
                        f"   Doctor: {record['doctor']}")
                tk.Label(self.frame, text=text, justify="left", anchor="w",
                         padx=10, pady=5, bd=1, relief="solid", bg="#f9f9f9").pack(fill="x", padx=5, pady=2)

        tk.Button(self.frame, text="Back", command=self.main_menu).pack(pady=10)


if __name__ == "__main__":
    root = tk.Tk()
    app = CaremintApp(root)
    root.mainloop()
