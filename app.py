# for pushing changes to github
""" 
 git add .
 git commit -m "add charge description to output and remove js code"
 git push origin main
"""
# Activate virtual environment
# venv\Scripts\activate

# flask run --host 0.0.0.0
# python -m pip install numpy
# "python -m" ensures pip installs it for the exact python interpreter

from flask import Flask, render_template, request
import threading
import webview
from controllers import process_input, static_var
app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        # Sidebar buttons
        if "button" in request.form:
            btn = request.form.get("button")
            static_var.button = btn if btn in [
                "button_one", "button_two", "button_three"] else "Unknown button"

        # Input type select
        elif "input_type" in request.form:
            input_type = request.form.get("input_type")
            static_var.input_type = input_type if input_type in [
                "two vectors with c", "two vectors without c", "single vector"] else "two vectors with c"

        # Vector input fields
        elif "input_x1" in request.form:  # detect vector submission
            static_var.output, static_var.input = process_input(
                request, static_var.input_type)

    return render_template(
        "index.html",
        button_section=static_var.button,
        input_to_jinja=static_var.input,
        output_to_jinja=static_var.output,
        input_type=static_var.input_type
    )


def run_flask():
    # IMP:disable debug for production build
    app.run(debug=True, use_reloader=True)


if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=5000)

    # # Start Flask in background thread
    # flask_thread = threading.Thread(target=run_flask)
    # flask_thread.daemon = True
    # flask_thread.start()

    # # Open PyWebView window
    # webview.create_window(
    #     "EMF App", "http://127.0.0.1:5000", width=1200, height=800)
    # webview.start()
