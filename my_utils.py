import numpy as np
import math


def to_eng(value, precision=3):
    """
    Converts a float to a string in engineering notation.
    """
    if value == 0:
        return "0"

    # Calculate power in steps of 3
    pwr = int(math.floor(math.log10(abs(value)) / 3.0) * 3)

    # Scale the value
    mantissa = value / (10.0 ** pwr)

    # Suffix dictionary
    suffixes = {
        -18: 'a', -15: 'f', -12: 'p', -9: 'n', -6: 'µ', -3: 'm',
        0: '',
        3: 'k', 6: 'M', 9: 'G', 12: 'T', 15: 'P', 18: 'E'
    }

    suffix = suffixes.get(pwr, f"e{pwr}")
    return f"{mantissa:.{precision}f}{suffix}"


def make_output_clean(v):
    ''' TAKE INPUT v AS Vector, np.array, list, str, or float'''
    # convert Vector or np.array to a plain list of floats rounded to 3 decimal places
    if isinstance(v, Vector):
        return v.get_full_eng()
    elif isinstance(v, np.ndarray):
        # unpack NumPy array
        x, y, z = [float(round(x, 3)) for x in v]
        return f"<{x}, {y}, {z}>"
    elif isinstance(v, list):
        x, y, z = [float(round(x, 3)) for x in v]
        return f"<{x}, {y}, {z}>"        # unpack list
    elif isinstance(v, str):
        return v        # return string as is
    else:
        return round(v, 3)  # return float


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

    def get_x_eng(self):
        return to_eng(self.xyz[0])

    def get_y_eng(self):
        return to_eng(self.xyz[1])

    def get_z_eng(self):
        return to_eng(self.xyz[2])

    def get_mag_eng(self):
        return to_eng(self.magnitude())

    def get_full_eng(self):
        # Returns the whole vector like <10k, 5m, 0>
        return f"<{self.get_x_eng()}, {self.get_y_eng()}, {self.get_z_eng()}>"

    def set_charge(self, q):
        self.charge = q

    def magnitude(self):
        return np.linalg.norm(self.xyz)

    def unit_vector(self):
        magnitude = self.magnitude()
        if magnitude == 0:
            return Vector(0, 0, 0)
        else:
            return self.convert_to_vector(self.nxyz / magnitude)


def cross(v1, v2):
    return Vector.convert_to_vector(np.cross(v1.nxyz, v2.nxyz))


def dot(v1, v2):
    return np.dot(v1.nxyz, v2.nxyz)


def vector_12(v1, v2):
    return Vector.convert_to_vector(np.array(v1.nxyz) - np.array(v2.nxyz))


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
