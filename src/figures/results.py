import plotly.graph_objects as go
import plotly.offline
import plotly.graph_objects as go

options = {
    "template": 'presentation+plotly_dark', 
    "autosize":True 
}

fig = go.Figure(go.Bar(
            x=[0.48, 0.69],
            y=['5-nearest neighbor', 'gender baseline'],
            orientation='h',  marker_color=['indianred', 'gray']),
            layout=go.Layout(
        title=go.layout.Title(text="test f-score")
    ))

fig.update_layout(**options)
plotly.offline.plot(fig, filename='docs/figures/results.html')

fig = go.Figure(go.Bar(
            x=[0.48, 0.69, 0.72, 0.71],
            y=['5-nearest neighbor', 'gender baseline', 'logistic regression', 'random forrest'],
            orientation='h', marker_color=['gray', 'gray', 'indianred', 'indianred']),
            layout=go.Layout(
        title=go.layout.Title(text="test f-score")
    ))

fig.update_layout(**options)
plotly.offline.plot(fig, filename='docs/figures/results_classification.html')

