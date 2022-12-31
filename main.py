# Import Library
import numpy as np
import pandas as pd
from bokeh.io import curdoc
from bokeh.layouts import row, column
from bokeh.models import ColumnDataSource, RangeTool, RadioButtonGroup
from bokeh.models.widgets import TextInput, Select
from bokeh.plotting import figure

# Inisialisasi
df = pd.read_csv('covid_data.csv')
df['Date'] = pd.to_datetime(df['Date'])
df_grouped = df.groupby([pd.PeriodIndex(df['Date'], freq='M'), df['Province']]).sum()
dates = [x[0].to_timestamp() for x in df_grouped.index.tolist()]
dates = sorted(set(dates))
dates = np.array(dates, dtype=np.datetime64)
chosen_case = 'Daily_Case'

data = df_grouped[df_grouped.index.isin(['ACEH'], level='Province')]
data2 = df_grouped[df_grouped.index.isin(['DKI JAKARTA'], level='Province')]
source = ColumnDataSource(data=dict(date=dates, freq=data[chosen_case]))
source2 = ColumnDataSource(data=dict(date=dates, freq=data2[chosen_case]))

# options

sumatera_options = [ 'ACEH', 'SUMATERA UTARA', 'KEPULAUAN RIAU', 'SUMATERA BARAT', 'JAMBI', 'SUMATERA SELATAN', 'BENGKULU', 'LAMPUNG', 'KEPULAUAN BANGKA BELITUNG', 'RIAU']
jawa_options = [ 'DKI JAKARTA', 'BANTEN', 'JAWA BARAT', 'JAWA TENGAH', 'JAWA TIMUR', 'DAERAH ISTIMEWA YOGYAKARTA', 'BALI', 'NUSA TENGGARA BARAT', 'NUSA TENGGARA TIMUR']
kalimantan_options = ['KALIMANTAN BARAT', 'KALIMANTAN TIMUR', 'KALIMANTAN TENGAH', 'KALIMANTAN SELATAN', 'KALIMANTAN UTARA']
sulawesi_options = [ 'SULAWESI UTARA', 'GORONTALO', 'SULAWESI TENGAH', 'SULAWESI BARAT', 'SULAWESI SELATAN', 'SULAWESI TENGGARA']
papua_options = [ 'MALUKU UTARA', 'MALUKU', 'PAPUA','PAPUA BARAT']

pulau_options = ['Sumatera', 'Jawa', 'Kalimantan', 'Sulawesi', 'Papua']

case_options = ['Daily Case', 'Daily Death', 'Daily Recovered']

# widgets
title = TextInput(title='Judul Plot', value='')

pulau1 = Select(title='Pulau 1', value='Sumatera', options=pulau_options)
provinsi1 = Select(title='Provinsi 1', value='ACEH', options=sumatera_options)

pulau2 = Select(title='Pulau 2', value='Jawa', options=pulau_options)
provinsi2 = Select(title='Provinsi 2', value='DKI JAKARTA', options=jawa_options)

case = RadioButtonGroup(labels=case_options, active=0)

# plot
p = figure(title="Covid Figure", height=600, width=800, tools="reset,save",
            x_axis_type="datetime", x_axis_location="above", 
            x_range=(dates[0], dates[len(dates)-1]))

l1 = p.line('date', 'freq', source=source, legend_label=provinsi1.value, color='red')

p.line('date', 'freq', source=source2, legend_label=provinsi2.value, color='blue')
p.yaxis.axis_label = 'Frequency'

select = figure(title="Adjust the range here",
                height=130, width=800, y_range=p.y_range,
                x_axis_type="datetime", y_axis_type=None,
                tools="reset,save", toolbar_location=None, background_fill_color="#efefef")

range_tool = RangeTool(x_range=p.x_range)
range_tool.overlay.fill_color = "navy"
range_tool.overlay.fill_alpha = 0.2

select.line('date', 'freq', source=source, color='red')
select.line('date', 'freq', source=source2, color='blue')
select.ygrid.grid_line_color = None
select.add_tools(range_tool)
select.toolbar.active_multi = range_tool

def update_title(attr, old, new):
    p.title.text = title.value

def update_pulau_and_provinsi(attr, old, new) :
    if pulau1.value == 'Sumatera':
        provinsi1.options = sumatera_options
        provinsi1.value = 'ACEH'
    elif pulau1.value == 'Jawa':
        provinsi1.options = jawa_options
        provinsi1.value = 'DKI JAKARTA'
    elif pulau1.value == 'Sulawesi':
        provinsi1.options = sulawesi_options 
        provinsi1.value = 'SULAWESI UTARA'
    elif pulau1.value == 'Kalimantan':
        provinsi1.value = 'KALIMANTAN BARAT'
        provinsi1.options = kalimantan_options
    elif pulau1.value == 'Papua':
        provinsi1.options = papua_options
        provinsi1.value = 'MALUKU UTARA'

    if pulau2.value == 'Sumatera':
        provinsi2.options = sumatera_options
        provinsi2.value = 'ACEH'
    elif pulau2.value == 'Jawa':
        provinsi2.options = jawa_options
        provinsi2.value = 'DKI JAKARTA'
    elif pulau2.value == 'Sulawesi':
        provinsi2.options = sulawesi_options 
        provinsi2.value = 'SULAWESI UTARA'
    elif pulau2.value == 'Kalimantan':
        provinsi2.value = 'KALIMANTAN BARAT'
        provinsi2.options = kalimantan_options
    elif pulau2.value == 'Papua':
        provinsi2.options = papua_options
        provinsi2.value = 'MALUKU UTARA'

    data = df_grouped[df_grouped.index.isin([provinsi1.value], level='Province')]
    data2 = df_grouped[df_grouped.index.isin([provinsi2.value], level='Province')]

    source.data = dict(date=dates, freq=data[chosen_case])
    source2.data = dict(date=dates, freq=data2[chosen_case])

    p.legend.items = []

    p.line('date', 'freq', source=source, legend_label=provinsi1.value, color='red')
    p.line('date', 'freq', source=source2, legend_label=provinsi2.value, color='blue')


def update_provinsi(attr, old, new):
    data = df_grouped[df_grouped.index.isin([provinsi1.value], level='Province')]
    data2 = df_grouped[df_grouped.index.isin([provinsi2.value], level='Province')]

    source.data = dict(date=dates, freq=data[chosen_case])
    source2.data = dict(date=dates, freq=data2[chosen_case])

    p.legend.items = []

    p.line('date', 'freq', source=source, legend_label=provinsi1.value, color='red')
    p.line('date', 'freq', source=source2, legend_label=provinsi2.value, color='blue')

def update_case(attr, old, new):
    global chosen_case
    if case.active == 0:
        chosen_case = 'Daily_Case'
    elif case.active == 1:
        chosen_case = 'Daily_Death'
    elif case.active == 2:
        chosen_case = 'Daily_Recovered'
    print(chosen_case)
    source.data = dict(date=dates, freq=data[chosen_case])
    source2.data = dict(date=dates, freq=data2[chosen_case])

    p.legend.items = []

    p.line('date', 'freq', source=source, legend_label=provinsi1.value, color='red')
    p.line('date', 'freq', source=source2, legend_label=provinsi2.value, color='blue')

title.on_change('value', update_title)
pulau1.on_change('value', update_pulau_and_provinsi)
pulau2.on_change('value', update_pulau_and_provinsi)
provinsi1.on_change('value', update_provinsi)
provinsi2.on_change('value', update_provinsi)
case.on_change('active', update_case)

# add to document
inputs = column(title, row(pulau1, provinsi1), row(pulau2, provinsi2), case)
curdoc().add_root(row(column(p, select), inputs))
curdoc().title = 'Final Project - Kelompok 1'
curdoc().theme = 'caliber'