from ipywidgets import register, DOMWidget, Layout
from traitlets import Unicode, default
import json
import copy
from .simplify import simplify

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

    def show_topology(self, file_name=None, object_name=None):
        if file_name is not None:
            with open(file_name) as f:
                topo_dict = json.load(f)
        if object_name is not None:
            topo_dict['objects'] = {'topoHi': topo_dict['objects'][object_name]}
        arcsLo = []
        arcsHi = topo_dict['arcs']
        quantized = 'transform' in topo_dict
        for arcHi in arcsHi:
            pointsHi = [{'x': xy[0], 'y': xy[1]} for xy in arcHi]
            if quantized:
                xy_prev = {'x': 0, 'y': 0}
                for xy in pointsHi:
                    xy['x'] = xy['x'] + xy_prev['x']
                    xy['y'] = xy['y'] + xy_prev['y']
                    xy_prev = xy
            pointsLo = simplify(pointsHi, tolerance=5, highestQuality=False)
            if quantized:
                xy_prev = {'x': 0, 'y': 0}
                for xy in pointsLo:
                    xy_keep = dict(xy)
                    xy['x'] = xy['x'] - xy_prev['x']
                    xy['y'] = xy['y'] - xy_prev['y']
                    xy_prev = xy_keep
            arcsLo.append([[xy['x'], xy['y']] for xy in pointsLo])
        arc_len = len(arcsHi)
        topo_dict['arcs'] += arcsLo
        topo_dict['objects']['topoLo'] = copy.deepcopy(topo_dict['objects']['topoHi'])
        def offset_values(values, const):
            for i, v in enumerate(values):
                if type(v) is list:
                    offset_values(v, const)
                else:
                    value = values[i]
                    if value < 0:
                        values[i] = -(-value + const)
                    else:
                        values[i] = value + const
        for geometry in topo_dict['objects']['topoLo']['geometries']:
            arcs = geometry['arcs']
            offset_values(arcs, arc_len)
        self.topology = json.dumps(topo_dict)

    def show_wind(self, vector_field):
        self.overlay = 'wind'
        self.vector_field = vector_field

    def show_ocean(self, vector_field):
        self.overlay = 'ocean'
        self.vector_field = vector_field

    def show_overlay(self, overlay):
        self.overlay = overlay
