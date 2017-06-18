from flask import Flask, request

app = Flask(__name__)
app.config['DEBUG'] = True

form = """
<!doctype html>
<html>
    <body>
        <form action="/hello" method="POST">
            <label for="first_name">First Name</label>
            <input id="first_name" type="text" name="first_name">
            <input type="submit">
        </form>
    </body>
</html>
"""

time_form = """
    <style>
        .error {{ color: red; }}
    </style>
    <h1>Validation Time</h1>
    <form method="POST">
        <label>
            Hours (24-hour format)
            <input name="hours" type="text" value="{hours}">
        </label>
        <p class="error">{hours_error}</p>
        <label>
            Minutes
            <input name="minutes" type="text" value="{minutes}">
        </label>
        <p class="error">{minutes_error}</p>
        <input type="submit" value="Validate">
    </form>
"""

def is_integer(num):
    try:
        int(num)
        return True
    except ValueError:
        return False

def validate_hours(hours):
    hours, hours_error = hours, ""
    if not is_integer(hours):
            hours_error = "Not a valid integer"
            hours = ""
    else:
        hours = int(hours)
        if hours not in range(24):
            hours_error = "Hour value out of range (0-23)"
            hours = ""
    return hours, hours_error

def validate_minutes(minutes):
    minutes, minutes_error = minutes, ""
    if not is_integer(minutes):
        minutes_error = "Not a valid integer"
        minutes = ""
    else:
        minutes = int(minutes)
        if minutes not in range(60):
            minutes_error = "Minutes value out of range (0 - 59)"
            minutes = ""
    return minutes, minutes_error


@app.route("/")
def index():
    return form

@app.route("/hello", methods=['POST'])
def hello():
    first_name = request.form["first_name"]
    return "<h1>Hello, " + first_name + "!</h1>"


@app.route("/validate-time", methods=["GET", "POST"])
def validate_time():
    if request.method == "GET":
         return time_form.format(hours="", hours_error="", minutes="", minutes_error="")
    
    if request.method == "POST":
        hours, hours_error = validate_hours(request.form["hours"])
        minutes, minutes_error = validate_minutes(request.form["minutes"])
    
        if not minutes_error and not hours_error:
            return "Success!"
        else:
            return time_form.format(hours_error=hours_error, minutes_error=minutes_error, hours=hours, minutes=minutes)



app.run()