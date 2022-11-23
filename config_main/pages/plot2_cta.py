#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Oct 23, 2022

@author: Disha
"""
from sqlalchemy import create_engine
import pymysql
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objs as go
from plotly.offline import plot
import numpy as np
import csv
import pandas as pd
import sqlalchemy

import dash
import dash_html_components as html
import dash_core_components as dcc
pd.set_option('precision',10)



def cumulative_cta():
    db_connection_str = 'mysql+pymysql://admin:railtec123@railtec-db.cwguuce51yor.us-east-1.rds.amazonaws.com/db_railtec'
    db_connection = create_engine(db_connection_str)
    df = pd.read_sql('SELECT * FROM cta_backup_10222022', con=db_connection)
    V1E = df["V1E_pks"]
    V1W = df["V1W_pks"]
    speed = df["Speed"]
    

    fig = make_subplots(
        rows=2,cols=2,
        subplot_titles=("V1E Peaks", "V1W Peaks", "Speed"))

    fig.add_trace(go.Histogram(
        x=V1E,
        histfunc = "count",
        #histnorm = 'density',
        name='V1E', # name used in legend and hover labels
        marker_color='rgba(36, 231, 128)',
        opacity=1.00,
        xbins=dict( # bins used for histogram
        size=0.5,
        )
        #hover_data={'x':':.2f'},

        ),
    row=1,col=1)
    fig.add_trace(go.Histogram(
        x=V1W,
        histfunc = "count",
        name='V1W', # name used in legend and hover labels
        marker_color='rgba(255, 153, 0)',
        opacity=0.50,
        xbins=dict( # bins used for histogram
        start=0,
        size=0.5,
        )
        ),
    row=1,col=2)


    fig.add_trace(go.Histogram(
        x=speed,
        histfunc = "count",
        name='Speed', # name used in legend and hover labels
        marker_color='rgba(0,0,255)',
        opacity=0.75,
        xbins=dict( # bins used for histogram
        start=0,
        size=0.5,
        )
        ),
    row=2,col=1)

    fig.update_xaxes(title_text = "Wheel Load (Kips)", row=1,col=1)
    fig.update_xaxes(title_text="Wheel Load (Kips)", row=1,col=2)
    fig.update_xaxes(title_text="Speed (MPH)", row=2,col=1)
    fig.update_yaxes(title_text="Frequency",row=1,col=1)
    fig.update_yaxes(title_text="Frequency",row=1,col=2)
    fig.update_yaxes(title_text="Frequency",row=2,col=1)

    fig.update_layout(
        title_text='Wheel Loads', # title of plot
        bargap=0.05, # gap between bars of adjacent location coordinates
        bargroupgap=0, # gap between bars of the same location coordinates
        width = 1000,
        height = 700,
         
    )
    fig.show()
    plot_div = plot(fig, output_type='div', include_plotlyjs=False)
    
    return plot_div
    



