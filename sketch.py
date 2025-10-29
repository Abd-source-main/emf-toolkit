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


# data must be a list of dictionaries with start and end points
# with name and optional size
def sketch_vector(vec, config, size=6):
    start = x0, y0, z0 = vec["start"]
    end = x1, y1, z1 = vec["end"]
    vec_name = vec["name"]
    if vec_name[2:] == "axis":
        vec_color = "blue"
    else:
        vec_color = Vector_colors.get_color()
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

    # calculate vector length
    L = np.linalg.norm(np.array(end) - np.array(start))

    # Avoid division by zero
    L = max(L, 1e-6)

    # k is base size
    k = 0.9
    sizeref = k / L
    config.add_trace(go.Cone(x=[x1], y=[y1],
                             z=[z1],
                             u=[x1 - x0],
                             v=[y1 - y0],
                             w=[z1 - z0],
                             sizemode="absolute",
                             sizeref=0.2,
                             anchor="tip",
                             showscale=False,
                             colorscale=[[0, vec_color], [1, vec_color]],
                             legendgroup=vec_name,
                             showlegend=False
                             ))


def create_cartesian_sketch(strdata=[]):
    if not getattr(create_cartesian_sketch, "initialized", False):
        # setup counter for vector naming
        create_cartesian_sketch.counter = 1
        create_cartesian_sketch.vectors = []
        create_cartesian_sketch.larger_z = create_cartesian_sketch.larger_y = create_cartesian_sketch.larger_x = 1
        setattr(create_cartesian_sketch, "initialized", True)
    fig = go.Figure()

    # add the axes x,y,z
    # iykyk
    vector = [float(x) for x in strdata]
    if vector:
        create_cartesian_sketch.larger_x = abs(vector[0]) if abs(vector[0]) > abs(
            create_cartesian_sketch.larger_x) else create_cartesian_sketch.larger_x
        create_cartesian_sketch.larger_y = abs(vector[1]) if abs(vector[1]) > abs(
            create_cartesian_sketch.larger_y) else create_cartesian_sketch.larger_y
        create_cartesian_sketch.larger_z = abs(vector[2]) if abs(vector[2]) > abs(
            create_cartesian_sketch.larger_z) else create_cartesian_sketch.larger_z
    unitVectors = [
        {"start": (0, 0, 0), "end": (create_cartesian_sketch.larger_x, 0, 0),
            "name": "x-axis"},
        {"start": (0, 0, 0), "end": (0, create_cartesian_sketch.larger_y, 0),
            "name": "y-axis"},
        {"start": (0, 0, 0), "end": (0, 0, create_cartesian_sketch.larger_z),
            "name": "z-axis"}
    ]
    # sketch unit vectors
    for unitVector in unitVectors:
        sketch_vector(unitVector, fig,
                      size=8)

    # add padding
    x_padding = create_cartesian_sketch.larger_x + 0.3
    y_padding = create_cartesian_sketch.larger_y + 0.3
    z_padding = create_cartesian_sketch.larger_z + 0.3

    # Determan the max range for the figure
    fig.update_layout(
        scene=dict(
            aspectmode="cube",
            xaxis=dict(range=[-x_padding, x_padding]),
            yaxis=dict(range=[-y_padding, y_padding]),
            zaxis=dict(range=[-z_padding, z_padding]),
        )
    )

    fig.update_layout(
        autosize=True,
        margin=dict(l=0, r=0, t=0, b=0),
        height=None,
    )
   # if it was called for only the axises
    if not vector or vector[0] == vector[1] == vector[2] == 0:
        return fig.to_html(
            full_html=False, include_plotlyjs=True, config={"responsive": True})

    # add the input vector (data must be multiple of 3)
    if not len(vector) == 3:
        return "<h>There was somthing wrong with the input data" \
            "it should be 3</h>"
    # defin inputed vector
    input_vector = {"start": (0, 0, 0), "end": (
        vector[0], vector[1], vector[2]),
        "name": f"vector-{create_cartesian_sketch.counter}"}
    create_cartesian_sketch.counter += 1
    # add it to vectors list
    create_cartesian_sketch.vectors.append(input_vector)
    # re sketch every inputed vector
    for i in create_cartesian_sketch.vectors:
        sketch_vector(i, fig)
    sketch_vector(input_vector, fig)

    # Convert figure to HTML
    plot_html = fig.to_html(
        full_html=False, include_plotlyjs=True, config={"responsive": True})

    return plot_html
