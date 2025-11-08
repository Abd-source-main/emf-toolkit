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
from sketch import sketch_cartesian

app = Flask(__name__)
skc = sketch_cartesian()


@app.route("/", methods=["GET", "POST"])
def home():
    button, input, output, input_type = ctrl.process_form_request_home(request)
    if button == "cartesian":
        ctrl.static_var.button = "home"
        return redirect('/cartesian_sketch')
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
    plot_html = skc.create_cartesian_sketch(strdata=data)
    return render_template("sketch.html",
                           plot_html=plot_html)


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
