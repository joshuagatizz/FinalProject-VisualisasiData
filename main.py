# Import Library yang diperlukan
import pandas as pd
from bokeh.io import curdoc
from bokeh.layouts import row
from bokeh.models import Column, ColumnDataSource
from bokeh.models.widgets import TextInput, Select, CheckboxButtonGroup
from bokeh.plotting import figure

# Inisialisasi
df = pd.read_csv('kendaraan.csv')
x = df['Premi']
y = df['Lama_Berlangganan']
source = ColumnDataSource(data=dict(x=x, y=y))

# Membuat widget
title = TextInput(title="Judul Plot", value='Plot Kendaraan')

umur_options = ["< 1 Tahun", "> 2 Tahun", "1-2 Tahun"]
umur = Select(title="Umur Kendaraan", value="< 1 Tahun", options=umur_options)

axis_options = list(df.columns)[2:]
x_axis = Select(title="X Axis", value="Premi", options=axis_options)
y_axis = Select(title="Y Axis", value="Lama_Berlangganan", options=axis_options)

gender = CheckboxButtonGroup(labels=["Pria", "Wanita"], active=[0,1])

# Membuat plot
plot = figure(sizing_mode="scale_width", title="Plot Kendaraan", tools="crosshair,pan,reset,save,wheel_zoom", x_range=[0, 100], y_range=[0, 60])

plot.dot('x', 'y', source=source, size=30)

plot.xaxis.axis_label = x_axis.value
plot.yaxis.axis_label = y_axis.value

# Membuat callback
def update_title(attrname, old, new):
    plot.title.text = title.value

title.on_change('value', update_title)

def update_data(attrname, old, new):

    plot.xaxis.axis_label = x_axis.value
    plot.yaxis.axis_label = y_axis.value

    df2 = df['Umur_Kendaraan']==umur.value
    x = df2[x_axis.value]
    y = df2[x_axis.value]
    source.data = dict(x=x, y=y)

for data in [x_axis, y_axis, umur]:
    data.on_change('value', update_data)

def update_gender_data(attrname, old, new):
    dct = {0: 'Pria', 1: 'Wanita'}
    mapped_active = [*map(dct.get, gender.active)]
    if len(gender.active) == 0:
        df2 = df['Jenis_Kelamin']=='0'
    elif len(gender.active) == 1:
        df2 = df['Jenis_Kelamin']==mapped_active[0]
    else:
        df2 = df
    x = df2[x_axis.value]
    y = df2[x_axis.value]
    source.data = dict(x=x, y=y)

gender.on_change('active', update_gender_data)

# Menambahkan ke document
inputs = Column(title, x_axis, y_axis, umur, gender)
curdoc().add_root(row(inputs, plot, width=1000))
curdoc().title = "Final Project - Kelompok 1"
curdoc().theme = "dark_minimal"