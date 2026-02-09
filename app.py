from flask import Flask, render_template, request, redirect, url_for
from access_control import grant_access, has_access, remaining_time
import random

app = Flask(__name__)


# Packages: price in KES, duration in minutes
PACKAGES = {
    "1_hour": {"label": "1 Hour", "price": 20, "minutes": 60},
    "24_hours": {"label": "24 Hours", "price": 80, "minutes": 1440},
    "3_days": {"label": "3 Days", "price": 200, "minutes": 4320},
}

# ----------------------
# Simulate M-Pesa Payment
# ----------------------
def simulate_mpesa_payment(phone, amount):
    """
    Simulate M-Pesa STK Push.
    Returns (success: bool, transaction ID)
    """
    txid = f"MPESA{random.randint(1000,9999)}"
    print(f"[MPESA SIM] Payment from {phone} for KES {amount} | TXID: {txid}")
    return True, txid

# ----------------------
# Routes
# ----------------------
@app.route("/")
def index():
    return render_template("index.html", packages=PACKAGES)

@app.route("/pay", methods=["POST"])
def pay():
    phone = request.form.get("phone")
    package = request.form.get("package")
    if not phone or not package or package not in PACKAGES:
        return "Invalid request", 400

    amount = PACKAGES[package]["price"]
    txid = f"MPESA{random.randint(1000,9999)}"

    # Grant access immediately (demo)
    mac_address = "DEMO-MAC-001"
    duration = PACKAGES[package]["minutes"]
    grant_access(mac_address, duration)

    # Show simulated STK push before success
    return render_template("stk_push.html", phone=phone, package=PACKAGES[package], txid=txid)

@app.route("/success")
def success():
    # Show success page (user already granted access)
    return render_template("success.html", txid="DEMO-TXID", package={"label": "Demo Package", "price": 0})

@app.route("/status")
def status():
    mac_address = "DEMO-MAC-001"
    if has_access(mac_address):
        remaining = remaining_time(mac_address)
        return f"✅ Access granted. Remaining time: {remaining}"
    else:
        return redirect(url_for("expired"))


@app.route("/time-left")
def time_left():
    mac_address = "DEMO-MAC-001"
    remaining = remaining_time(mac_address)

    if remaining is None:
        # If time expired, show 0 and mark as expired
        return render_template("time_left.html", total_seconds=0, expired=True)

    seconds = int(remaining.total_seconds())
    print("Remaining:", seconds)

    # Render the hourglass page with the total seconds
    return render_template("time_left.html", total_seconds=seconds, expired=False)


@app.route("/expired")
def expired():
    return render_template("expired.html")

# ----------------------
# Run the app
# ----------------------
if __name__ == "__main__":
    app.run(debug=True)

