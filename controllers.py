from my_utils import *

# To have similar to a static variable in c++


class static_var:
    button = "home"
    output = []
    input = []
    input_type = "two vectors with c"


def to_list_and_round_for_output(v):
    # convert Vector or np.array to a plain list of floats rounded to 3 decimal places
    if isinstance(v, Vector):
        return [float(round(x, 3)) for x in v.xyz]   # unpack Vector
    elif isinstance(v, np.ndarray):
        return [float(round(x, 3)) for x in v]        # unpack NumPy array
    elif isinstance(v, list):
        return [float(round(x, 3)) for x in v]        # unpack list
    elif isinstance(v, str):
        return v
    else:
        return round(v, 3)


def process_input(request, input_type):
    x1 = float(request.form.get("input_x1")
               )if request.form.get("input_x1") else 0
    y1 = float(request.form.get("input_y1")
               )if request.form.get("input_y1") else 0
    z1 = float(request.form.get("input_z1")
               )if request.form.get("input_z1") else 0
    v1 = Vector(x1, y1, z1)
    unit1 = v1.unit_vector()
    mag1 = v1.magnitude()
    if input_type == "single vector":
        static_var.input = [*v1.xyz]
        static_var.output = [
            f"unit vector of vector1: {to_list_and_round_for_output(unit1)}",
            f"magnitude of vector1: {to_list_and_round_for_output(mag1)}"
        ]
    elif input_type == "two vectors without c" or input_type == "two vectors with c":
        # GET INPUT
        x2 = float(request.form.get("input_x2")
                   )if request.form.get("input_x2") else 0
        y2 = float(request.form.get("input_y2")
                   )if request.form.get("input_y2") else 0
        z2 = float(request.form.get("input_z2")
                   )if request.form.get("input_z2") else 0
        v2 = Vector(x2, y2, z2)
        # do output
        unit2 = v2.unit_vector()
        mag2 = v2.magnitude()
        v12 = vector_12(v1, v2)
        mag = v12.magnitude()
        unit = v12.unit_vector()
        cross_prod = cross(v1, v2)
        dot_prod = dot(v1, v2)

        if input_type == "two vectors with c":
            # get input
            c2 = float(request.form.get("input_c2")
                       )if request.form.get("input_c2") else 0
            c1 = float(request.form.get("input_c1")
                       )if request.form.get("input_c1") else 0
            v1.set_charge(c1)
            v2.set_charge(c2)
            # do output
            f = electric_force(v1, v2, v1.charge, v2.charge)
            e = electrical_field(v1, v2, v1.charge)
            v = electrical_potential(v1, v2, v1.charge)
            flux = flux_density(v1, v2, v1.charge)
    else:
        return ["Select an input type"], []
    # prepare output
    # FOR jinja its x1,y1,z1,c1,x2,y2,z2,c2 in order
    if input_type == "two vectors with c":
        static_var.input = [*v1.xyz, v1.charge, *v2.xyz, v2.charge]
        static_var.output = [
            f"vector2 - vector1: {to_list_and_round_for_output(v12)}",
            f"vector1 + vector2: {to_list_and_round_for_output(v1.nxyz + v2.nxyz)}",
            f"magnitude of vector12: {to_list_and_round_for_output(mag)}",
            f"unit vector of vector12: {to_list_and_round_for_output(unit)}",
            f"force vector of vector12: {to_list_and_round_for_output(f)}",
            f"electric field vector of vector12: {to_list_and_round_for_output(e)}",
            f"potential vector of vector12: {to_list_and_round_for_output(v)}",
            f"flux vector of vector12: {to_list_and_round_for_output(flux)}",
            f"cross product vector of vector12: {to_list_and_round_for_output(cross_prod)}",
            f"dot product vector of vector12: {to_list_and_round_for_output(dot_prod)}",
            f"unit vector of vector1: {to_list_and_round_for_output(unit1)}",
            f"unit vector of vector2: {to_list_and_round_for_output(unit2)}",
            f"magnitude of vector1: {to_list_and_round_for_output(mag1)}",
            f"magnitude of vector2: {to_list_and_round_for_output(mag2)}"
        ]
    elif input_type == "two vectors without c":
        static_var.input = [*v1.xyz, *v2.xyz]
        static_var.output = [
            f"vector2 - vector1: {to_list_and_round_for_output(v12)}",
            f"vector1 + vector2: {to_list_and_round_for_output(v1.nxyz + v2.nxyz)}",
            f"magnitude of vector12: {to_list_and_round_for_output(mag)}",
            f"unit vector of vector12: {to_list_and_round_for_output(unit)}",
            f"cross product vector of vector12: {to_list_and_round_for_output(cross_prod)}",
            f"dot product vector of vector12: {to_list_and_round_for_output(dot_prod)}",
            f"unit vector of vector1: {to_list_and_round_for_output(unit1)}",
            f"unit vector of vector2: {to_list_and_round_for_output(unit2)}",
            f"magnitude of vector1: {to_list_and_round_for_output(mag1)}",
            f"magnitude of vector2: {to_list_and_round_for_output(mag2)}"
        ]
    elif input_type == "single vector":
        static_var.input = [*v1.xyz]
        static_var.output = [
            f"unit vector of vector1: {to_list_and_round_for_output(unit1)}",
            f"magnitude of vector1: {to_list_and_round_for_output(mag1)}"
        ]
    else:
        static_var.input = []
        static_var.output = ["Select an input type"]
    return static_var.output, static_var.input


def process_form_request_home(request):
    # Sidebar buttons
    if "button" in request.form:
        btn = request.form.get("button")
        static_var.button = btn if btn in [
            "button_one", "cartesian", "cylindrical", "spherical", "button_three"] else "home"

    # Input type select
    if "input_type" in request.form:
        input_type = request.form.get("input_type")
        static_var.input_type = input_type if input_type in [
            "two vectors with c", "two vectors without c", "single vector"] else "single vector"

    # Vector input fields
    if "input_x1" in request.form:  # detect vector submission
        static_var.output, static_var.input = process_input(
            request, static_var.input_type)
    return static_var.button, static_var.input, static_var.output, static_var.input_type


def process_form_sketch(request):
    if "sketch_button" in request.form:  # detect sketch submision
        button = request.form.get("sketch_button")
        if button == "submit":
            x = float(request.form.get("input_x")
                      )if request.form.get("input_x") else 0
            y = float(request.form.get("input_y")
                      )if request.form.get("input_y") else 0
            z = float(request.form.get("input_z")
                      )if request.form.get("input_z") else 0
            return [x, y, z]
        elif button == "reset":
            return ["reset"]
    elif "system_type" in request.form:  # detect system type change
        system_type = request.form.get("system_type")
        if system_type in ["cartesian", "cylindrical", "spherical"]:
            return [system_type]
    return []
