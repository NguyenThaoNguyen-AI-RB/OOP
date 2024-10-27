import tkinter as tk
from tkinter import messagebox
import csv
import os

class Users:
    def __init__(self, name, password):
        self.name = name
        self.password = password
# Lớp Product
class Product:
    def __init__(self, product_id, product_name, price, quantity_in_stock):
        self.product_id = product_id
        self.product_name = product_name
        self.price = price
        self.quantity_in_stock = quantity_in_stock


# Lớp Customer
class Customer(Users):
    def __init__(self, name, password, phone='', email='', address=''):
        super().__init__(name, password)
        self.phone = phone
        self.email = email
        self.address = address
        self.cart = []

    def add_to_cart(self, product, quantity):
        self.cart.append({"product": product, "quantity": quantity})

    def view_cart(self):
        cart_items = []
        for item in self.cart:
            cart_items.append(f"{item['product'].product_name}: {item['quantity']}")
        return "\n".join(cart_items)


# Lớp Manager để quản lý sản phẩm và kiểm tra tồn kho
class Manager(Users):
    def __init__(self, name, password):
        super().__init__(name, password)
        self.product_list = []

    def add_product(self, product):
        self.product_list.append(product)

    def edit_product(self, product_id, new_name, new_price, new_quantity):
        for product in self.product_list:
            if product.product_id == product_id:
                product.product_name = new_name
                product.price = new_price
                product.quantity_in_stock = new_quantity
                return True
        return False

    def delete_product(self, product_id):
        for product in self.product_list:
            if product.product_id == product_id:
                self.product_list.remove(product)
                return True
        return False

    def view_inventory(self):
        inventory = []
        for product in self.product_list:
            inventory.append(f"{product.product_name}: {product.quantity_in_stock} in stock")
        return "\n".join(inventory)


# Quản lý thông tin người dùng
class UserManager:
    def __init__(self):
        # Một tài khoản quản lý mặc định
        self.users = {"admin": {"password": "admin", "role": "manager"}}

    def register(self, username, password):
        if username in self.users:
            return False  # Tên người dùng đã tồn tại
        self.users[username] = {"password": password, "role": "customer"}
        return True

    def login(self, username, password):
        if username in self.users and self.users[username]["password"] == password:
            return self.users[username]["role"]  # Trả về vai trò (manager hoặc customer)
        return None

class StoreApp:
    def manager_products(self):
        self.manager_product()  

    def view_customer_info(self):
        pass  

    def manager_orders(self):
        pass 

    def view_inventory(self):
        pass  

    def __init__(self, root):
        self.root = root
        self.root.title("Ứng dụng quản lý cửa hàng")

        # Tạo customer và manager giả lập
        self.customer = None
        self.manager = Manager("Quản lý 1")

        # Quản lý tài khoản người dùng
        self.user_manager = UserManager()

        # Thêm một số sản phẩm vào kho hàng ban đầu
        initial_products = [
            Product(1, "Áo", 100000, 10),
            Product(2, "Quần", 200000, 5),
            Product(3, "Giày", 300000, 2)
        ]
        for product in initial_products:
            self.manager.add_product(product)

        # Tạo giao diện
        self.create_login_screen()

    # Giao diện đăng nhập
    def create_login_screen(self):
        self.clear_screen()

        tk.Label(self.root, text="Đăng nhập", font=("Arial", 16)).pack(pady=10)

        tk.Label(self.root, text="Tên đăng nhập").pack()
        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack()

        tk.Label(self.root, text="Mật khẩu").pack()
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.pack()

        self.login_button = tk.Button(self.root, text="Đăng nhập", command=self.login)
        self.login_button.pack(pady=10)

        self.register_button = tk.Button(self.root, text="Đăng ký", command=self.create_register_screen)
        self.register_button.pack()

    # Giao diện đăng ký
    def create_register_screen(self):
        self.clear_screen()

        tk.Label(self.root, text="Đăng ký", font=("Arial", 16)).pack(pady=10)

        tk.Label(self.root, text="Tên đăng nhập").pack()
        self.register_username_entry = tk.Entry(self.root)
        self.register_username_entry.pack()

        tk.Label(self.root, text="Mật khẩu").pack()
        self.register_password_entry = tk.Entry(self.root, show="*")
        self.register_password_entry.pack()

        self.register_button = tk.Button(self.root, text="Tạo tài khoản", command=self.register)
        self.register_button.pack(pady=10)

        self.back_to_login_button = tk.Button(self.root, text="Quay lại", command=self.create_login_screen)
        self.back_to_login_button.pack()

    # Đăng ký tài khoản
    def register(self):
        username = self.register_username_entry.get()
        password = self.register_password_entry.get()
        if self.user_manager.register(username, password):
            messagebox.showinfo("Thành công", "Đăng ký thành công! Vui lòng đăng nhập.")
            self.create_login_screen()
        else:
            messagebox.showerror("Lỗi", "Tên đăng nhập đã tồn tại!")

    # Đăng nhập
    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        role = self.user_manager.login(username, password)

        if role == "manager":
            self.manager_dashboard()
        elif role == "customer":
            self.customer = Customer(username)  # Khởi tạo khách hàng
            self.customer_dashboard()
        else:
            messagebox.showerror("Lỗi", "Sai tên đăng nhập hoặc mật khẩu!")

    # Giao diện chính của Customer
    def customer_dashboard(self):
        self.clear_screen()
        tk.Label(self.root, text=f"Chào mừng {self.customer.name}", font=("Arial", 16)).pack(pady=10)

        # Hiển thị thông tin cá nhân
        tk.Label(self.root, text="Thông tin cá nhân:", font=("Arial", 14)).pack(pady=5)

        # Tên
        tk.Label(self.root, text=f"Tên: {self.customer.name}").pack()

        # Số điện thoại
        tk.Label(self.root, text="Số điện thoại:").pack()
        self.phone_entry = tk.Entry(self.root)
        self.phone_entry.insert(0, self.customer.phone)  
        self.phone_entry.pack()

        # Email
        tk.Label(self.root, text="Email:").pack()
        self.email_entry = tk.Entry(self.root)
        self.email_entry.insert(0, self.customer.email)  
        self.email_entry.pack()

        # Địa chỉ
        tk.Label(self.root, text="Địa chỉ:").pack()
        self.address_entry = tk.Entry(self.root)
        self.address_entry.insert(0, self.customer.address)  
        self.address_entry.pack()

        # Nút cập nhật thông tin
        self.update_info_button = tk.Button(self.root, text="Cập nhật thông tin", command=self.update_customer_info)
        self.update_info_button.pack(pady=5)

        # Nút quay lại
        self.back_button = tk.Button(self.root, text="Quay lại", command=self.show_previous_screen)
        self.back_button.pack(pady=5)

    def update_customer_info(self):
    # Lưu thông tin 
        self.customer.phone = self.phone_entry.get()
        self.customer.email = self.email_entry.get()
        self.customer.address = self.address_entry.get()
    # Thông báo lưu thành công
        messagebox.showinfo("Thông báo", "Thông tin khách hàng đã được cập nhật thành công.")
    def show_previous_screen(self):
    # Quay lại dashboard khách hàng mà không cần lưu
        self.customer_selection_dashboard()
    def customer_selection_dashboard(self):
    # Hàm này hiển thị màn hình lựa chọn thông tin cá nhân và đặt hàng
        self.clear_screen()
        tk.Label(self.root, text="Màn hình lựa chọn", font=("Arial", 16)).pack(pady=10)

    # Các nút cho lựa chọn
        tk.Button(self.root, text="Thông tin cá nhân", command=self.customer_dashboard).pack(pady=5)
        tk.Button(self.root, text="Đặt hàng", command=self.order_dashboard).pack(pady=5)
    def order_dashboard(self):
        self.clear_screen()
        tk.Label(self.root, text="Danh sách sản phẩm", font=("Arial", 16)).pack(pady=10)

        self.product_listbox = tk.Listbox(self.root, height=5)
        for product in self.manager.product_list:
            self.product_listbox.insert(tk.END, f"{product.product_name} - {product.price} VND")
        self.product_listbox.pack()

        tk.Label(self.root, text="Số lượng:").pack()
        self.quantity_entry = tk.Entry(self.root)
        self.quantity_entry.pack()

        self.add_button = tk.Button(self.root, text="Thêm vào giỏ hàng", command=self.add_to_cart)
        self.add_button.pack()

        self.view_cart_button = tk.Button(self.root, text="Xem giỏ hàng", command=self.view_cart)
        self.view_cart_button.pack()

    def add_to_cart(self):
        try:
            selected_index = self.product_listbox.curselection()[0]
            selected_product = self.manager.product_list[selected_index]
            quantity = int(self.quantity_entry.get())

            self.customer.add_to_cart(selected_product, quantity)
            messagebox.showinfo("Thông báo", f"Đã thêm {quantity} {selected_product.product_name} vào giỏ hàng.")
        except IndexError:
            messagebox.showerror("Lỗi", "Vui lòng chọn một sản phẩm.")
        except ValueError:
            messagebox.showerror("Lỗi", "Vui lòng nhập số lượng hợp lệ.")

    def view_cart(self):
        cart_content = self.customer.view_cart()
        if cart_content:
            messagebox.showinfo("Giỏ hàng", cart_content)
        else:
            messagebox.showinfo("Giỏ hàng", "Giỏ hàng của bạn đang trống.")
    def on_customer_login(self):
        self.customer_dashboard()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def add_account(self):
        self.clear_screen()
        tk.Label(self.root, text="Thêm tài khoản", font=("Arial", 16)).pack(pady=10)

    # Nhập thông tin tài khoản
        tk.Label(self.root, text="Tên đăng nhập:").pack()
        self.new_username_entry = tk.Entry(self.root)
        self.new_username_entry.pack()

        tk.Label(self.root, text="Mật khẩu:").pack()
        self.new_password_entry = tk.Entry(self.root, show='*')
        self.new_password_entry.pack()

        tk.Label(self.root, text="Vai trò (quản lý/khách hàng):").pack()
        self.new_role_entry = tk.Entry(self.root)
        self.new_role_entry.pack()

        self.submit_account_button = tk.Button(self.root, text="Thêm", command=self.submit_add_account)
        self.submit_account_button.pack(pady=10)

        self.back_button = tk.Button(self.root, text="Quay lại", command=self.manage_accounts)
        self.back_button.pack(pady=5)

    def submit_add_account(self):
        username = self.new_username_entry.get()
        password = self.new_password_entry.get()
        role = self.new_role_entry.get()

    # Kiểm tra thông tin hợp lệ
        if username and password and role:
        # Thêm tài khoản mới vào danh sách tài khoản 
            new_account = User(username, password, role)  
            self.manager.add_account(new_account)  
            messagebox.showinfo("Thành công", "Tài khoản đã được thêm!")
            self.manage_accounts()
        else:
            messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin.")

    # Giao diện chính của Manager
    def manager_dashboard(self):
        self.clear_screen()
        tk.Label(self.root, text="Dashboard Quản lý", font=("Arial", 16)).pack(pady=10)

    # Các nút chức năng của manager
        tk.Button(self.root, text="Quản lý sản phẩm", command=self.manager_products).pack(pady=5)
        tk.Button(self.root, text="Quản lý khách hàng", command=self.view_customer_info).pack(pady=5)
        tk.Button(self.root, text="Quản lý đơn hàng", command=self.manager_orders).pack(pady=5)
        tk.Button(self.root, text="Quản lý kho", command=self.view_inventory).pack(pady=5)
        tk.Button(self.root, text="Thêm tài khoản", command = self.add_account).pack(pady=5)
        tk.Button(self.root, text="Đăng xuất", command=self.create_login_screen).pack(pady=5)

    def manage_products(self):
        self.clear_screen()
        tk.Label(self.root, text="Quản lý sản phẩm", font=("Arial", 16)).pack(pady=10)
    
    # Danh sách sản phẩm
        self.inventory_listbox = tk.Listbox(self.root, height=5)
        for product in self.manager.product_list:
            self.inventory_listbox.insert(tk.END, f"{product.product_name}: {product.quantity_in_stock} in stock")
        self.inventory_listbox.pack()
    
    # Thêm sản phẩm mới
        tk.Label(self.root, text="Thêm sản phẩm mới").pack()

        self.new_product_name_entry = tk.Entry(self.root)
        self.new_product_name_entry.insert(0, "Tên sản phẩm")
        self.new_product_name_entry.pack()

        self.new_product_price_entry = tk.Entry(self.root)
        self.new_product_price_entry.insert(0, "Giá sản phẩm")
        self.new_product_price_entry.pack()

        self.new_product_quantity_entry = tk.Entry(self.root)
        self.new_product_quantity_entry.insert(0, "Số lượng sản phẩm")
        self.new_product_quantity_entry.pack()

        self.add_product_button = tk.Button(self.root, text="Thêm sản phẩm", command=self.add_product)
        self.add_product_button.pack()

        # Sửa sản phẩm
        tk.Label(self.root, text="Sửa sản phẩm").pack()

        self.edit_product_id_entry = tk.Entry(self.root)
        self.edit_product_id_entry.insert(0, "ID sản phẩm cần sửa")
        self.edit_product_id_entry.pack()

        self.edit_product_name_entry = tk.Entry(self.root)
        self.edit_product_name_entry.insert(0, "Tên mới")
        self.edit_product_name_entry.pack()

        self.edit_product_price_entry = tk.Entry(self.root)
        self.edit_product_price_entry.insert(0, "Giá mới")
        self.edit_product_price_entry.pack()

        self.edit_product_quantity_entry = tk.Entry(self.root)
        self.edit_product_quantity_entry.insert(0, "Số lượng mới")
        self.edit_product_quantity_entry.pack()

        self.edit_product_button = tk.Button(self.root, text="Sửa sản phẩm", command=self.edit_product)
        self.edit_product_button.pack(pady=5)

    # Xóa sản phẩm
        tk.Label(self.root, text="Xóa sản phẩm").pack()

        self.delete_product_id_entry = tk.Entry(self.root)
        self.delete_product_id_entry.insert(0, "ID sản phẩm cần xóa")
        self.delete_product_id_entry.pack()

        self.delete_product_button = tk.Button(self.root, text="Xóa sản phẩm", command=self.delete_product)
        self.delete_product_button.pack(pady=5)
    


    def add_product(self):
        try:
            name = self.new_product_name_entry.get()
            price = int(self.new_product_price_entry.get())
            quantity = int(self.new_product_quantity_entry.get())
            product_id = len(self.manager.product_list) + 1
            new_product = Product(product_id, name, price, quantity)
            self.manager.add_product(new_product)
            self.manager_dashboard()
        except ValueError:
            messagebox.showerror("Lỗi", "Vui lòng nhập giá và số lượng hợp lệ.")

    # Xóa toàn bộ giao diện hiện tại
    def delete_product(self):
        try:
            selected_index = self.inventory_listbox.curselection()[0]
            selected_product = self.manager.product_list[selected_index]
            if self.manager.delete_product(selected_product.product_id):
                messagebox.showinfo("Thông báo", f"Đã xóa sản phẩm: {selected_product.product_name}")
                self.manage_products()  # Refresh the product list
            else:
                messagebox.showerror("Lỗi", "Không thể xóa sản phẩm.")
        except IndexError:
            messagebox.showerror("Lỗi", "Vui lòng chọn một sản phẩm để xóa.")

    # Thêm phương thức để sửa sản phẩm
    def edit_product(self):
        try:
            selected_index = self.inventory_listbox.curselection()[0]
            selected_product = self.manager.product_list[selected_index]

            # Lấy thông tin mới từ người dùng
            new_name = self.new_product_name_entry.get()
            new_price = float(self.new_product_price_entry.get())
            new_quantity = int(self.new_product_quantity_entry.get())

            if self.manager.edit_product(selected_product.product_id, new_name, new_price, new_quantity):
                messagebox.showinfo("Thông báo", f"Đã sửa sản phẩm: {selected_product.product_name}")
                self.manage_products()  # Refresh the product list
            else:
                messagebox.showerror("Lỗi", "Không thể sửa sản phẩm.")
        except (IndexError, ValueError):
            messagebox.showerror("Lỗi", "Vui lòng chọn một sản phẩm và nhập thông tin hợp lệ.")


# Chạy ứng dụng
if __name__ == "__main__":
    root = tk.Tk()
    app = StoreApp(root)
    root.mainloop()

