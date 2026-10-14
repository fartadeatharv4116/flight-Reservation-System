"""
DSL Mini-Project: Implementation of Flight Reservation System
Student: Fartade Atharv Parmeshwar | Class: SE-C | Roll No.: SECCOMP89

Concepts demonstrated:
- Linear Search by Flight ID, flight name, source, or destination
- Binary Search by Flight ID (on a sorted copy of flight records)
- Bubble Sort by ticket price (ascending/descending)
- Operation counts for comparisons/swaps (educational step count)

Run: python main.py
Python 3.x; Tkinter is included with most standard Python installations.
"""
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from dataclasses import dataclass
from typing import List, Optional, Tuple


@dataclass
class Flight:
    flight_id: str
    name: str
    source: str
    destination: str
    departure: str
    price: int
    seats: int = 20


def sample_flights() -> List[Flight]:
    """Sample/demo data; not connected to a real airline or booking service."""
    return [
        Flight("FL101", "Deccan Air", "Pune", "Delhi", "06:30", 4500, 18),
        Flight("FL102", "Sky Maharashtra", "Pune", "Mumbai", "08:15", 1800, 15),
        Flight("FL103", "Indigo Demo", "Mumbai", "Bengaluru", "09:40", 3800, 12),
        Flight("FL104", "Western Wings", "Pune", "Goa", "11:20", 2500, 20),
        Flight("FL105", "Deccan Air", "Delhi", "Pune", "13:05", 4700, 10),
        Flight("FL106", "Sky Maharashtra", "Pune", "Hyderabad", "14:30", 3200, 16),
        Flight("FL107", "Indigo Demo", "Mumbai", "Delhi", "16:00", 4200, 8),
        Flight("FL108", "Western Wings", "Pune", "Nashik", "17:10", 1500, 14),
        Flight("FL109", "Deccan Air", "Bengaluru", "Pune", "18:25", 3900, 11),
        Flight("FL110", "Sky Maharashtra", "Pune", "Chennai", "19:15", 3600, 17),
        Flight("FL111", "Indigo Demo", "Goa", "Pune", "20:05", 2700, 9),
        Flight("FL112", "Western Wings", "Pune", "Kolkata", "21:30", 5200, 6),
    ]


def linear_search(flights: List[Flight], query: str) -> Tuple[List[Flight], int]:
    """Case-insensitive substring search over ID, name, source and destination."""
    query = query.strip().casefold()
    comparisons = 0
    if not query:
        return flights.copy(), comparisons
    found = []
    for flight in flights:
        comparisons += 1
        fields = (flight.flight_id, flight.name, flight.source, flight.destination)
        if any(query in value.casefold() for value in fields):
            found.append(flight)
    return found, comparisons


def binary_search_flight_id(flights: List[Flight], flight_id: str) -> Tuple[Optional[Flight], int]:
    """Binary search for exact Flight ID. A sorted copy is made so the display order is unchanged."""
    ordered = sorted(flights, key=lambda f: f.flight_id.casefold())
    low, high = 0, len(ordered) - 1
    comparisons = 0
    target = flight_id.strip().casefold()
    while low <= high:
        mid = (low + high) // 2
        comparisons += 1
        current = ordered[mid].flight_id.casefold()
        if current == target:
            return ordered[mid], comparisons
        if current < target:
            low = mid + 1
        else:
            high = mid - 1
    return None, comparisons


def bubble_sort_by_price(flights: List[Flight], descending: bool = False) -> Tuple[List[Flight], int, int]:
    """Return a sorted copy, plus comparison and swap counts."""
    result = flights.copy()
    comparisons = swaps = 0
    n = len(result)
    for i in range(n - 1):
        swapped = False
        for j in range(0, n - i - 1):
            comparisons += 1
            left, right = result[j].price, result[j + 1].price
            should_swap = left < right if descending else left > right
            if should_swap:
                result[j], result[j + 1] = result[j + 1], result[j]
                swaps += 1
                swapped = True
        if not swapped:
            break
    return result, comparisons, swaps


class FlightReservationApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Flight Reservation System | DSL Mini-Project")
        self.root.geometry("1100x650")
        self.root.minsize(900, 560)
        self.flights = sample_flights()
        self.visible_flights = self.flights.copy()
        self.bookings = []
        self.last_step_message = "Ready. Sample data is used; no real ticket is issued."
        self._build_ui()
        self._refresh_table(self.visible_flights)

    def _build_ui(self):
        self.root.configure(bg="#f3f6fa")
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        style.configure("Treeview", rowheight=28, font=("Arial", 10))
        style.configure("Treeview.Heading", font=("Arial", 10, "bold"))
        style.configure("TButton", font=("Arial", 10), padding=6)

        header = tk.Frame(self.root, bg="#12304a", padx=18, pady=14)
        header.pack(fill="x")
        tk.Label(header, text="✈  FLIGHT RESERVATION SYSTEM", bg="#12304a",
                 fg="white", font=("Arial", 19, "bold")).pack(anchor="w")
        tk.Label(header, text="DSL Mini-Project | Searching and Sorting",
                 bg="#12304a", fg="#d8e7f5", font=("Arial", 10)).pack(anchor="w", pady=(4, 0))

        controls = ttk.LabelFrame(self.root, text="Search and Sort Flights", padding=12)
        controls.pack(fill="x", padx=16, pady=(14, 8))
        ttk.Label(controls, text="Search by ID / airline / source / destination:").grid(row=0, column=0, sticky="w")
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(controls, textvariable=self.search_var, width=34)
        search_entry.grid(row=0, column=1, padx=8, sticky="w")
        search_entry.bind("<Return>", lambda _event: self.search_flights())
        ttk.Button(controls, text="Linear Search", command=self.search_flights).grid(row=0, column=2, padx=4)
        ttk.Button(controls, text="Binary Search by ID", command=self.binary_search).grid(row=0, column=3, padx=4)
        ttk.Button(controls, text="Sort Price ↑", command=lambda: self.sort_prices(False)).grid(row=0, column=4, padx=4)
        ttk.Button(controls, text="Sort Price ↓", command=lambda: self.sort_prices(True)).grid(row=0, column=5, padx=4)
        ttk.Button(controls, text="Show All", command=self.show_all).grid(row=0, column=6, padx=4)

        table_frame = ttk.LabelFrame(self.root, text="Available Demo Flights", padding=8)
        table_frame.pack(fill="both", expand=True, padx=16, pady=8)
        columns = ("id", "name", "source", "destination", "departure", "price", "seats")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", selectmode="browse")
        headings = {
            "id": "Flight ID", "name": "Airline", "source": "From",
            "destination": "To", "departure": "Departure", "price": "Price (INR)", "seats": "Seats"
        }
        widths = {"id": 85, "name": 150, "source": 105, "destination": 110, "departure": 95, "price": 110, "seats": 75}
        for col in columns:
            self.tree.heading(col, text=headings[col])
            self.tree.column(col, width=widths[col], anchor="center")
        yscroll = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=yscroll.set)
        self.tree.pack(side="left", fill="both", expand=True)
        yscroll.pack(side="right", fill="y")

        bottom = tk.Frame(self.root, bg="#f3f6fa", padx=16, pady=8)
        bottom.pack(fill="x")
        ttk.Button(bottom, text="Reserve Selected Flight", command=self.reserve_flight).pack(side="left")
        ttk.Button(bottom, text="View Bookings", command=self.view_bookings).pack(side="left", padx=8)
        self.status_var = tk.StringVar(value=self.last_step_message)
        tk.Label(bottom, textvariable=self.status_var, bg="#f3f6fa", fg="#334155",
                 font=("Arial", 9), anchor="w", justify="left", wraplength=650).pack(side="left", padx=14)

    def _refresh_table(self, flights: List[Flight]):
        self.visible_flights = flights.copy()
        for item in self.tree.get_children():
            self.tree.delete(item)
        for flight in flights:
            self.tree.insert("", "end", iid=flight.flight_id, values=(
                flight.flight_id, flight.name, flight.source, flight.destination,
                flight.departure, f"₹{flight.price:,}", flight.seats
            ))
        self.status_var.set(f"Showing {len(flights)} flight(s). {self.last_step_message}")

    def search_flights(self):
        query = self.search_var.get().strip()
        if not query:
            messagebox.showinfo("Search", "Enter a Flight ID, airline, source, or destination.")
            return
        found, steps = linear_search(self.flights, query)
        self.last_step_message = f"Linear Search: {steps} flight-record checks."
        self._refresh_table(found)
        if found:
            self.status_var.set(f"Found {len(found)} result(s). {self.last_step_message}")
        else:
            messagebox.showinfo("No Results", "No matching flight was found.")
            self.status_var.set(f"No match. {self.last_step_message}")

    def binary_search(self):
        query = self.search_var.get().strip()
        if not query:
            messagebox.showinfo("Binary Search", "Enter an exact Flight ID, e.g. FL105.")
            return
        result, steps = binary_search_flight_id(self.flights, query)
        self.last_step_message = f"Binary Search: {steps} midpoint comparison(s)."
        self._refresh_table([result] if result else [])
        if result:
            self.status_var.set(f"Flight ID found: {result.flight_id}. {self.last_step_message}")
        else:
            messagebox.showinfo("No Results", "Flight ID not found. Use an exact ID such as FL105.")
            self.status_var.set(f"No match. {self.last_step_message}")

    def sort_prices(self, descending: bool):
        ordered, comparisons, swaps = bubble_sort_by_price(self.flights, descending)
        direction = "high to low" if descending else "low to high"
        self.last_step_message = (
            f"Bubble Sort ({direction}): {comparisons} comparison(s), {swaps} swap(s)."
        )
        self._refresh_table(ordered)

    def show_all(self):
        self.search_var.set("")
        self.last_step_message = "Showing the complete demo flight list."
        self._refresh_table(self.flights)

    def reserve_flight(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Select Flight", "Select a flight from the table first.")
            return
        flight_id = selected[0]
        flight = next((f for f in self.flights if f.flight_id == flight_id), None)
        if flight is None:
            return
        if flight.seats <= 0:
            messagebox.showwarning("No Seats", "No demo seats are available on this flight.")
            return
        passenger = simpledialog.askstring("Passenger Details", "Enter passenger name:", parent=self.root)
        if not passenger or not passenger.strip():
            return
        flight.seats -= 1
        booking = {
            "booking_id": f"BK{len(self.bookings) + 1:03d}",
            "passenger": passenger.strip(),
            "flight_id": flight.flight_id,
            "route": f"{flight.source} → {flight.destination}",
            "price": flight.price,
        }
        self.bookings.append(booking)
        self._refresh_table(self.visible_flights)
        messagebox.showinfo(
            "Demo Booking Confirmed",
            f"Booking ID: {booking['booking_id']}\nPassenger: {booking['passenger']}\n"
            f"Flight: {flight.flight_id}\nRoute: {booking['route']}\n"
            f"Demo fare: ₹{flight.price:,}\n\nThis is a local demonstration only; no real ticket was issued."
        )
        self.status_var.set(f"Demo booking {booking['booking_id']} saved in memory. No real ticket issued.")

    def view_bookings(self):
        if not self.bookings:
            messagebox.showinfo("Bookings", "No demo bookings have been made in this session.")
            return
        lines = []
        for b in self.bookings:
            lines.append(f"{b['booking_id']} | {b['passenger']} | {b['flight_id']} | {b['route']} | ₹{b['price']:,}")
        messagebox.showinfo("Demo Bookings", "\n".join(lines))

def main():
    root = tk.Tk()
    FlightReservationApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
