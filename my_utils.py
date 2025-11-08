import numpy as np
from math import sqrt
import math


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


class CoordinateConverter:
    @staticmethod
    def cartesian_to_spherical(x, y, z):
        """
        Cartesian (x, y, z) -> Spherical (radius, theta, phi)
        """
        radius = math.sqrt(x ** 2 + y ** 2 + z ** 2)
        theta = math.atan2(y, x)
        phi = math.acos(z / radius) if radius != 0 else 0
        return radius, theta, phi

    @staticmethod
    def spherical_to_cartesian(radius, theta, phi):
        """
        Spherical (radius, theta, phi) -> Cartesian (x, y, z)
        """
        x = radius * math.sin(phi) * math.cos(theta)
        y = radius * math.sin(phi) * math.sin(theta)
        z = radius * math.cos(phi)
        return x, y, z

    @staticmethod
    def cartesian_to_cylindrical(x, y, z):
        """
        Cartesian (x, y, z) -> Cylindrical (rho, phi, z)
        """
        rho = math.sqrt(x ** 2 + y ** 2)
        phi = math.atan2(y, x)
        return rho, phi, z

    @staticmethod
    def cylindrical_to_cartesian(rho, phi, z):
        """
        Cylindrical (rho, phi, z) -> Cartesian (x, y, z)
        """
        x = rho * math.cos(phi)
        y = rho * math.sin(phi)
        return x, y, z

    @staticmethod
    def spherical_to_cylindrical(radius, theta, phi):
        """
        cuz idk how there is this
        """
        x, y, z = CoordinateConverter.spherical_to_cartesian(
            radius, theta, phi)
        return CoordinateConverter.cartesian_to_cylindrical(x, y, z)

    @staticmethod
    def cylindrical_to_spherical(rho, phi, z):
        """
        cuz idk how there is this
        """

        x, y, z = CoordinateConverter.cylindrical_to_cartesian(rho, phi, z)
        return CoordinateConverter.cartesian_to_spherical(x, y, z)
