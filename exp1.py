from itertools import product
import numpy as np
from typing import List, Tuple
import streamlit as st
import math
import pandas as pd
import plotly.express as px


def draw_mesh(_mesh):
    df_mesh = pd.DataFrame(data=_mesh, columns=["theta", "alpha"])

    fig1 = px.scatter(df_mesh, x='alpha', y='theta')
    st.plotly_chart(fig1)


st.subheader("Generate Mesh in Spherical Coordinate space")
with st.echo():
    def generate_a_square_grid(start = 0, end = 10, n = 10) -> List[Tuple[float, float]]:
        interpolated_sides = np.linspace(start, end, n)
        cartesian_coupling = [* product(interpolated_sides,interpolated_sides)]
        return cartesian_coupling


    mesh = generate_a_square_grid(start=0, end=2 * np.pi, n=30)

    draw_mesh(mesh)



st.subheader("Rotate Mesh in Spherical Coordinate space")

degrees = st.slider("spherical mesh rotation", 0,360, 0)



with st.echo():
    def rotatePoint(center_point, point, angle):
        """Rotates a point around another centerPoint. Angle is in degrees.
        Rotation is counter-clockwise"""
        angle = math.radians(angle)
        temp_point = point[0] - center_point[0] , point[1] - center_point[1]
        temp_point = ( temp_point[0]*math.cos(angle)-temp_point[1]*math.sin(angle) , temp_point[0]*math.sin(angle)+temp_point[1]*math.cos(angle))
        temp_point = temp_point[0] + center_point[0] , temp_point[1] + center_point[1]
        return temp_point

    mesh = [*map(lambda x: rotatePoint((np.pi, np.pi), x, degrees), mesh)]

    draw_mesh(mesh)




st.subheader("Transform rotated spherical coordinates to cartesian")
with st.echo():
    def spherical_to_cartesian(theta, alpha, r=1):
        x = r * np.sin(theta) * np.cos(alpha)
        y = r * np.sin(theta) * np.sin(alpha)
        z = r * np.cos(theta)
        return x, y, z

    cartesian_coords = [*map(lambda x: spherical_to_cartesian(theta= x[0], alpha=x[1]), mesh )]


df = pd.DataFrame(data = cartesian_coords, columns= ["x","y","z"])
fig = px.scatter_3d(df, x='x', y='y', z='z')
st.plotly_chart(fig, width = 800)

st.subheader("Citations")

st.text("- https://en.wikipedia.org/wiki/Spherical_coordinate_system")
st.text("- http://tutorial.math.lamar.edu/Classes/CalcIII/SphericalCoords.aspx")
st.text("- https://gist.github.com/somada141/d81a05f172bb2df26a2c")

st.subheader("Citations ( future work )")
st.text("- https://en.wikipedia.org/wiki/Conformal_map")
st.text("- https://stackoverflow.com/questions/40778440/conformal-maps-algorithm")
st.text("- http://www.cs.cmu.edu/~kmcrane/Projects/Other/OverviewConformalGeometryProcessing.pdf")
