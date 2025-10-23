# for pushing changes to github
""" 
 git add .
 git commit -m "add more output details"
 git push origin main

"""
"""
# for pulling changes from github

cd ~/emf-toolkit
git fetch origin
git reset --hard origin/main


"""

# Activate virtual environment
# venv\Scripts\activate

from flask import Flask, render_template, request
from controllers import process_form_request
app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():
    button, input, output, input_type = process_form_request(request)
    return render_template(
        "index.html",
        button_section=button,
        input_to_jinja=input,
        output_to_jinja=output,
        input_type=input_type
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
