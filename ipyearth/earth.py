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
    topology = Unicode('').tag(sync=True)
    vector_field = Unicode('').tag(sync=True)
    overlay = Unicode('').tag(sync=True)

    def set_projection(self, projection):
        self.projection = projection

    def show_topology(self, topology):
        self.topology = topology

    def show_wind(self, vector_field):
        self.overlay = 'wind'
        self.vector_field = vector_field

    def show_ocean(self, vector_field):
        self.overlay = 'ocean'
        self.vector_field = vector_field

    def show_overlay(self, overlay):
        self.overlay = overlay
