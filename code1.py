import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

# Function to establish a database connection
def get_db_connection():
    return mysql.connector.connect(
        host=&quot;localhost&quot;,
        user=&quot;root&quot;,
        password=&quot;***********”
        database=&quot;hm&quot;
    )

# Function to fetch available rooms
def fetch_available_rooms():
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute(&quot;SELECT * FROM rooms WHERE status = &#39;available&#39;&quot;)
    rooms = cursor.fetchall()
    connection.close()
    return rooms

# Function to book a room
def book_room(room_id):
    connection = get_db_connection()
    cursor = connection.cursor()
   
    # Check if the room is available
    cursor.execute(&quot;SELECT status FROM rooms WHERE room_id = %s&quot;, (room_id,))
    result = cursor.fetchone()
   
    if not result:
        messagebox.showerror(&quot;Error&quot;, &quot;Room ID does not exist!&quot;)
    elif result[0] != &#39;available&#39;:
        messagebox.showerror(&quot;Error&quot;, &quot;This room is already booked or unavailable!&quot;)
    else:
        # Update room status to &#39;booked&#39;
        cursor.execute(&quot;UPDATE rooms SET status = &#39;booked&#39; WHERE room_id = %s&quot;, (room_id,))
        connection.commit()
        messagebox.showinfo(&quot;Success&quot;, f&quot;Room {room_id} has been successfully booked!&quot;)
   
    connection.close()
    display_available_rooms()

# Function to cancel a reservation
def cancel_reservation(room_id):
    connection = get_db_connection()
    cursor = connection.cursor()
   
    # Check if the room is booked
    cursor.execute(&quot;SELECT status FROM rooms WHERE room_id = %s&quot;, (room_id,))

    result = cursor.fetchone()
   
    if not result:
        messagebox.showerror(&quot;Error&quot;, &quot;Room ID does not exist!&quot;)
    elif result[0] != &#39;booked&#39;:
        messagebox.showerror(&quot;Error&quot;, &quot;This room is not currently booked!&quot;)
    else:
        # Update room status to &#39;available&#39;
        cursor.execute(&quot;UPDATE rooms SET status = &#39;available&#39; WHERE room_id = %s&quot;, (room_id,))
        # Delete associated reservation (if a reservations table exists)
        cursor.execute(&quot;DELETE FROM reservations WHERE room_id = %s&quot;, (room_id,))
        connection.commit()
        messagebox.showinfo(&quot;Success&quot;, f&quot;Reservation for Room {room_id} has been successfully canceled!&quot;)
   
    connection.close()
    display_available_rooms()

# Function to display available rooms in the GUI
def display_available_rooms():
    # Clear the tree view first
    for item in tree.get_children():
        tree.delete(item)
   
    # Fetch and display available rooms
    rooms = fetch_available_rooms()
    for room in rooms:
        tree.insert(&quot;&quot;, tk.END, values=room)

# Function to handle booking from the GUI
def on_book_room():
    try:
        room_id = int(room_id_entry.get())
        book_room(room_id)
    except ValueError:

        messagebox.showerror(&quot;Error&quot;, &quot;Please enter a valid Room ID.&quot;)

# Function to handle canceling a reservation
def on_cancel_reservation():
    try:
        room_id = int(cancel_room_id_entry.get())
        cancel_reservation(room_id)
    except ValueError:
        messagebox.showerror(&quot;Error&quot;, &quot;Please enter a valid Room ID.&quot;)

# GUI Setup
app = tk.Tk()
app.title(&quot;Hotel Management System&quot;)
app.geometry(&quot;700x500&quot;)

# Room booking input section
tk.Label(app, text=&quot;Enter Room ID to Book:&quot;).pack(pady=10)
room_id_entry = tk.Entry(app)
room_id_entry.pack(pady=5)

book_button = tk.Button(app, text=&quot;Book Room&quot;, command=on_book_room)
book_button.pack(pady=10)

# Cancel reservation input section
tk.Label(app, text=&quot;Enter Room ID to Cancel Reservation:&quot;).pack(pady=10)
cancel_room_id_entry = tk.Entry(app)
cancel_room_id_entry.pack(pady=5)

cancel_button = tk.Button(app, text=&quot;Cancel Reservation&quot;, command=on_cancel_reservation)
cancel_button.pack(pady=10)

# Available rooms display section
tk.Label(app, text=&quot;Available Rooms:&quot;).pack(pady=10)

columns = (&quot;Room ID&quot;, &quot;Type&quot;, &quot;Price&quot;, &quot;Status&quot;)
tree = ttk.Treeview(app, columns=columns, show=&quot;headings&quot;)
for col in columns:
    tree.heading(col, text=col)
tree.pack(fill=tk.BOTH, expand=True)

# Initial display of available rooms
display_available_rooms()

app.mainloop()