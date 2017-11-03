from ipywidgets import register, DOMWidget, Layout
from traitlets import Unicode, default

@register
class Earth(DOMWidget):
    @default('layout')
    def _default_layout(self):
        return Layout(height='600px', align_self='stretch')

    _view_name = Unicode('EarthView').tag(sync=True)
    _model_name = Unicode('EarthModel').tag(sync=True)
    _view_module = Unicode('ipyearth').tag(sync=True)
    _model_module = Unicode('ipyearth').tag(sync=True)
    _view_module_version = Unicode('^0.1.0').tag(sync=True)
    _model_module_version = Unicode('^0.1.0').tag(sync=True)
    projection = Unicode('orthographic').tag(sync=True)
    #with open('/home/david/git/ipyearth/examples/data/earth-topo.json') as f:
    #    topo_json = f.read()
    topology = Unicode('').tag(sync=True)
