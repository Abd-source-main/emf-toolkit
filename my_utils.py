import numpy as np
from math import sqrt
import math
from flask import Flask, render_template, request


# To have similar to a static variable in c++
class static_var:
    button = "home"
    output = []
    input = []
    input_type = "two vectors with c"


class Vector:
    def __init__(self, x, y, z, c=1):
        self.xyz = [x, y, z]
        self.charge = c
        self.nxyz = np.array(self.xyz)

    @classmethod
    def convert_to_vector(cls, var):
        arr = np.array(var)
        if arr.size == 1:
            return arr.item()  # return as a scalar
        return cls(*var)

    def set_charge(self, q):
        self.charge = q

    def magnitude(self):
        return np.linalg.norm(self.xyz)

    def unit_vector(self):
        # avoid division by zero
        if self.magnitude() == 0:
            return [0, 0, 0]
        else:
            return self.convert_to_vector(self.nxyz/self.magnitude())


k = 8.99 * (10 ** 9)  # coloumb's constant
E0 = 8.854 * (10 ** -12)  # permittivity of free space


def cross(v1, v2):
    return Vector.convert_to_vector(np.cross(v1.nxyz, v2.nxyz))


def dot(v1, v2):
    return np.dot(v1.nxyz, v2.nxyz)


def vector_12(v1, v2):
    return Vector.convert_to_vector(np.array(v2.nxyz) - np.array(v1.nxyz))

# vector


def electric_force(v1, v2, q1, q2):
    # r is a vector
    r = vector_12(v1, v2)
    scaler = (k * q1 * q2) / (r.magnitude() ** 3) if r.magnitude() != 0 else 0
    # F = (k * q1*q2 / |r^3| ) * v12
    force = scaler * r.nxyz if r.magnitude() != 0 else 'can NOT divide by zero'
    return Vector.convert_to_vector(force)

# vector


def electrical_field(v1, v2, q1):
    # E = F/q2 (when q2 = 1 --> E = F)
    E = electric_force(v1, v2, q1, 1)
    return E

# scalar


def electrical_potential(v1, v2, q1):
    r = vector_12(v1, v2).magnitude()
    # V = k * q1 / r
    v = (k*q1) / r if r != 0 else 0
    return v


# vector
def flux_density(v1, v2, q1, Er=1):
    # Er is relative permittivity
    # D = Er * E0 * electric_field
    D = Er * E0 * electrical_field(v1, v2, q1).nxyz if isinstance(
        electrical_field(v1, v2, q1), Vector) else 'can NOT divide by zero'
    return D

# unedeted ..............................................................


def cartesian_to_spherical(x, y, z):
    r = math.sqrt(x ** 2 + y ** 2 + z ** 2)
    theta = math.atan2(y, x)
    phi = math.acos(z / r) if r != 0 else 0
    return r, theta, phi


def spherical_to_cartesian(r, theta, phi):
    x = r * math.sin(phi) * math.cos(theta)
    y = r * math.sin(phi) * math.sin(theta)
    z = r * math.cos(phi)
    return x, y, z


def cartesian_to_cylindrical(fi, sec, thrd):
    x = fi
    y = sec
    z = thrd
    r = math.sqrt(x ** 2 + y ** 2)
    theta = math.atan2(y, x)
    return r, theta, z


def cylindrical_to_cartesian(fi, sec, thrd):
    r = fi
    theta = sec
    z = thrd
    x = r * math.cos(theta)
    y = r * math.sin(theta)
    return x, y, z

# ......................................................


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
