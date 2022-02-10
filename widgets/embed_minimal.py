import altair as alt
from vega.widget import VegaWidget
from vega_datasets import data
from ipywidgets.embed import embed_minimal_html

p = (
    alt.Chart(data.cars())
    .mark_point()
    .encode(
        x="Horsepower",
        y="Miles_per_Gallon",
        color="Origin",
    )
)
w = VegaWidget(p.to_dict())
embed_minimal_html("index.html", views=[w], title="Vega Widget")
