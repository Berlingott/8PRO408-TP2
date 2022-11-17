import os
import pandas as pd
import plotly.express as px

data = pd.read_csv([file for file in os.listdir() if file.endswith('.csv')][1])
fig = px.scatter(data)
fig.write_image("graph.png")