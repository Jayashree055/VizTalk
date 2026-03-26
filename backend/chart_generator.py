import plotly.express as px

def create_chart(df):

    x = df.columns[0]
    y = df.columns[1]

    fig = px.bar(df, x=x, y=y)

    return fig