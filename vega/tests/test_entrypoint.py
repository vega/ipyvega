import altair as alt
import altair.vega as alt_vg
from vega import vega, vegalite


def test_entrypoint_exists():
    assert "notebook" in alt.renderers.names()
    assert "notebook" in alt_vg.renderers.names()


def test_entrypoint_identity():
    with alt.renderers.enable("notebook"):
        assert alt.renderers.get() is vegalite.entry_point_renderer
    with alt.vega.renderers.enable("notebook"):
        assert alt_vg.renderers.get() is vega.entry_point_renderer
