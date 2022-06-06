# Notes for Visualisation Session

- Automation (e.g. using a function to apply same style to all elements)
- Automation (e.g. using a function to create a comparable plot for each columns)
- Add MSOA Names data.
- Good review of doing stuff using Airbnb data and matplotlib https://darribas.org/gds_course/content/bG/lab_G.html (especially tiling of outputs). See also: K-means.
- Linking points to polygons (including hexbinning); and interaction via ipywidges+function for mapping! https://darribas.org/gds_course/content/bH/lab_H.html (especially contextily) 
- https://darribas.org/gds_course/content/slides/block_D_iii.html#/choropleths (good content on classification)
- https://darribas.org/gds_course/content/bD/lab_D.html#quantiles (also good for classification: combine the varioius plots together)

### Showing Off Plots

Focus on the organisation: https://seaborn.pydata.org/_images/function_overview_8_0.png

Line plot
Bar plot
Dist plot
KDE plot
Violin plot
Joint plots (2D versions of the above + hexplots)
Pair plot
Swarm plot
Lmplot
Pair grid
FacetGrid
Factor plot

### Getting at Matplotlib

- Figure size, height, aspect ratio
- Dealing with one figure / multiple figures: subplots, sharey and sharex, gridspec, 
- Drawing lines (vertical, horizontal, otherwise)
- Axis limits
- Axis tics
- Axis labels
- Axis names
- Rotating labels
- Figure titles
- Legends
- Annotation 
- PiP: https://stackoverflow.com/a/34862213

#### Bokeh

Providing data: https://docs.bokeh.org/en/latest/docs/user_guide/data.html

Specifying a layout: https://docs.bokeh.org/en/latest/docs/user_guide/layout.html

Colour: https://docs.bokeh.org/en/latest/docs/user_guide/styling.html

Annotation: https://docs.bokeh.org/en/latest/docs/user_guide/annotations.html (and see especially Bands: https://docs.bokeh.org/en/latest/docs/user_guide/annotations.html#bands; then Spans and Slopes)

Specifying Tools: https://docs.bokeh.org/en/latest/docs/user_guide/tools.html (Tooltips: https://docs.bokeh.org/en/latest/docs/user_guide/tools.html#basic-tooltips)

This creates a standalone plotting file

```python
from bokeh.plotting import figure, output_file, show

# output to static HTML file
output_file("foo.html")

# create a new plot with a title and axis labels
p = figure(title="simple line example", x_axis_label='x', y_axis_label='y')

# add a line renderer with legend and line thickness
p.line(x, y, legend_label="Temp.", line_width=2)

# show the results
show(p)
```

For notebooks:

Change `output_file` to `output_notebook`.

```python
from bokeh.plotting import figure, output_file, show

# prepare some data
x = [0.1, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0]
y0 = [i**2 for i in x]
y1 = [10**i for i in x]
y2 = [10**(i**2) for i in x]

# output to static HTML file
output_file("log_lines.html")

# create a new plot
p = figure(
   tools="pan,box_zoom,reset,save",
   y_axis_type="log", y_range=[0.001, 10**11], title="log axis example",
   x_axis_label='sections', y_axis_label='particles'
)

# add some renderers
p.line(x, x, legend_label="y=x")
p.circle(x, x, legend_label="y=x", fill_color="white", size=8)
p.line(x, y0, legend_label="y=x^2", line_width=3)
p.line(x, y1, legend_label="y=10^x", line_color="red")
p.circle(x, y1, legend_label="y=10^x", fill_color="red", line_color="red", size=6)
p.line(x, y2, legend_label="y=10^x^2", line_color="orange", line_dash="4 4")

# show the results
show(p)
```

Range:

`p = figure(x_range=[start,finish], y_range=[start,finish])`

Colour and Tools:

```python
import numpy as np

from bokeh.plotting import figure, output_file, show

# prepare some data
N = 4000
x = np.random.random(size=N) * 100
y = np.random.random(size=N) * 100
radii = np.random.random(size=N) * 1.5
colors = [
    "#%02x%02x%02x" % (int(r), int(g), 150) for r, g in zip(50+2*x, 30+2*y)
]

# output to static HTML file (with CDN resources)
output_file("color_scatter.html", title="color_scatter.py example", mode="cdn")

TOOLS = "crosshair,pan,wheel_zoom,box_zoom,reset,box_select,lasso_select"

# create a new plot with the tools above, and explicit ranges
p = figure(tools=TOOLS, x_range=(0, 100), y_range=(0, 100))

# add a circle renderer with vectorized colors and sizes
p.circle(x, y, radius=radii, fill_color=colors, fill_alpha=0.6, line_color=None)

# show the results
show(p)
```

Multiple figures on one plot and linked panning/brushing:

```python
import numpy as np

from bokeh.layouts import gridplot
from bokeh.plotting import figure, output_file, show

# prepare some data
N = 100
x = np.linspace(0, 4*np.pi, N)
y0 = np.sin(x)
y1 = np.cos(x)
y2 = np.sin(x) + np.cos(x)

# output to static HTML file
output_file("linked_panning.html")

# create a new plot
s1 = figure(width=250, plot_height=250, title=None)
s1.circle(x, y0, size=10, color="navy", alpha=0.5)

# NEW: create a new plot and share both ranges
s2 = figure(width=250, height=250, x_range=s1.x_range, y_range=s1.y_range, title=None)
s2.triangle(x, y1, size=10, color="firebrick", alpha=0.5)

# NEW: create a new plot and share only one range
s3 = figure(width=250, height=250, x_range=s1.x_range, title=None)
s3.square(x, y2, size=10, color="olive", alpha=0.5)

# NEW: put the subplots in a gridplot
p = gridplot([[s1, s2, s3]], toolbar_location=None)

# show the results
show(p)
```

Linked selection using shared data source:

```python
import numpy as np
from bokeh.plotting import *
from bokeh.models import ColumnDataSource

# prepare some date
N = 300
x = np.linspace(0, 4*np.pi, N)
y0 = np.sin(x)
y1 = np.cos(x)

# output to static HTML file
output_file("linked_brushing.html")

# NEW: create a column data source for the plots to share
source = ColumnDataSource(data=dict(x=x, y0=y0, y1=y1))

TOOLS = "pan,wheel_zoom,box_zoom,reset,save,box_select,lasso_select"

# create a new plot and add a renderer
left = figure(tools=TOOLS, width=350, height=350, title=None)
left.circle('x', 'y0', source=source)

# create another new plot and add a renderer
right = figure(tools=TOOLS, width=350, height=350, title=None)
right.circle('x', 'y1', source=source)

# put the subplots in a gridplot
p = gridplot([[left, right]])

# show the results
show(p)
```

Mapping:

```python
from bokeh.plotting import figure, output_file, show
from bokeh.tile_providers import CARTODBPOSITRON, get_provider

output_file("tile.html")

tile_provider = get_provider(CARTODBPOSITRON)

# range bounds supplied in web mercator coordinates
p = figure(x_range=(-2000000, 6000000), y_range=(-1000000, 7000000),
           x_axis_type="mercator", y_axis_type="mercator")
p.add_tile(tile_provider)

show(p)
```

Bokeh’s `GeoJSONDataSource` can be used almost seamlessly in place of Bokeh’s `ColumnDataSource`. See, available tile providers: https://docs.bokeh.org/en/latest/docs/reference/tile_providers.html#bokeh-tile-providers For example:

```python
import json

from bokeh.io import output_file, show
from bokeh.models import GeoJSONDataSource
from bokeh.plotting import figure
from bokeh.sampledata.sample_geojson import geojson

output_file("geojson.html")

data = json.loads(geojson)
for i in range(len(data['features'])):
    data['features'][i]['properties']['Color'] = ['blue', 'red'][i%2]

geo_source = GeoJSONDataSource(geojson=json.dumps(data))

TOOLTIPS = [
    ('Organisation', '@OrganisationName')
]

p = figure(background_fill_color="lightgrey", tooltips=TOOLTIPS)
p.circle(x='x', y='y', size=15, color='Color', alpha=0.7, source=geo_source)

show(p)
```

Intervals

```python
from bokeh.io import output_file, show
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure
from bokeh.sampledata.sprint import sprint

output_file("sprint.html")

sprint.Year = sprint.Year.astype(str)
group = sprint.groupby('Year')
source = ColumnDataSource(group)

p = figure(y_range=group, x_range=(9.5,12.7), plot_width=400, plot_height=550, toolbar_location=None,
           title="Time Spreads for Sprint Medalists (by Year)")
p.hbar(y="Year", left='Time_min', right='Time_max', height=0.4, source=source)

p.ygrid.grid_line_color = None
p.xaxis.axis_label = "Time (seconds)"
p.outline_line_color = None

show(p)
```

Add jitter:

```python
from bokeh.io import output_file, show
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure
from bokeh.sampledata.commits import data
from bokeh.transform import jitter

output_file("bars.html")

DAYS = ['Sun', 'Sat', 'Fri', 'Thu', 'Wed', 'Tue', 'Mon']

source = ColumnDataSource(data)

p = figure(plot_width=800, plot_height=300, y_range=DAYS, x_axis_type='datetime',
           title="Commits by Time of Day (US/Central) 2012—2016")

p.circle(x='time', y=jitter('day', width=0.6, range=p.y_range),  source=source, alpha=0.3)

p.xaxis[0].formatter.days = ['%Hh']
p.x_range.range_padding = 0
p.ygrid.grid_line_color = None

show(p)
```

Ridge Plot

```python
import colorcet as cc
from numpy import linspace
from scipy.stats.kde import gaussian_kde

from bokeh.io import output_file, show
from bokeh.models import ColumnDataSource, FixedTicker, PrintfTickFormatter
from bokeh.plotting import figure
from bokeh.sampledata.perceptions import probly

output_file("ridgeplot.html")

def ridge(category, data, scale=20):
    return list(zip([category]*len(data), scale*data))

cats = list(reversed(probly.keys()))

palette = [cc.rainbow[i*15] for i in range(17)]

x = linspace(-20,110, 500)

source = ColumnDataSource(data=dict(x=x))

p = figure(y_range=cats, plot_width=700, x_range=(-5, 105), toolbar_location=None)

for i, cat in enumerate(reversed(cats)):
    pdf = gaussian_kde(probly[cat])
    y = ridge(cat, pdf(x))
    source.add(y, cat)
    p.patch('x', cat, color=palette[i], alpha=0.6, line_color="black", source=source)

p.outline_line_color = None
p.background_fill_color = "#efefef"

p.xaxis.ticker = FixedTicker(ticks=list(range(0, 101, 10)))
p.xaxis.formatter = PrintfTickFormatter(format="%d%%")

p.ygrid.grid_line_color = None
p.xgrid.grid_line_color = "#dddddd"
p.xgrid.ticker = p.xaxis[0].ticker

p.axis.minor_tick_line_color = None
p.axis.major_tick_line_color = None
p.axis.axis_line_color = None

p.y_range.range_padding = 0.12

show(p)
```

# Lynda/LinkedIn Learning Stuff

### Videos

https://www.linkedin.com/learning/pandas-essential-training/using-pandas

https://www.linkedin.com/learning/python-data-analysis-2015/pandas-overview

https://www.linkedin.com/learning/python-data-analysis-2015/dataframes-in-pandas

https://www.linkedin.com/learning/python-data-analysis-2015/series-in-pandas

https://www.linkedin.com/learning/python-data-analysis-2015/using-multilevel-indices

https://www.linkedin.com/learning/python-data-analysis-2015/aggregation

https://www.linkedin.com/learning/data-science-foundations-python-scientific-stack/pandas-overview

https://www.linkedin.com/learning/data-science-foundations-python-scientific-stack/use-geo-data-with-shapely

https://www.linkedin.com/learning/python-for-data-science-tips-tricks-techniques/aggregate-data-with-pandas

https://www.linkedin.com/learning/python-for-data-science-tips-tricks-techniques/aggregate-data-with-pandas

https://www.linkedin.com/learning/python-for-data-science-essential-training/group-and-aggregate-data

https://www.linkedin.com/learning/python-statistics-essential-training/data-cleaning

https://www.linkedin.com/learning/machine-learning-and-ai-foundations-recommendations/introduction-to-numpy-scipy-and-pandas

### Courses

https://www.linkedin.com/learning/programming-foundations-fundamentals-2011

https://www.linkedin.com/learning/learning-the-python-3-standard-library

https://www.linkedin.com/learning/learning-python-generators

https://www.linkedin.com/learning/python-data-analysis-2015

https://www.linkedin.com/learning/numpy-data-science-essential-training

https://www.linkedin.com/learning/python-for-data-science-essential-training

https://www.linkedin.com/learning/python-for-data-science-tips-tricks-techniques

https://www.linkedin.com/learning/pandas-for-data-science