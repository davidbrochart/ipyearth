from ipywidgets import register, DOMWidget, Layout
from traitlets import Unicode, Float, List, default
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
    animate = Unicode('').tag(sync=True)
    vector_show = Unicode('').tag(sync=True)
    overlay = Unicode('').tag(sync=True)
    overlayType = Unicode('').tag(sync=True)
    param = Unicode('').tag(sync=True)
    color_map = Unicode('').tag(sync=True)
    color_vmin = Float(0).tag(sync=True)
    color_vmax = Float(0).tag(sync=True)
    particleVelocityScale = Float(0).tag(sync=True)
    particleMaxIntensity = Float(0).tag(sync=True)

    _coord = List([]).tag(sync=True)

    @property
    def coord(self):
        return self._coord[::-1]

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
            pointsLo = simplify(pointsHi, tolerance=10, highestQuality=True)
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

    def show(self, animate=None, overlay=None):
        self.param = 'off'
        self.overlayType = 'off'
        if animate is None:
            self.vector_show = 'false'
        else:
            u = [val if val * 0 == 0 else 'null' for val in animate['u'].flatten().tolist()]
            v = [val if val * 0 == 0 else 'null' for val in animate['v'].flatten().tolist()]
            dx = animate['dx']
            dy = animate['dy']
            nx = animate['nx']
            ny = animate['ny']
            la1 = animate['ullat']
            lo1 = animate['ullon']
            la2 = int(la1 - (ny - 1) * dy)
            lo2 = int(lo1 + (nx - 1) * dx)
            self.animate = json.dumps([{'header': {'nx': nx, 'ny': ny, 'lo1': lo1, 'la1': la1, 'lo2': lo2, 'la2': la2, 'dx': dx, 'dy': dy}, 'data': u}, {'header': {'nx': nx, 'ny': ny, 'lo1': lo1, 'la1': la1, 'lo2': lo2, 'la2': la2, 'dx': dx, 'dy': dy}, 'data': v}])
            self.vector_show = 'true'
            self.param = 'wind'
            self.overlayType = 'wind'
        if overlay == 'fromAnim':
            self.param = 'wind'
            self.overlayType = 'wind'
        elif overlay is not None:
            data = [val if val * 0 == 0 else 'null' for val in overlay['data'].flatten().tolist()]
            dx = overlay['dx']
            dy = overlay['dy']
            nx = overlay['nx']
            ny = overlay['ny']
            la1 = overlay['ullat']
            lo1 = overlay['ullon']
            la2 = int(la1 - (ny - 1) * dy)
            lo2 = int(lo1 + (nx - 1) * dx)
            self.overlay = json.dumps([{'header': {'nx': nx, 'ny': ny, 'lo1': lo1, 'la1': la1, 'lo2': lo2, 'la2': la2, 'dx': dx, 'dy': dy}, 'data': data}])
            self.param = 'wind'
            self.overlayType = 'temp'
        else:
            self.overlayType = 'off'
