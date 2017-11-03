var widgets = require('@jupyter-widgets/base');
var _ = require('underscore');
var E = require('./libs/earth/1.0.0/earth.js');

// Custom Model. Custom widgets models must at least provide default values
// for model attributes, including
//
//  - `_view_name`
//  - `_view_module`
//  - `_view_module_version`
//
//  - `_model_name`
//  - `_model_module`
//  - `_model_module_version`
//
//  when different from the base class.

// When serialiazing the entire widget state for embedding, only values that
// differ from the defaults will be specified.
var EarthModel = widgets.DOMWidgetModel.extend({
    //defaults: _.extend(widgets.DOMWidgetModel.prototype.defaults(), {
    defaults: _.extend({}, widgets.WidgetModel.prototype.defaults, {

        _model_name : 'EarthModel',
        _view_name : 'EarthView',
        _model_module : 'ipyearth',
        _view_module : 'ipyearth',
        _model_module_version : '0.1.0',
        _view_module_version : '0.1.0',
        width : "600px",
        height : "400px",
    })
});


// Custom View. Renders the widget model.
var EarthView = widgets.DOMWidgetView.extend({
    render: function() {
        this.el.style['width'] = this.model.get('width');
        this.el.style['height'] = this.model.get('height');
        //this.value_changed();
        //this.model.on('change:value', this.value_changed, this);
        this.displayed.then(_.bind(this.render_earth, this));
    },

    //value_changed: function() {
    //    this.el.textContent = this.model.get('value');
    //}

    render_earth: function () {
        this.create_obj();
        //this.layer_views.update(this.model.get('layers'));
        //this.control_views.update(this.model.get('controls'));
        //this.leaflet_events();
        //this.model_events();
        //this.update_bounds();
        // TODO: hack to get all the tiles to show.
        //var that = this;
        //window.setTimeout(function () {
        //    that.obj.invalidateSize();
        //}, 1000);
        //return that;
        return this;
    },

    create_obj: function () {
        this.obj = E.map(this.el);
        //this.obj = E.test(this.el);
    }

});


module.exports = {
    EarthModel : EarthModel,
    EarthView : EarthView
};
