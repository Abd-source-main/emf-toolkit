from flask import flash
from my_utils import *
import physics_applications


# To have similar to a static variable in c++


class static_var:
    button = "home"
    output = []
    input = []
    input_type = "two vectors with c"


def process_input(request, input_type):
    x1, y1, z1 = ProcessForm.get_form_input(
        request, ["input_x1", "input_y1", "input_z1"])
    v1 = Vector(x1, y1, z1)
    unit1 = v1.unit_vector()
    mag1 = v1.magnitude()
    if input_type == "single vector":
        static_var.input = [*v1.xyz]
        static_var.output = [
            f"unit vector of vector1: {make_output_clean(unit1)}",
            f"magnitude of vector1: {make_output_clean(mag1)}"
        ]
    elif input_type == "two vectors without c" or input_type == "two vectors with c":
        # GET INPUT
        x2, y2, z2 = ProcessForm.get_form_input(
            request, ["input_x2", "input_y2", "input_z2"])
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

    else:
        return ["Select an input type"], []
    # prepare output
    # FOR jinja its x1,y1,z1,c1,x2,y2,z2,c2 in order
    if input_type == "two vectors with c":
        static_var.input = [*v1.xyz, v1.charge, *v2.xyz, v2.charge]
        static_var.output = [
            f"vector2 - vector1: {make_output_clean(v12)}",
            f"vector1 + vector2: {make_output_clean(v1.nxyz + v2.nxyz)}",
            f"magnitude of vector12: {make_output_clean(mag)}",
            f"unit vector of vector12: {make_output_clean(unit)}",
            f"cross product vector of vector12: {make_output_clean(cross_prod)}",
            f"dot product vector of vector12: {make_output_clean(dot_prod)}",
            f"unit vector of vector1: {make_output_clean(unit1)}",
            f"unit vector of vector2: {make_output_clean(unit2)}",
            f"magnitude of vector1: {make_output_clean(mag1)}",
            f"magnitude of vector2: {make_output_clean(mag2)}"
        ]
    elif input_type == "two vectors without c":
        static_var.input = [*v1.xyz, *v2.xyz]
        static_var.output = [
            f"vector2 - vector1: {make_output_clean(v12)}",
            f"vector1 + vector2: {make_output_clean(v1.nxyz + v2.nxyz)}",
            f"magnitude of vector12: {make_output_clean(mag)}",
            f"unit vector of vector12: {make_output_clean(unit)}",
            f"cross product vector of vector12: {make_output_clean(cross_prod)}",
            f"dot product vector of vector12: {make_output_clean(dot_prod)}",
            f"unit vector of vector1: {make_output_clean(unit1)}",
            f"unit vector of vector2: {make_output_clean(unit2)}",
            f"magnitude of vector1: {make_output_clean(mag1)}",
            f"magnitude of vector2: {make_output_clean(mag2)}"
        ]
    elif input_type == "single vector":
        static_var.input = [*v1.xyz]
        static_var.output = [
            f"unit vector of vector1: {make_output_clean(unit1)}",
            f"magnitude of vector1: {make_output_clean(mag1)}"
        ]
    else:
        static_var.input = []
        static_var.output = ["Select an input type"]
    return static_var.output, static_var.input


def compare_text_only(str1, str2):
    # Remove digits from both strings
    clean1 = ''.join(char for char in str1 if not char.isdigit())
    clean2 = ''.join(char for char in str2 if not char.isdigit())
    return clean1 == clean2


class ProcessForm:
    @staticmethod
    def get_form_input(request, input_name_list,):
        input_list = []
        for name in input_name_list:
            input_list.append(float(request.form.get(name))
                              if request.form.get(name) else 0)
        return input_list

    @staticmethod
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

    @classmethod
    def process_form_sketch(cls, request):
        if "sketch_button" in request.form:  # detect sketch submision
            button = request.form.get("sketch_button")
            if button == "submit":
                op = cls.get_form_input(
                    request, ["input_i", "input_j", "input_k"])
                return op
            elif button == "reset":
                return ["reset"]
        elif "system_type" in request.form:  # detect system type change
            system_type = request.form.get("system_type")
            if system_type in ["cartesian", "cylindrical", "spherical"]:
                return [system_type]
        return []

    @classmethod
    def process_form_physics(cls, request):
        # buttons in source section
        if "source_charge_button" in request.form:
            theButton = request.form.get("source_charge_button")
            if theButton == "add_charge":
                input_charge = cls.get_form_input(
                    request, ["charge_value", "x_pos", "y_pos", "z_pos"])
                dict_charge = physics_applications.Charges(
                    input_charge).to_dict()
                return dict_charge, 'dict_input'  # return dict to be added
            elif theButton == "clear_charges":
                physics_applications.Session.clear_charges()
                flash("All charges cleared successfully.")
                return [], "clear_charges"  # indicate cleared

        # buttons in current charges section
        elif "current_charges_button" in request.form:
            theButton = request.form.get("current_charges_button")
            if compare_text_only(theButton, "remove_charge"):
                target_id = int(''.join(filter(str.isdigit, theButton)))
                physics_applications.Session.delete_charge(target_id)
                flash(f"Charge ID {target_id} removed successfully.")
                return [], "remove_charge"
                # finish later
            elif compare_text_only(theButton, "edit_charge"):
                pass
            elif compare_text_only(theButton, "calculate_effect"):
                target_id = int(''.join(filter(str.isdigit, theButton)))
                try:
                    f, e, v = physics_applications.calculate_effect(target_id)
                    return [f, e, v], "calculate_effect"
                except Exception as e:
                    flash(str(e) + " in controllers ")

        return [], None
