"""
pyinstaller --onefile --noconsole  --add-data "templates;templates" --add-data "static;static" app.py


"""


# Activate virtual environment
# venv\Scripts\activate

from controllers import ProcessForm, static_var
import physics_applications as pa
from flask import Flask, flash, render_template, request, redirect
import threading
from sketch import Sketch_controller
import webview

app = Flask(__name__)
app.secret_key = 'ruIUEcBFieu#79407:+34rkd,q'
sk = Sketch_controller()


@app.route("/", methods=["GET", "POST"])
def home():
    button, input, output, input_type = ProcessForm.process_form_request_home(
        request)

    """ redirecting """
    if button in ["cartesian", "cylindrical", "spherical"]:
        static_var.button = "home"
        return redirect(f'/{button}_sketch')
    elif button == "button_three":
        static_var.button = "home"
        return redirect("/physics")
    """ end of redirecting """

    return render_template(
        "index.html",
        button_section=button,
        input_to_jinja=input,
        output_to_jinja=output,
        input_type=input_type,
    )


@app.route("/cartesian_sketch", methods=["GET", "POST"])
def cartesian_sketch():
    global sk
    data = ProcessForm.process_form_sketch(request)
    if data == ["reset"]:
        sk.reinitialize_cartesian(is_like_first_time=True)
        data.clear()
    elif data and data[0] in ["cartesian", "cylindrical", "spherical"]:
        return redirect(f'/{data[0]}_sketch')
    plot_html = sk.create_cartesian_sketch(strdata=data)
    return render_template("sketch.html",
                           system="cartesian",
                           plot_html=plot_html)


@app.route("/cylindrical_sketch", methods=["GET", "POST"])
def cylindrical_sketch():
    data = ProcessForm.process_form_sketch(request)
    if data == ["reset"]:
        sk.reinitialize_cylindrical(is_like_first_time=True)
        data.clear()
    if data and data[0] in ["cartesian", "cylindrical", "spherical"]:
        return redirect(f'/{data[0]}_sketch')
    plot_html = sk.create_cylindrical_sketch(strdata=data)
    return render_template("sketch.html",
                           system="cylindrical",
                           plot_html=plot_html)


@app.route("/spherical_sketch", methods=["GET", "POST"])
def spherical_sketch():
    data = ProcessForm.process_form_sketch(request)

    if data and data[0] in ["cartesian", "cylindrical", "spherical"]:
        return redirect(f'/{data[0]}_sketch')
    return render_template("sketch.html",
                           system="spherical",
                           plot_html="<h3>Spherical sketch page under construction.</h3>")


@app.route("/physics", methods=["GET", "POST"])
def button_three():
    input_charge = None
    output = None
    var, action = ProcessForm.process_form_physics(request)
    if action == 'dict_input':
        input_charge = var
        pa.Session.save_charge(input_charge)
    elif 'calculate_effect':
        output = var
    charges = pa.Session.get_charges()
    return render_template("physics.html", input_charge=input_charge,
                           charges=charges,
                           output=output
                           )


def run_flask():
    # IMP:disable debug for production build
    app.run(debug=True, use_reloader=True)


if __name__ == "__main__":
    # uncomment to for final product
    run_flask()

    # # Start Flask in background thread
    # flask_thread = threading.Thread(target=run_flask)
    # flask_thread.daemon = True
    # flask_thread.start()

    # # Open PyWebView window
    # webview.create_window(
    #     "EMF App", "http://127.0.0.1:5000", width=1200, height=800)
    # webview.start()
