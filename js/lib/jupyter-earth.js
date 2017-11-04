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
        width : "100%",
        height : "600px",
    })
});


// Custom View. Renders the widget model.
var EarthView = widgets.DOMWidgetView.extend({
    render: function() {
        this.el.style['width'] = this.model.get('width');
        this.el.style['height'] = this.model.get('height');
        this.model.on('change:projection', this.projection_changed, this);
        this.model.on('change:topology', this.topology_changed, this);
        this.model.on('change:vector_field', this.vector_field_changed, this);
        this.displayed.then(_.bind(this.render_earth, this));
    },

    projection_changed: function() {
        this.obj.configuration.save({projection: this.model.get('projection')});
    },

    topology_changed: function() {
        this.obj.configuration.save({topology: JSON.parse(this.model.get('topology'))});
    },

    vector_field_changed: function() {
        var vector_field = this.model.get('vector_field');
        if (vector_field === 'off')
            this.obj.configuration.save({param: 'off'});
        else
            this.obj.configuration.save({param: 'wind', overlayType: 'vector_field', vector_data: JSON.parse(vector_field)});
    },

    render_earth: function () {
        this.create_obj();
        return this;
    },

    create_obj: function () {
        this.obj = E.map(this.el);
    }

});


module.exports = {
    EarthModel : EarthModel,
    EarthView : EarthView
};
