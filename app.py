from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# ── 36 seats setup ──
seats = {}
for row in range(1, 10):
    for col in ['A', 'B', 'C', 'D']:
        seat_id = f"{row}{col}"
        seats[seat_id] = "available"

# ── Ticket price logic ──
def get_price(passenger_type):
    if passenger_type == "child":
        return 40
    elif passenger_type == "adult":
        return 80
    elif passenger_type == "senior":
        return round(80 - (80 * 0.15))
    return 0

# ── Routes ──
@app.route("/")
def index():
    return render_template("index.html", seats=seats)

@app.route("/book", methods=["POST"])
def book():
    data = request.json
    seat = data["seat"]
    passenger_type = data["type"]

    if seats[seat] == "booked":
        return jsonify({"success": False, "message": "Seat already booked!"})

    seats[seat] = "booked"
    price = get_price(passenger_type)
    return jsonify({"success": True, "message": f"Seat {seat} booked! Price: Rs.{price}"})

@app.route("/cancel", methods=["POST"])
def cancel():
    data = request.json
    seat = data["seat"]

    if seats[seat] == "available":
        return jsonify({"success": False, "message": "Seat is not booked!"})

    seats[seat] = "available"
    return jsonify({"success": True, "message": f"Seat {seat} cancelled successfully!"})

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=10000)