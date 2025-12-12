import plotly.graph_objects as go
import random
import numpy as np
from my_utils import CoordinateConverter as CC


class Vector_colors:
    origin_colors = [
        "red", "green", "yellow", "orange", "purple", "pink", "brown",
        "black", "white", "gray", "grey", "cyan", "magenta", "lime", "teal",
        "navy", "maroon", "olive", "gold", "silver", "beige", "coral", "crimson",
        "indigo", "ivory", "khaki", "lavender", "lightblue", "lightgreen",
        "lightcoral", "lightpink", "lightgray", "darkblue", "darkgreen",
        "darkred", "darkorange", "darkviolet", "deepskyblue", "dodgerblue",
        "forestgreen", "hotpink", "midnightblue", "royalblue", "salmon",
        "seagreen", "skyblue", "slategray", "tomato", "turquoise", "violet",
        "wheat"
    ]
    copy_colors = origin_colors.copy()

    @classmethod
    def get_color(cls,):
        if not cls.copy_colors:
            cls.copy_colors = cls.origin_colors.copy()
        color = random.choice(cls.copy_colors)
        cls.copy_colors.remove(color)
        return color


class Sketch_element:
    # data must be a list of dictionaries with start and end points
    # with name and optional size
    @staticmethod
    def sketch_cartesian_vector(vec, config, size=8):
        x0, y0, z0 = vec["start"]
        x1, y1, z1 = vec["end"]
        vec_name = vec["name"]
        # ONLY axises doesnt have color attribute in their dict
        vec_color = vec["color"] if "color" in vec else "blue"
        config.add_trace(go.Scatter3d(
            x=[x0, x1],
            y=[y0, y1],
            z=[z0, z1],
            mode='lines',
            line=dict(width=size, color=vec_color),
            name=vec_name,
            legendgroup=vec_name,
            showlegend=True
        ))

        config.add_trace(go.Cone(x=[x1], y=[y1],
                                 z=[z1],
                                 u=[x1 - x0],
                                 v=[y1 - y0],
                                 w=[z1 - z0],
                                 sizemode="absolute",
                                 sizeref=0.2,
                                 anchor="tip",
                                 showscale=False,
                                 colorscale=[
                                          [0, vec_color], [1, vec_color]],
                                 legendgroup=vec_name,
                                 showlegend=False
                                 ))

    @staticmethod
    def sketch_cylindrical_vector(vec, config, size=8):
        r, phi, z = vec["start"]
        r_end, phi_end, z_end = vec["end"]
        vec_name = vec["name"]
        vec_color = vec["color"] if "color" in vec else "blue"

        # Convert cylindrical to cartesian coordinates for plotting
        x0, y0, z = CC.cylindrical_to_cartesian(r, phi, z)
        x1, y1, z_end = CC.cylindrical_to_cartesian(r_end, phi_end, z_end)

        new_dict = {"start": (x0, y0, z),
                    "end": (x1, y1, z_end),
                    "name": vec_name,
                    "color": vec_color}

        Sketch_element.sketch_cartesian_vector(
            new_dict, config=config, size=size)

    @staticmethod
    def sketch_spherical_vector(vec, config, size=8):
        """ under development """
        radius, theta, phi = vec["start"]
        radius_end, theta_end, phi_end = vec["end"]
        vec_name = vec["name"]
        vec_color = vec["color"] if "color" in vec else "blue"

        # Convert spherical to cartesian coordinates for plotting
        x0, y0, z0 = CC.spherical_to_cartesian(radius, theta, phi)
        x1, y1, z1 = CC.spherical_to_cartesian(
            radius_end, theta_end, phi_end)

        new_dict = {"start": (x0, y0, z0),
                    "end": (x1, y1, z1),
                    "name": vec_name,
                    "color": vec_color}
        Sketch_element.sketch_cartesian_vector(
            new_dict, config=config, size=size)

    @staticmethod
    def sketch_unit_vectors(larger_i, larger_j, larger_k, config, system="cartesian"):
        if system == "cartesian":
            unit_names = ["x-axis", "y-axis", "z-axis"]
            unitVectors = [
                {"start": (0, 0, 0), "end": (larger_i, 0, 0),
                 "name": unit_names[0]},
                {"start": (0, 0, 0), "end": (0, larger_j, 0),
                 "name": unit_names[1]},
                {"start": (0, 0, 0), "end": (0, 0, larger_k),
                 "name": unit_names[2]},
                {"start": (0, 0, 0), "end": (-larger_i, 0, 0),
                 "name": f"negative {unit_names[0]}"},
                {"start": (0, 0, 0), "end": (0, -larger_j, 0),
                 "name": f"negative {unit_names[1]}"},
                {"start": (0, 0, 0), "end": (0, 0, -larger_k),
                 "name": f"negative {unit_names[2]}"}
            ]
        elif system == "cylindrical":
            unit_names = ["ρ-axis", "φ-axis", "z-axis"]
            unitVectors = [
                {"start": (0, 0, 0), "end": (larger_i, 0, 0),
                 "name": unit_names[0]},
                {"start": (0, 0, 0), "end": (0, 0, larger_k),
                 "name": unit_names[2]},
                {"start": (0, 0, 0), "end": (0, 0, -larger_k),
                 "name": f"negative {unit_names[2]}"}
            ]
        else:
            # not coded yet
            unit_names = ["r-axis", "θ-axis", "φ-axis"]
            unitVectors = []
        # sketch origin point
        config.add_trace(go.Scatter3d(
            x=[0],
            y=[0],
            z=[0],
            mode='markers',
            marker=dict(size=4, color='black'),
            name='origin',
            showlegend=True
        ))
        # sketch unit vectors
        if system == "cartesian":
            for unitVector in unitVectors:
                Sketch_element.sketch_cartesian_vector(
                    unitVector, config=config, size=8)
        elif system == "cylindrical":
            for unitVector in unitVectors:
                Sketch_element.sketch_cylindrical_vector(
                    unitVector, config=config, size=8)
        elif system == "spherical":
            for unitVector in unitVectors:
                Sketch_element.sketch_spherical_vector(
                    unitVector, config=config, size=8)

    @staticmethod
    def sketch_grid_lines(larger_i, larger_j, config):
        """ sketch grid lines between an axis (i) and another axis (j) """
        if not isinstance(larger_i, np.ndarray) and not isinstance(larger_j, np.ndarray):
            x_points = np.linspace(larger_i, -larger_i, 10)
            y_points = np.linspace(larger_j, -larger_j, 10)
        else:
            x_points = larger_i
            y_points = larger_j
        for x in x_points:
            config.add_trace(go.Scatter3d(
                x=[x, x],
                y=[larger_j, -larger_j],
                z=[0, 0],
                mode='lines',
                line=dict(width=2, color='lightgray'),
                showlegend=False,
                hoverinfo='skip'
            ))
        for y in y_points:
            config.add_trace(go.Scatter3d(
                x=[larger_i, -larger_i],
                y=[y, y],
                z=[0, 0],
                mode='lines',
                line=dict(width=2, color='lightgray'),
                showlegend=False,
                hoverinfo='skip'
            ))

    # still in development
    # range must be a tuple
    @staticmethod
    def sketch_circle(radius, range, around_axis, config, size=4, shift=0):
        min, max = range
        theta = np.linspace(min, max, 1000)
        theta = np.append(theta, max)
        theta = np.insert(theta, 0, min)
        if around_axis == 'x':
            y = radius * np.cos(theta)
            z = radius * np.sin(theta)
            x = np.ones_like(theta) * shift
        elif around_axis == 'y':
            x = radius * np.cos(theta)
            z = radius * np.sin(theta)
            y = np.ones_like(theta) * shift
        elif around_axis == 'z':
            x = np.cos(theta) * radius
            y = np.sin(theta) * radius
            z = np.ones_like(theta) * shift
        else:
            return
        config.add_trace(go.Scatter3d(
            x=x,
            y=y,
            z=z,
            mode='lines',
            line=dict(width=size, color='blue'),
            name=f'circle-r{radius}',
            showlegend=False
        ))

    @staticmethod
    def sketch_cylinder(rho, phi, z, config, size=4):
        x, y, z = CC.cylindrical_to_cartesian(rho, phi, z)
        # sketch top and bottom circles
        Sketch_element.sketch_circle(radius=rho, range=(
            0, phi), around_axis='z', config=config, size=size, shift=-z)
        Sketch_element.sketch_circle(radius=rho, range=(
            0, phi), around_axis='z', config=config, size=size, shift=z)
        # sketch vertical lines that connect top and bottom circles
        config.add_trace(go.Scatter3d(
            x=[rho, rho],
            y=[0, 0],
            z=[-z, z],
            mode='lines',
            line=dict(width=size, color='blue'),
            name=f'cylinder-r{rho}',
            showlegend=False
        ))
        config.add_trace(go.Scatter3d(
            x=[x, x],
            y=[y, y],
            z=[-z, z],
            mode='lines',
            line=dict(width=size, color='blue'),
            name=f'cylinder-r{rho}',
            showlegend=False
        ))
        # sketch top/bottom lines at the ending phi
        config.add_trace(go.Scatter3d(
            x=[0, x],
            y=[0, y],
            z=[z, z],
            mode='lines',
            line=dict(width=size, color='blue'),
            name=f'cylinder-r{rho}',
            showlegend=False
        ))
        config.add_trace(go.Scatter3d(
            x=[0, x],
            y=[0, y],
            z=[-z, -z],
            mode='lines',
            line=dict(width=size, color='blue'),
            name=f'cylinder-r{rho}',
            showlegend=False
        ))
        # sketch top/bottom lines at the starting phi=0
        config.add_trace(go.Scatter3d(
            x=[0, rho],
            y=[0, 0],
            z=[-z, -z],
            mode='lines',
            line=dict(width=size, color='blue'),
            name=f'cylinder-r{rho}',
            showlegend=False
        ))
        config.add_trace(go.Scatter3d(
            x=[0, rho],
            y=[0, 0],
            z=[z, z],
            mode='lines',
            line=dict(width=size, color='blue'),
            name=f'cylinder-r{rho}',
            showlegend=False
        ))
        # sketch grid lines on top and bottom circles
        theta = np.linspace(0, phi, 10)
        x = np.cos(theta) * rho
        y = np.sin(theta) * rho
        Sketch_element.sketch_grid_lines(x, y, config)


class Sketch_plane:
    # lists of dict to store vectors data
    counter = 1
    xyz_vectors = []
    ppz_vectors = []
    rtp_vectors = []

    def add_input_vector(self, vector, system, config):
        # define inputed vector
        input_vector = {"start": (0, 0, 0),
                        "end": (vector[0], vector[1], vector[2]),
                        "name": f"vector-{self.counter}",
                        "color": Vector_colors.get_color()}
        self.add_counter()
        if system == "cartesian":
            # re sketch every inputed vector
            for i in self.xyz_vectors:
                Sketch_element.sketch_cartesian_vector(i, config)
            Sketch_element.sketch_cartesian_vector(input_vector, config)
            # add the new vector to vectors list
            self.add_xyz_vector(input_vector)
        elif system == "cylindrical":
            # re sketch every inputed vector
            for i in self.ppz_vectors:
                Sketch_element.sketch_cylindrical_vector(i, config)
            Sketch_element.sketch_cylindrical_vector(input_vector, config)
            # add the new vector to vectors list
            self.add_ppz_vector(input_vector)
        elif system == "spherical":
            # re sketch every inputed vector
            for i in self.rtp_vectors:
                Sketch_element.sketch_spherical_vector(i, config)
            Sketch_element.sketch_spherical_vector(input_vector, config)
            # add the new vector to vectors list
            self.add_rtp_vector(input_vector)

    @classmethod
    def add_counter(cls):
        cls.counter += 1

    @classmethod
    def reset_counter(cls):
        cls.counter = 1

    @classmethod
    def clear_saved_vectors(cls):
        cls.xyz_vectors.clear()
        cls.ppz_vectors.clear()
        cls.rtp_vectors.clear()

    @classmethod
    def reset_sketch(cls):
        cls.reset_counter()
        cls.clear_saved_vectors()

    @classmethod
    def add_xyz_vector(cls, vector):
        cls.xyz_vectors.append(vector)

        # Cartesian -> Cylindrical
        rho, phi, z = CC.cartesian_to_cylindrical(*vector['end'])
        cls.ppz_vectors.append({
            'start': (0, 0, 0),
            'end': (rho, phi, z),
            'name': vector['name'],
            'color': vector['color']
        })

        # Cartesian -> Spherical
        radius, theta, phi = CC.cartesian_to_spherical(*vector['end'])
        cls.rtp_vectors.append({
            'start': (0, 0, 0),
            'end': (radius, theta, phi),
            'name': vector['name']
        })

    @classmethod
    def add_ppz_vector(cls, vector):
        cls.ppz_vectors.append(vector)

        # Cylindrical -> Cartesian
        x, y, z = CC.cylindrical_to_cartesian(*vector['end'])
        cls.xyz_vectors.append({
            'start': (0, 0, 0),
            'end': (x, y, z),
            'name': vector['name'],
            'color': vector['color']
        })

        # Cylindrical -> Spherical
        radius, theta, phi = CC.cylindrical_to_spherical(*vector['end'])
        cls.rtp_vectors.append({
            'start': (0, 0, 0),
            'end': (radius, theta, phi),
            'name': vector['name']
        })

    @classmethod
    def add_rtp_vector(cls, vector):
        cls.rtp_vectors.append(vector)

        # Spherical -> Cartesian
        x, y, z = CC.spherical_to_cartesian(*vector['end'])
        cls.xyz_vectors.append({
            'start': (0, 0, 0),
            'end': (x, y, z),
            'name': vector['name'],
            'color': vector['color']
        })

        # Spherical -> Cylindrical
        rho, phi, z = CC.spherical_to_cylindrical(*vector['end'])
        cls.ppz_vectors.append({
            'start': (0, 0, 0),
            'end': (rho, phi, z),
            'name': vector['name']
        })

    @staticmethod
    def check_larger_vector(vector, larger_i, larger_j, larger_k):
        larger_i = abs(vector[0]) if abs(
            vector[0]) > abs(larger_i) else larger_i
        larger_j = abs(vector[1]) if abs(
            vector[1]) > abs(larger_j) else larger_j
        larger_k = abs(vector[2]) if abs(
            vector[2]) > abs(larger_k) else larger_k
        return larger_i, larger_j, larger_k


class Sketch_cartesian(Sketch_plane):

    def __init__(self):
        self.reinitialize_cartesian(is_like_first_time=True)

    def reinitialize_cartesian(self, is_like_first_time=True):
        self.fig = go.Figure()
        if is_like_first_time:
            self.reset_sketch()
            self.larger_z = self.larger_y = self.larger_x = 1

    def create_cartesian_sketch(self, strdata=[]):
        self.reinitialize_cartesian(is_like_first_time=False)
        # add the axes x,y,z
        # iykyk
        vector = [float(x) for x in strdata]
        if vector:
            self.larger_x = abs(vector[0]) if abs(vector[0]) > abs(
                self.larger_x) else self.larger_x
            self.larger_y = abs(vector[1]) if abs(vector[1]) > abs(
                self.larger_y) else self.larger_y
            self.larger_z = abs(vector[2]) if abs(vector[2]) > abs(
                self.larger_z) else self.larger_z
        # sketch unit vectors
        Sketch_element.sketch_unit_vectors(
            self.larger_x, self.larger_y, self.larger_z, config=self.fig)
        # sketch grid lines betweem x,y axises
        Sketch_element.sketch_grid_lines(
            self.larger_x, self.larger_y, config=self.fig)
        # add padding
        x_padding = self.larger_x + 0.3
        y_padding = self.larger_y + 0.3
        z_padding = self.larger_z + 0.3

        # Determan the max range for the figure
        self.fig.update_layout(
            scene=dict(
                aspectmode="cube",
                xaxis=dict(range=[-x_padding, x_padding]),
                yaxis=dict(range=[-y_padding, y_padding]),
                zaxis=dict(range=[-z_padding, z_padding]),
            )
        )
        # set layout to be responsive
        self.fig.update_layout(
            autosize=True,
            margin=dict(l=0, r=0, t=0, b=0),
            height=None,
        )
    # if it was called for only the axises
        if not vector or vector[0] == vector[1] == vector[2] == 0:
            # re sketch every inputed vector
            for i in self.xyz_vectors:
                Sketch_element.sketch_cartesian_vector(i, config=self.fig)
            return self.fig.to_html(
                full_html=False, include_plotlyjs=True, config={"responsive": True})

        # add the input vector data must be 3
        if not len(vector) == 3:
            return "<h>There was somthing wrong with the input data" \
                "it should be 3</h>"
        super().add_input_vector(vector, system="cartesian", config=self.fig)

        # Convert figure to HTML
        plot_html = self.fig.to_html(
            full_html=False, include_plotlyjs=True, config={"responsive": True})

        return plot_html


class Sketch_cylindrical(Sketch_plane):
    def __init__(self):
        self.reinitialize_cylindrical(is_like_first_time=True)

    def reinitialize_cylindrical(self, is_like_first_time=True):
        self.fig = go.Figure()
        if is_like_first_time:
            self.reset_sketch()
            self.larger_rho = 1
            self.larger_phi = 0
            self.larger_z = 0

    def create_cylindrical_sketch(self, strdata=[]):
        self.reinitialize_cylindrical(is_like_first_time=False)
        # add the axes rho,phi,z
        # iykyk
        vector = [float(x) for x in strdata]
        if vector and len(vector) > 1:  # avoid index error
            if vector[0] < 0:
                vector[0] = abs(vector[0])
                vector[1] = vector[1] + 180
            while vector[1] > 360:
                vector[1] -= 360
            while vector[1] < 0:
                vector[1] += 360
            vector[1] = vector[1] * (np.pi / 180)  # convert phi to radians
        if vector:
            self.larger_rho = max(abs(vector[0]), abs(self.larger_rho))
            self.larger_phi = max(abs(vector[1]), abs(self.larger_phi))
            self.larger_z = max(abs(vector[2]), abs(self.larger_z))
        larger_axis = [self.larger_rho, self.larger_phi, self.larger_z]
        # sketch unit vectors
        Sketch_element.sketch_unit_vectors(
            *larger_axis, config=self.fig, system="cylindrical")

        # add padding
        for_a_true_circle = max(self.larger_rho, self.larger_phi) + 1
        z_padding = self.larger_z + 1

        # Determan the max range for the figure
        self.fig.update_layout(
            scene=dict(
                aspectmode="cube",
                xaxis=dict(range=[-for_a_true_circle, for_a_true_circle]),
                yaxis=dict(range=[-for_a_true_circle, for_a_true_circle]),
                zaxis=dict(range=[-z_padding, z_padding]),
            )
        )
        # set layout to be responsive
        self.fig.update_layout(
            autosize=True,
            margin=dict(l=0, r=0, t=0, b=0),
            height=None,
        )
        # if it was called for only the axises or pressed submit without input
        if not vector or vector[0] == vector[1] == vector[2] == 0:
            # re sketch every inputed vector
            for i in self.ppz_vectors:
                Sketch_element.sketch_cylindrical_vector(i, config=self.fig)
            Sketch_element.sketch_cylinder(rho=self.larger_rho,
                                           phi=self.larger_phi,
                                           z=self.larger_z,
                                           config=self.fig)
            return self.fig.to_html(
                full_html=False, include_plotlyjs=True, config={"responsive": True})

        # add the input vector data must be 3
        if not len(vector) == 3:
            return "<h>There was somthing wrong with the input data" \
                "it should be 3</h>"
        super().add_input_vector(vector, system="cylindrical", config=self.fig)

        Sketch_element.sketch_cylinder(rho=self.larger_rho,
                                       phi=self.larger_phi,
                                       z=self.larger_z,
                                       config=self.fig)

        # Convert figure to HTML
        plot_html = self.fig.to_html(
            full_html=False, include_plotlyjs=True, config={"responsive": True})
        return plot_html


class Sketch_spherical(Sketch_plane):
    def __init__(self):
        self.reinitialize_spherical(is_like_first_time=True)

    def reinitialize_spherical(self, is_like_first_time=True):
        self.fig = go.Figure()
        if is_like_first_time:
            self.reset_sketch()
            self.larger_r = self.larger_theta = self.larger_phi = 1


class Sketch_controller(Sketch_cartesian, Sketch_cylindrical, Sketch_spherical):
    ''' A controller class to manage different sketch systems (three classes) '''

    def __init__(self):
        Sketch_cartesian.__init__(self)
        Sketch_cylindrical.__init__(self)
        Sketch_spherical.__init__(self)
