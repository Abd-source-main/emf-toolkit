# for pushing changes to github
""" 
 git add .
 git commit -m "just shorted the requirment"
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

from flask import Flask, render_template, request, redirect
import controllers as ctrl
from sketch import Sketch_cartesian

app = Flask(__name__)
skc = Sketch_cartesian()


@app.route("/", methods=["GET", "POST"])
def home():
    button, input, output, input_type = ctrl.process_form_request_home(request)
    if button in ["cartesian", "cylindrical", "spherical"]:
        ctrl.static_var.button = "home"
        return redirect(f'/{button}_sketch')
    return render_template(
        "index.html",
        button_section=button,
        input_to_jinja=input,
        output_to_jinja=output,
        input_type=input_type,
    )


@app.route("/cartesian_sketch", methods=["GET", "POST"])
def cartesian_sketch():
    global skc
    data = ctrl.process_form_sketch(request)
    if data == ["reset"]:
        skc.reinitialize(is_first_time=True)
        data.clear()
    elif data and data[0] in ["cartesian", "cylindrical", "spherical"]:
        return redirect(f'/{data[0]}_sketch')
    plot_html = skc.create_cartesian_sketch(strdata=data)
    return render_template("sketch.html",
                           system="cartesian",
                           plot_html=plot_html)


@app.route("/cylindrical_sketch", methods=["GET", "POST"])
def cylindrical_sketch():
    return "cylindrical sketch page"


@app.route("/spherical_sketch", methods=["GET", "POST"])
def spherical_sketch():
    return "spherical sketch page"


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
