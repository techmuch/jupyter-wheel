import ipywidgets as widgets
from traitlets import Unicode

from IPython.display import display # Used to display widgets in the notebook
from IPython.display import Javascript # Used to insert javascript in the notebook
from IPython.display import HTML # Used to insert HTML in the notebook

# Thank you to the authors of the example starbust chart within the D3 examples

html = '''
<style>
path {
  stroke: #fff;
  fill-rule: evenodd;
}

text {
  font-family: Arial, sans-serif;
  font-size: 12px;
}
</style>
'''

script = '''
requirejs.undef("wheel_view");

require.config({
  paths: {
    "hamster": "http://monospaced.github.io/hamster.js/hamster",
    "d3": "https://cdn.jsdelivr.net/d3js/3.5.12/d3.min"
  },
  shim: {
    'd3': {
      deps: [],
      exports: 'd3'
    }
  }
});

require(
[
    "nbextensions/widgets/widgets/js/widget",
    "nbextensions/widgets/widgets/js/manager",
    "jquery",
    "d3",
    "hamster",
    "underscore"
],
function(widget, manager, $, d3, Hamster, _){
    "use strict";
    console.log("WheelView was required");
    
    // Define the WheelView
    var WheelView = widget.DOMWidgetView.extend({
        render: function(){
           
            var self = this,
                width = $(element).width(),
                height =$(element).width() + 25,
                radius = Math.min(width, height) / 2;

            var x = d3.scale.linear()
                .range([0, 2 * Math.PI]);

            var y = d3.scale.linear()
                .range([0, radius]);

            var color = this.color = ['#BDBDBD','#31A354'];

            var svg = d3.select(this.el).append("svg")
                .attr("width", width)
                .attr("height", height)
                .append("g")
                .attr("transform", "translate(" + width / 2 + "," + (height / 2 + 10) + ")");
            
            var ang = 0;
            
            Hamster(this.el).wheel(function(e, delta, deltaX, deltaY){
                //debugger
                e.preventDefault();
                e.stopPropagation();
                ang = ang + (10 * delta);
                d3.select($(e.originalEvent.currentTarget).find('svg g')[0])
                    .transition()
                    .duration(200)
                    .attr("transform", "translate(" + width / 2 + "," + (height / 2 + 10) + "), rotate(" + ang + ")");
            })

            var partition = this.partition = d3.layout.partition()
                .value(function(d) { return d.size ? d.size : 1; });
            
            var arc = this.arc = d3.svg.arc()
                .startAngle(function(d) { return Math.max(0, Math.min(2 * Math.PI, x(d.x))); })
                .endAngle(function(d) { return Math.max(0, Math.min(2 * Math.PI, x(d.x + d.dx))); })
                .innerRadius(function(d) { return Math.max(0, y(d.y)); })
                .outerRadius(function(d) { return Math.max(0, y(d.y + d.dy)); });

            d3.select(self.frameElement).style("height", height + "px");

            // Interpolate the scales!
            function arcTween(d) {
              var xd = d3.interpolate(x.domain(), [d.x, d.x + d.dx]),
                  yd = d3.interpolate(y.domain(), [d.y, 1]),
                  yr = d3.interpolate(y.range(), [d.y ? 20 : 0, radius]);
              return function(d, i) {
                return i
                    ? function(t) { return arc(d); }
                    : function(t) { x.domain(xd(t)); y.domain(yd(t)).range(yr(t)); return arc(d); };
              };
            }

            function computeTextRotation(d) {
              return (x(d.x + d.dx / 2) - Math.PI / 2) / Math.PI * 180;
            }
           
            var jstring = this.model.get('value') ? this.model.get('value') : "{}";
            var root = JSON.parse(jstring)
            var g = this.g = svg.selectAll("g")
                .data(partition.nodes(root))
                .enter().append("g");

            var path = this.path = g.append("path")
                .attr("d", arc)
                .style("fill", function(d) {
                    d.active = d.active ? true : false
                    return d.active || d.center ? color[1] : color[0];
                })
                .on("click", click);
            
            function click(d) {
                    var jstring = self.model.get('value') ? self.model.get('value') : "{}";
                    var root = JSON.parse(jstring)
                    d.active = d.active ? false : true;
                    //path.style("fill", function(d) { return d.active ? color[1] : color[0]; });
                    debugger
                    var newString = JSON.stringify(root, function(key, val) {
                      //debugger
                      if (Array.isArray(val)){
                          return val
                      }
                      if (val != null && typeof val == "object") {
                          val = _.pick(val, 'name', 'children', 'active', 'id');
                          if(d.id == val.id){
                              val.active = d.active;
                          }
                          else{
                            val.active = val.active ? true : false;  
                          }
                          val.children = Array.isArray(val.children) ? val.children : [];
                          
                          return val
                      }
                      return val
                    })
                    self.model.set('value', newString)
                  console.log('clicked')
                  self.touch()
                  self.update()
            }

            var text = this.text = g.append("text")
                .attr("transform", function(d) { return "rotate(" + computeTextRotation(d) + ")"; })
                .attr("x", function(d) { return y(d.y); })
                .attr("dx", "6") // margin
                .attr("dy", ".35em") // vertical-align
                .text(function(d) { return d.name; });

            
            
            this.model.on('change:value', this.update, this);
        },
        
        update: function(){
            var color = this.color,
                g = this.g,
                path = this.path,
                partition = this.partition;
            
            var jstring = this.model.get('value') ? this.model.get('value') : "{}";
            var root = JSON.parse(jstring)
            
            path.data(partition.nodes(root))
            path.style("fill", function(d) { return d.active ? color[1] : color[0]; });
            console.log('updated')
            //debugger
        }
    });
    
    // Register the HelloView with the widget manager.
    manager.WidgetManager.register_widget_view('WheelView', WheelView);
});
'''

display(HTML(html))
display(Javascript(script))

class Wheel(widgets.DOMWidget):
    _view_name = Unicode('WheelView', sync=True)
    value = Unicode('{\"name\":\"Missing Value Property\"}', sync=True)
    