import mysql.connector
from mysql.connector import Error

# ---------------- DATABASE SETTINGS ----------------
HOST = "localhost"
USER = "root"
PASSWORD = "MySQL@12345"
DATABASE = "inventory_management"


# ---------------- DATABASE CONNECTION ----------------
def create_database():
    try:
        connection = mysql.connector.connect(
            host=HOST,
            user=USER,
            password=PASSWORD
        )

        cursor = connection.cursor()
        cursor.execute(
            "CREATE DATABASE IF NOT EXISTS inventory_management"
        )

        cursor.close()
        connection.close()

        print("Database created successfully.")

    except Error as e:
        print("Database Error:", e)


def connect_database():
    try:
        connection = mysql.connector.connect(
            host=HOST,
            user=USER,
            password=PASSWORD,
            database=DATABASE
        )
        return connection

    except Error as e:
        print("Connection Error:", e)
        return None


# ---------------- CREATE TABLE ----------------
def create_table():
    connection = connect_database()

    if connection is None:
        return

    cursor = connection.cursor()

    query = """
    CREATE TABLE IF NOT EXISTS products (
        product_id INT PRIMARY KEY,
        product_name VARCHAR(100) NOT NULL,
        category VARCHAR(50),
        price DECIMAL(10,2),
        quantity INT,
        supplier VARCHAR(100)
    )
    """

    cursor.execute(query)
    connection.commit()

    cursor.close()
    connection.close()


# ---------------- ADD PRODUCT ----------------
def add_product():
    connection = connect_database()

    if connection is None:
        return

    cursor = connection.cursor()

    try:
        product_id = int(input("Enter Product ID: "))
        product_name = input("Enter Product Name: ")
        category = input("Enter Category: ")
        price = float(input("Enter Price: "))
        quantity = int(input("Enter Quantity: "))
        supplier = input("Enter Supplier Name: ")

        query = """
        INSERT INTO products
        (product_id, product_name, category, price, quantity, supplier)
        VALUES (%s, %s, %s, %s, %s, %s)
        """

        values = (
            product_id,
            product_name,
            category,
            price,
            quantity,
            supplier
        )

        cursor.execute(query, values)
        connection.commit()

        print("Product added successfully.")

    except Error as e:
        print("Error:", e)

    except ValueError:
        print("Please enter valid numbers.")

    finally:
        cursor.close()
        connection.close()


# ---------------- DISPLAY PRODUCTS ----------------
def display_products():
    connection = connect_database()

    if connection is None:
        return

    cursor = connection.cursor()

    cursor.execute("SELECT * FROM products")
    records = cursor.fetchall()

    if len(records) == 0:
        print("No products found.")

    else:
        print("\n" + "=" * 100)
        print(
            "{:<10} {:<25} {:<18} {:<12} {:<10} {:<20}".format(
                "ID",
                "Product Name",
                "Category",
                "Price",
                "Quantity",
                "Supplier"
            )
        )
        print("=" * 100)

        for row in records:
            print(
                "{:<10} {:<25} {:<18} {:<12} {:<10} {:<20}".format(
                    row[0],
                    row[1],
                    row[2],
                    row[3],
                    row[4],
                    row[5]
                )
            )

        print("=" * 100)

    cursor.close()
    connection.close()


# ---------------- SEARCH PRODUCT ----------------
def search_product():
    connection = connect_database()

    if connection is None:
        return

    cursor = connection.cursor()

    keyword = input("Enter Product Name to Search: ")

    query = """
    SELECT * FROM products
    WHERE product_name LIKE %s
    """

    cursor.execute(query, ("%" + keyword + "%",))
    records = cursor.fetchall()

    if len(records) == 0:
        print("Product not found.")

    else:
        print("\nSearch Results:")
        print("-" * 80)

        for row in records:
            print("Product ID :", row[0])
            print("Product Name:", row[1])
            print("Category   :", row[2])
            print("Price      :", row[3])
            print("Quantity   :", row[4])
            print("Supplier   :", row[5])
            print("-" * 80)

    cursor.close()
    connection.close()


# ---------------- UPDATE PRODUCT ----------------
def update_product():
    connection = connect_database()

    if connection is None:
        return

    cursor = connection.cursor()

    try:
        product_id = int(input("Enter Product ID to Update: "))

        cursor.execute(
            "SELECT * FROM products WHERE product_id = %s",
            (product_id,)
        )

        record = cursor.fetchone()

        if record is None:
            print("Product not found.")
            return

        print("Leave field blank to keep old value.")

        name = input("Enter New Product Name: ")
        category = input("Enter New Category: ")
        price = input("Enter New Price: ")
        quantity = input("Enter New Quantity: ")
        supplier = input("Enter New Supplier: ")

        if name == "":
            name = record[1]

        if category == "":
            category = record[2]

        if price == "":
            price = record[3]
        else:
            price = float(price)

        if quantity == "":
            quantity = record[4]
        else:
            quantity = int(quantity)

        if supplier == "":
            supplier = record[5]

        query = """
        UPDATE products
        SET product_name = %s,
            category = %s,
            price = %s,
            quantity = %s,
            supplier = %s
        WHERE product_id = %s
        """

        values = (
            name,
            category,
            price,
            quantity,
            supplier,
            product_id
        )

        cursor.execute(query, values)
        connection.commit()

        print("Product updated successfully.")

    except ValueError:
        print("Please enter valid numbers.")

    except Error as e:
        print("Error:", e)

    finally:
        cursor.close()
        connection.close()


# ---------------- DELETE PRODUCT ----------------
def delete_product():
    connection = connect_database()

    if connection is None:
        return

    cursor = connection.cursor()

    try:
        product_id = int(input("Enter Product ID to Delete: "))

        cursor.execute(
            "SELECT * FROM products WHERE product_id = %s",
            (product_id,)
        )

        record = cursor.fetchone()

        if record is None:
            print("Product not found.")
            return

        confirm = input(
            "Are you sure you want to delete this product? (yes/no): "
        )

        if confirm.lower() == "yes":

            cursor.execute(
                "DELETE FROM products WHERE product_id = %s",
                (product_id,)
            )

            connection.commit()

            print("Product deleted successfully.")

        else:
            print("Delete operation cancelled.")

    except ValueError:
        print("Please enter a valid Product ID.")

    except Error as e:
        print("Error:", e)

    finally:
        cursor.close()
        connection.close()


# ---------------- ADD STOCK ----------------
def add_stock():
    connection = connect_database()

    if connection is None:
        return

    cursor = connection.cursor()

    try:
        product_id = int(input("Enter Product ID: "))
        quantity = int(input("Enter Quantity to Add: "))

        if quantity <= 0:
            print("Quantity must be greater than zero.")
            return

        cursor.execute(
            "SELECT quantity FROM products WHERE product_id = %s",
            (product_id,)
        )

        record = cursor.fetchone()

        if record is None:
            print("Product not found.")
            return

        new_quantity = record[0] + quantity

        cursor.execute(
            """
            UPDATE products
            SET quantity = %s
            WHERE product_id = %s
            """,
            (new_quantity, product_id)
        )

        connection.commit()

        print("Stock added successfully.")
        print("New Quantity:", new_quantity)

    except ValueError:
        print("Please enter valid numbers.")

    except Error as e:
        print("Error:", e)

    finally:
        cursor.close()
        connection.close()


# ---------------- SELL PRODUCT ----------------
def sell_product():
    connection = connect_database()

    if connection is None:
        return

    cursor = connection.cursor()

    try:
        product_id = int(input("Enter Product ID: "))
        quantity = int(input("Enter Quantity Sold: "))

        if quantity <= 0:
            print("Quantity must be greater than zero.")
            return

        cursor.execute(
            "SELECT quantity FROM products WHERE product_id = %s",
            (product_id,)
        )

        record = cursor.fetchone()

        if record is None:
            print("Product not found.")
            return

        current_quantity = record[0]

        if quantity > current_quantity:
            print("Not enough stock available.")
            print("Available Stock:", current_quantity)
            return

        new_quantity = current_quantity - quantity

        cursor.execute(
            """
            UPDATE products
            SET quantity = %s
            WHERE product_id = %s
            """,
            (new_quantity, product_id)
        )

        connection.commit()

        print("Sale recorded successfully.")
        print("Remaining Stock:", new_quantity)

    except ValueError:
        print("Please enter valid numbers.")

    except Error as e:
        print("Error:", e)

    finally:
        cursor.close()
        connection.close()


# ---------------- LOW STOCK PRODUCTS ----------------
def low_stock():
    connection = connect_database()

    if connection is None:
        return

    cursor = connection.cursor()

    try:
        limit = int(input("Show products with quantity less than or equal to: "))

        cursor.execute(
            """
            SELECT * FROM products
            WHERE quantity <= %s
            """,
            (limit,)
        )

        records = cursor.fetchall()

        if len(records) == 0:
            print("No low-stock products found.")

        else:
            print("\nLOW STOCK PRODUCTS")
            print("-" * 80)

            for row in records:
                print(
                    "ID:", row[0],
                    "| Name:", row[1],
                    "| Category:", row[2],
                    "| Quantity:", row[4]
                )

            print("-" * 80)

    except ValueError:
        print("Please enter a valid number.")

    except Error as e:
        print("Error:", e)

    finally:
        cursor.close()
        connection.close()


# ---------------- MAIN MENU ----------------
def main():

    create_database()
    create_table()

    while True:

        print("\n")
        print("=" * 60)
        print("       INVENTORY MANAGEMENT SYSTEM")
        print("=" * 60)

        print("1. Add Product")
        print("2. Display All Products")
        print("3. Search Product")
        print("4. Update Product")
        print("5. Delete Product")
        print("6. Add Stock")
        print("7. Sell Product")
        print("8. Low Stock Products")
        print("9. Exit")

        print("=" * 60)

        choice = input("Enter your choice: ")

        if choice == "1":
            add_product()

        elif choice == "2":
            display_products()

        elif choice == "3":
            search_product()

        elif choice == "4":
            update_product()

        elif choice == "5":
            delete_product()

        elif choice == "6":
            add_stock()

        elif choice == "7":
            sell_product()

        elif choice == "8":
            low_stock()

        elif choice == "9":
            print("Thank you for using Inventory Management System.")
            break

        else:
            print("Invalid choice. Please try again.")


# ---------------- START PROGRAM ----------------
if __name__ == "__main__":
    main()
