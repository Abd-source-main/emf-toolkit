from flask import session, flash
from my_utils import Vector, vector_12, np, to_eng


k = 9 * (10 ** 9)  # coloumb's constant
E0 = 8.854 * (10 ** -12)  # permittivity of free space


class Charges:
    g_id = 1

    def __init__(self, input):
        if isinstance(input, list):
            input_list = input
            self.charge_value = input_list[0]
            self.x_pos = input_list[1]
            self.y_pos = input_list[2]
            self.z_pos = input_list[3]
            if len(input_list) > 4:
                self.id = input_list[4]
            else:
                self.id = Charges.g_id
                Charges.g_id += 1
        elif isinstance(input, dict):
            input_dict = input
            self.charge_value = input_dict['charge_value']
            self.x_pos = input_dict['x_pos']
            self.y_pos = input_dict['y_pos']
            self.z_pos = input_dict['z_pos']
            self.id = input_dict['id']

    def get_charge_vector(self):
        return Vector(self.x_pos, self.y_pos, self.z_pos)

    def to_dict(self):
        dict_charge = {
            'id': self.id,
            'charge_value': self.charge_value,
            'x_pos': self.x_pos,
            'y_pos': self.y_pos,
            'z_pos': self.z_pos
        }
        return dict_charge

    def to_list4sketch(self):
        return [self.x_pos, self.y_pos, self.z_pos]


class physical_quantity_calculation:
    @staticmethod
    def electric_force(v1, v2, q1, q2):
        # r is a vector
        r = vector_12(v1, v2)
        mag = r.magnitude()

        if mag == 0:
            flash(
                "Calculated Force: Division by zero encountered (charges overlap). Returning zero vector")
            return Vector(0, 0, 0)

        # F = (k * q1*q2 / |r^3| ) * v12
        scaler = (k * q1 * q2) / (mag ** 3)
        force = scaler * r.nxyz
        return Vector.convert_to_vector(force)

    @classmethod
    def electrical_field(cls, v1, v2, q1):
        # E = F/q2 (when q2 = 1 --> E = F)
        # This calls electric_force, so the zero-check and flash are handled there.
        E = cls.electric_force(v1, v2, q1, 1)
        return E

    @staticmethod
    def electrical_potential(v1, v2, q1):
        r = vector_12(v1, v2).magnitude()

        if r == 0:
            flash("Calculated Potential: Division by zero encountered. Returning 0.")
            return 0.0

        # V = k * q1 / r
        v = (k * q1) / r
        return v

    @classmethod
    def flux_density(cls, v1, v2, q1, Er=1):
        # Er is relative permittivity
        # D = Er * E0 * electric_field
        electric_field = cls.electrical_field(v1, v2, q1)
        D = Vector.convert_to_vector(Er * E0 * electric_field.nxyz)
        return D


pq = physical_quantity_calculation()


def calculate_quantitiesBetweenTwoCharges(charge1, charge2):
    """take Charge object"""
    v1 = charge1.get_charge_vector()
    v2 = charge2.get_charge_vector()
    c1 = charge1.charge_value
    c2 = charge2.charge_value
    f = pq.electric_force(v1, v2, c2, c1)
    e = pq.electrical_field(v1, v2, c2)
    v = pq.electrical_potential(v1, v2, c2)
    return [f, e, v]


class Session():
    @staticmethod
    def save_charge(charge_dict):
        """take dict of charge and saves it (as a dict) to session"""
        if 'charges' not in session:
            session['charges'] = []
        session['charges'].append(charge_dict)
        session.modified = True

    @staticmethod
    def get_charges():
        """returns a list of Charges objects that is stored in session"""
        charges = []
        if 'charges' in session:
            for charge_dict in session['charges']:
                if not charge_dict:
                    continue
                charge = Charges(charge_dict)
                charges.append(charge)
        return charges

    @staticmethod
    def clear_charges():
        session.pop('charges', None)
        Charges.g_id = int(1)

    # later for edit
    @staticmethod
    def modify_charge(id, new_charge_dict):
        if 'charges' in session:
            session['charges'][id - 1] = new_charge_dict  # id starts from 1
            session.modified = True
        else:
            raise ValueError("No charges in session to modify IDIOT")

    @classmethod
    def delete_charge(cls, id):
        if 'charges' in session:
            newListCharges = cls.get_charges()
            for charge in newListCharges:
                if charge.id == id:
                    newListCharges.remove(charge)
                    break
            session['charges'] = [charge.to_dict()
                                  for charge in newListCharges]
            session.modified = True
        else:
            raise ValueError("No charges in session to delete IDIOT")


def calculate_effect(id):
    total_charges = Session.get_charges()
    if not total_charges:
        raise ValueError("No charges in session to calculate")

    target_charge = next((c for c in total_charges if c.id == id), None)

    if target_charge is None:
        flash(f"Charge with ID {id} not found.")
        return [Vector(0.0, 0.0, 0.0), Vector(0.0, 0.0, 0.0), 0]

    net_force = np.array([0.0, 0.0, 0.0])
    net_electric_field = np.array([0.0, 0.0, 0.0])
    net_potential = 0.0

    for charge in total_charges:
        if charge.id == target_charge.id:
            continue

        f, e, v = calculate_quantitiesBetweenTwoCharges(target_charge, charge)
        net_potential += v
        if isinstance(f, Vector) and isinstance(e, Vector):
            net_force += f.nxyz
            net_electric_field += e.nxyz
        else:
            flash("Calculation error: division by zero encountered.")
            return [Vector(0.0, 0.0, 0.0), Vector(0.0, 0.0, 0.0), 0]

    final_force = Vector.convert_to_vector(net_force)
    final_field = Vector.convert_to_vector(net_electric_field)
    net_potential = to_eng(net_potential)
    return [final_force, final_field, net_potential]
