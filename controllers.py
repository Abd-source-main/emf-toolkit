from my_utils import *
from flask import Flask, render_template, request


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
        mag = vector_12(v1, v2).magnitude()
        unit = vector_12(v1, v2).unit_vector()
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
