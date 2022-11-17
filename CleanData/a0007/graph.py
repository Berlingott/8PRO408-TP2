import os
import pandas as pd
import plotly.express as px

data = pd.read_csv([file for file in os.listdir() if file.endswith('.csv')][0])
data.columns = ['acoustic pressure']
data['time (s)'] = data.index/16000
fig = px.line(data, x='time (s)', y='acoustic pressure')

# Works only when installing kaleido as "pip install kaleido==0.2.1.post1"
# Discussion: https://github.com/plotly/Kaleido/issues/134
fig.write_image("graph.png")