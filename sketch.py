import plotly.graph_objects as go
import random
import numpy as np


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


class sketch_element:
    def __init__(self, config):
        self.config = config
    # data must be a list of dictionaries with start and end points
    # with name and optional size

    def sketch_vector(self, vec, size=8):
        x0, y0, z0 = vec["start"]
        x1, y1, z1 = vec["end"]
        vec_name = vec["name"]
        if vec_name[2:] == "axis" or vec_name[:8] == "negative":
            vec_color = "blue"
        else:
            vec_color = Vector_colors.get_color()
        self.config.add_trace(go.Scatter3d(
            x=[x0, x1],
            y=[y0, y1],
            z=[z0, z1],
            mode='lines',
            line=dict(width=size, color=vec_color),
            name=vec_name,
            legendgroup=vec_name,
            showlegend=True
        ))

        self.config.add_trace(go.Cone(x=[x1], y=[y1],
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

    # still in development
    # range must be a tuple

    def sketch_circle(self, radius, range, around_axis, size=4):
        min, max = range
        theta = np.linspace(min, max, 100)
        if around_axis == 'x':
            y = radius * np.cos(theta)
            z = radius * np.sin(theta)
            x = np.zeros_like(theta)
        elif around_axis == 'y':
            x = radius * np.cos(theta)
            z = radius * np.sin(theta)
            y = np.zeros_like(theta)
        else:
            x = radius * np.cos(theta)
            y = radius * np.sin(theta)
            z = np.zeros_like(theta)

        self.config.add_trace(go.Scatter3d(
            x=x,
            y=y,
            z=z,
            mode='lines',
            line=dict(width=size, color='blue'),
            name=f'circle-r{radius}',
            showlegend=False
        ))


class sketch_cartesian:
    def __init__(self):
        self.reinitialize(is_first_time=True)

    def reinitialize(self, is_first_time=True):
        self.fig = go.Figure()
        self.sk = sketch_element(self.fig)
        if is_first_time:
            self.counter = 1
            self.vectors = []
            self.larger_z = self.larger_y = self.larger_x = 1

    def add_input_vector(self, vector):
        # defin inputed vector
        input_vector = {"start": (0, 0, 0), "end": (
            vector[0], vector[1], vector[2]),
            "name": f"vector-{self.counter}"}
        self.counter += 1

        # re sketch every inputed vector
        for i in self.vectors:
            self.sk.sketch_vector(i)
        self.sk.sketch_vector(input_vector)

        # add the new vector to vectors list
        self.vectors.append(input_vector)

    def create_cartesian_sketch(self, strdata=[]):
        self.reinitialize(is_first_time=False)
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
        unitVectors = [
            {"start": (0, 0, 0), "end": (self.larger_x, 0, 0),
                "name": "x-axis"},
            {"start": (0, 0, 0), "end": (0, self.larger_y, 0),
                "name": "y-axis"},
            {"start": (0, 0, 0), "end": (0, 0, self.larger_z),
                "name": "z-axis"},
            {"start": (0, 0, 0), "end": (-self.larger_x, 0, 0),
                "name": "negative x-axis"},
            {"start": (0, 0, 0), "end": (0, -self.larger_y, 0),
                "name": "negative y-axis"},
            {"start": (0, 0, 0), "end": (0, 0, -self.larger_z),
                "name": "negative z-axis"}
        ]
        # sketch unit vectors
        for unitVector in unitVectors:
            self.sk.sketch_vector(unitVector, size=8)

        # sketch grid lines betweem x,y axises
        x_points = np.linspace(self.larger_x, -self.larger_x, 10)
        y_points = np.linspace(self.larger_y, -self.larger_y, 10)
        for x in x_points:
            self.fig.add_trace(go.Scatter3d(
                x=[x, x],
                y=[self.larger_y, -self.larger_y],
                z=[0, 0],
                mode='lines',
                line=dict(width=2, color='lightgray'),
                showlegend=False
            ))
        for y in y_points:
            self.fig.add_trace(go.Scatter3d(
                x=[self.larger_x, -self.larger_x],
                y=[y, y],
                z=[0, 0],
                mode='lines',
                line=dict(width=2, color='lightgray'),
                showlegend=False
            ))
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
            return self.fig.to_html(
                full_html=False, include_plotlyjs=True, config={"responsive": True})

        # add the input vector data must be 3
        if not len(vector) == 3:
            return "<h>There was somthing wrong with the input data" \
                "it should be 3</h>"
        self.add_input_vector(vector)

        # Convert figure to HTML
        plot_html = self.fig.to_html(
            full_html=False, include_plotlyjs=True, config={"responsive": True})

        return plot_html
