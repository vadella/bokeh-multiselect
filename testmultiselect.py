""" Example demonstrating turning lines on and off - with JS only

"""

import numpy as np
import itertools
from collections import OrderedDict

from bokeh.io import push_notebook, show, output_notebook, output_file
from bokeh.layouts import row
from bokeh.palettes import Set1_6
from bokeh.plotting import figure as bf
from bokeh.models import MultiSelect, CustomJS, Range1d, LinearAxis, ColumnDataSource
from bokeh.resources import CDN
output_notebook()

def generate_example_data(x, param=1):
	
	t = 20 + param + np.sin(x * (1 + param))
	rh = 50 + param + 10 * np.tan(x * (1 + param))
	return {"x": x.copy(), "t": t, "rh": rh}

def generate_selector_code(locations):
	for index, location in enumerate(locations):
		res_str = """    if (%(index)i in multiselect.attributes.value) {
		%(loc)s_t.visible = true;
		%(loc)s_rh.visible = true;
		console.log('enabling0 %(loc)s' );
	} else {
		%(loc)s_t.visible = false;
		%(loc)s_rh.visible = false;
		console.log('disabling0 %(loc)s' );
	}
	if ('%(index)i' in multiselect.attributes.value) {
		%(loc)s_t.visible = true;
		%(loc)s_rh.visible = true;
		console.log('enabling1 %(loc)s' );
	} else {
		%(loc)s_t.visible = false;
		%(loc)s_rh.visible = false;
		console.log('disabling1 %(loc)s' );
	}
	if ('%(loc)s' in multiselect.attributes.value) {
		%(loc)s_t.visible = true;
		%(loc)s_rh.visible = true;
		console.log('enabling2 %(loc)s' );
	} else {
		%(loc)s_t.visible = false;
		%(loc)s_rh.visible = false;
		console.log('disabling2 %(loc)s' );
	}
	"""%({"index": index, "loc": location})
# other method's I've tested but which result into an error which states that Object does not have an attribute includes
#     if (multiselect.attributes.value.includes('%(index)i')) {
#         %(loc)s_t.visible = true;
#         %(loc)s_rh.visible = true;
#         console.log('enabling3 %(loc)s' );
#     } else {
#         %(loc)s_t.visible = false;
#         %(loc)s_rh.visible = false;
#         console.log('disabling3 %(loc)s' );
#     }
#     if (multiselect.attributes.value.includes('%(loc)s')) {
#         %(loc)s_t.visible = true;
#         %(loc)s_rh.visible = true;
#         console.log('enabling4 %(loc)s' );
#     } else {
#         %(loc)s_t.visible = false;
#         %(loc)s_rh.visible = false;
#         console.log('disabling4 %(loc)s' );
#     }

		yield res_str

locations = ["loc_one", "loc_two", "loc_three"]
x = np.linspace(0, 4 * np.pi, 20)
data_per_loc = OrderedDict()
for i, loc in enumerate(locations):
	data_per_loc[loc] = generate_example_data(x, i)
	
tools="pan,box_zoom,reset,resize,save,crosshair,hover,xbox_zoom, wheel_zoom"

def generate_plot(data_per_loc):    
	
	palet = itertools.cycle(Set1_6)
	p = bf(title="test", plot_height=500, plot_width=1000, tools=tools, y_range=(17, 27), 
	   toolbar_location="above")
	p.xaxis.axis_label = "x"

	p.yaxis.axis_label = "Temperature [°C]"
	p.extra_y_ranges = {"humidity": Range1d(start=30, end=80)}
	p.add_layout(LinearAxis(y_range_name="humidity", axis_label="Relative Humidity [%Rh]"), 'right')

	plot_locations = OrderedDict()
	for location, datadict in data_per_loc.items():
		colour = next(palet)
		source = ColumnDataSource(datadict)
		t = p.line(x='x', y='t', color=colour, source=source, legend=location)
		rh = p.line(x='x', y='rh', source=source, color=colour,
			   legend=location, y_range_name='humidity',
			   line_dash="dashed", )
		plot_locations.update({location+"_t": t, location+"_rh": rh})

	code = "console.log('value: ' + multiselect.attributes.value);\n " + "console.log('value_type: ' + Object.prototype.toString.call(multiselect.attributes.value).slice(8, -1));\n " +             "console.log('options: ' + multiselect.attributes.options);\n " + "".join(generate_selector_code(data_per_loc.keys()))
	return p, code, plot_locations

output_file("c:\html\multiselect_val.html")
p, code, plot_locations = generate_plot(data_per_loc) 

ms_options = [(str(i), v) for i , v in enumerate(locations)]
ms_value = [str(i) for i in range(len(locations))]

callback = CustomJS(code=code, args={})
multiselect = MultiSelect(title="Location:", options=ms_options value=ms_value, callback=callback)
callback.args = dict(**plot_locations, multiselect=multiselect)


layout = row(p, multiselect)
show(layout)


output_file("c:\html\multiselect_loc.html")
p, code, plot_locations = generate_plot(data_per_loc)

ms_options = locations
ms_value = locations

callback = CustomJS(code=code, args={})
multiselect = MultiSelect(title="Location:", options=ms_options, value=ms_value, callback=callback)
callback.args = dict(**plot_locations, multiselect=multiselect)


layout = row(p, multiselect)
show(layout)




