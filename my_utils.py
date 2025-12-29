import numpy as np
import math


def is_number(string):
    """ check if str can turn to float"""
    try:
        float(string)
        return True
    except ValueError:
        return False


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
    return f"{mantissa:.{precision}f} {suffix}"


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
    def _normalize(angle):
        return angle % (2 * math.pi)

    # ==========================
    # POINT CONVERSIONS
    # ==========================

    @staticmethod
    def cartesian_to_cylindrical_point(x, y, z):
        """ Returns (rho, phi, z) """
        rho = math.sqrt(x**2 + y**2)
        phi = CoordinateConverter._normalize(math.atan2(y, x))
        return rho, phi, z

    @staticmethod
    def cylindrical_to_cartesian_point(rho, phi, z):
        """ Returns (x, y, z) """
        phi = CoordinateConverter._normalize(phi)
        x = rho * math.cos(phi)
        y = rho * math.sin(phi)
        return x, y, z

    @staticmethod
    def cartesian_to_spherical_point(x, y, z):
        """ Returns (r, theta, phi) """
        r = math.sqrt(x**2 + y**2 + z**2)
        theta_raw = math.acos(z / r) if r != 0 else 0
        phi_raw = math.atan2(y, x)

        theta = CoordinateConverter._normalize(theta_raw)
        phi = CoordinateConverter._normalize(phi_raw)
        return r, theta, phi

    @staticmethod
    def spherical_to_cartesian_point(r, theta, phi):
        """ Returns (x, y, z) """
        theta = CoordinateConverter._normalize(theta)
        phi = CoordinateConverter._normalize(phi)

        x = r * math.sin(theta) * math.cos(phi)
        y = r * math.sin(theta) * math.sin(phi)
        z = r * math.cos(theta)
        return x, y, z

    @staticmethod
    def cylindrical_to_spherical_point(rho, phi, z):
        phi = CoordinateConverter._normalize(phi)
        x, y, z = CoordinateConverter.cylindrical_to_cartesian_point(
            rho, phi, z)
        return CoordinateConverter.cartesian_to_spherical_point(x, y, z)

    @staticmethod
    def spherical_to_cylindrical_point(r, theta, phi):
        theta = CoordinateConverter._normalize(theta)
        phi = CoordinateConverter._normalize(phi)
        x, y, z = CoordinateConverter.spherical_to_cartesian_point(
            r, theta, phi)
        return CoordinateConverter.cartesian_to_cylindrical_point(x, y, z)

    # ==========================
    # VECTOR CONVERSIONS
    # ==========================

    @staticmethod
    def vector_cartesian_to_cylindrical(Ax, Ay, Az, x, y, z):
        """ Returns (A_rho, A_phi, A_z) """
        # Only inputs are cartesian, phi is calculated (and normalized) internally
        _, phi, _ = CoordinateConverter.cartesian_to_cylindrical_point(x, y, z)
        c, s = math.cos(phi), math.sin(phi)

        matrix = np.array([
            [c,  s, 0],
            [-s,  c, 0],
            [0,  0, 1]
        ])
        return tuple(np.dot(matrix, [Ax, Ay, Az]))

    @staticmethod
    def vector_cylindrical_to_cartesian(Arho, Aphi, Az, rho, phi, z):
        """ Returns (Ax, Ay, Az) """
        phi = CoordinateConverter._normalize(phi)
        c, s = math.cos(phi), math.sin(phi)

        matrix = np.array([
            [c, -s, 0],
            [s,  c, 0],
            [0,  0, 1]
        ])
        return tuple(np.dot(matrix, [Arho, Aphi, Az]))

    @staticmethod
    def vector_cartesian_to_spherical(Ax, Ay, Az, x, y, z):
        """ Returns (A_r, A_theta, A_phi) """
        # Inputs are cartesian, angles are calculated internally
        _, theta, phi = CoordinateConverter.cartesian_to_spherical_point(
            x, y, z)

        st, ct = math.sin(theta), math.cos(theta)
        sp, cp = math.sin(phi),   math.cos(phi)

        matrix = np.array([
            [st*cp, st*sp, ct],
            [ct*cp, ct*sp, -st],
            [-sp,   cp,    0]
        ])
        return tuple(np.dot(matrix, [Ax, Ay, Az]))

    @staticmethod
    def vector_spherical_to_cartesian(Ar, Atheta, Aphi, r, theta, phi):
        """ Returns (Ax, Ay, Az) """
        theta = CoordinateConverter._normalize(theta)
        phi = CoordinateConverter._normalize(phi)

        st, ct = math.sin(theta), math.cos(theta)
        sp, cp = math.sin(phi),   math.cos(phi)

        matrix = np.array([
            [st*cp, ct*cp, -sp],
            [st*sp, ct*sp,  cp],
            [ct,    -st,    0]
        ])
        return tuple(np.dot(matrix, [Ar, Atheta, Aphi]))

    @staticmethod
    def vector_spherical_to_cylindrical(Ar, Atheta, Aphi, r, theta, phi):
        theta = CoordinateConverter._normalize(theta)
        phi = CoordinateConverter._normalize(phi)

        # 1. Spherical -> Cartesian
        Ax, Ay, Az = CoordinateConverter.vector_spherical_to_cartesian(
            Ar, Atheta, Aphi, r, theta, phi)

        # 2. Get Point in Cartesian
        x, y, z = CoordinateConverter.spherical_to_cartesian_point(
            r, theta, phi)

        # 3. Cartesian -> Cylindrical
        return CoordinateConverter.vector_cartesian_to_cylindrical(Ax, Ay, Az, x, y, z)

    @staticmethod
    def vector_cylindrical_to_spherical(Arho, Aphi, Az, rho, phi, z):
        phi = CoordinateConverter._normalize(phi)

        # 1. Cylindrical -> Cartesian
        Ax, Ay, Az = CoordinateConverter.vector_cylindrical_to_cartesian(
            Arho, Aphi, Az, rho, phi, z)

        # 2. Get Point in Cartesian
        x, y, z = CoordinateConverter.cylindrical_to_cartesian_point(
            rho, phi, z)

        # 3. Cartesian -> Spherical
        return CoordinateConverter.vector_cartesian_to_spherical(Ax, Ay, Az, x, y, z)
