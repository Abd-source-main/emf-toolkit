import plotly.graph_objects as go


def create_sketch_figure():
    fig = go.Figure()

    fig.add_trace(go.Scatter3d(
        x=[1, 2, 3],
        y=[4, 5, 6],
        z=[7, 8, 9],
        mode='markers',
        marker=dict(size=5, color='blue')
    ))

    fig.update_layout(scene=dict(
        xaxis_title='X', yaxis_title='Y', zaxis_title='Z', aspectmode='cube'))
    # Convert figure to HTML
    plot_html = fig.to_html(full_html=False, include_plotlyjs=True)

    return plot_html
