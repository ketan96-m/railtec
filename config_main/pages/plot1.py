#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 29 20:23:37 2021

@author: oishee
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



def cumulative_plot():
    db_connection_str = 'mysql+pymysql://admin:railtec123@railtec-db.cwguuce51yor.us-east-1.rds.amazonaws.com/db_railtec'
    db_connection = create_engine(db_connection_str)
    df = pd.read_sql('SELECT * FROM metratr116', con=db_connection)
    
    V1_car = df["V1N_pks"][df["carOrLoc"] == "car" ]
    
    V1_loc = df["V1N_pks"][df["carOrLoc"] == "locomotive"]
    speed = df["Speed"].loc[df["Speed"]>45]
    

    fig = make_subplots(
        rows=2,cols=2,
        subplot_titles=("Vertical Loads for Car", "Vertical Loads for Locomotive", "Speed"))

    fig.add_trace(go.Histogram(
        x=V1_car,
        histfunc = "count",
        #histnorm = 'density',
        name='V1N - Car', # name used in legend and hover labels
        marker_color='rgba(36, 231, 128)',
        opacity=1.00,
        xbins=dict( # bins used for histogram
        size=0.5,
        )
        #hover_data={'x':':.2f'},

        ),
    row=1,col=1)
    fig.add_trace(go.Histogram(
        x=V1_loc,
        histfunc = "count",
        name='V1N - Locomotive', # name used in legend and hover labels
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
    


def lateral_plot():
    db_connection_str = 'mysql+pymysql://admin:railtec123@railtec-db.cwguuce51yor.us-east-1.rds.amazonaws.com/db_railtec'
    db_connection = create_engine(db_connection_str)
    df = pd.read_sql('SELECT * FROM metratr116', con=db_connection)
    L1 = pd.read_sql('SELECT L1N_pks FROM metratr116', con=db_connection)
    L2 = pd.read_sql('SELECT L1S_pks FROM metratr116', con=db_connection)   
    fig = go.Figure()

    df.sort_values(['L1N_pks'], ascending=[False])
    df.sort_values(['L1S_pks'], ascending=[False])
    perc1 = np.linspace(0,100,len(L1)) #creates percentages
    perc2 = np.linspace(0,100,len(L2))
    fig.add_trace(go.Scatter(x=L1, y=perc1, mode='lines', name='Lateral Load 1'))
    fig.add_trace(go.Scatter(x=L2, y=perc2, mode='lines', name='Lateral Load 2'))
    fig.update_layout(title='Lateral Loads', xaxis_title='Peak Lateral Loads (kips)', yaxis_title='Percent Exceeding')

    lat_plot_div = plot(fig, output_type='div', include_plotlyjs=False)
    return lat_plot_div

def vertical_plot():
    db_connection_str = 'mysql+pymysql://admin:railtec123@railtec-db.cwguuce51yor.us-east-1.rds.amazonaws.com/db_railtec'
    db_connection = create_engine(db_connection_str)
    df = pd.read_sql('SELECT * FROM metratr116', con=db_connection)
    V1 = pd.read_sql('SELECT V1N_pks FROM metratr116', con=db_connection)
    V2 = pd.read_sql('SELECT V1S_pks FROM metratr116', con=db_connection)
    fig = go.Figure()

    df.sort_values(['V1N_pks'], ascending=[False])
    df.sort_values(['V1S_pks'], ascending=[False])
    perc1 = np.linspace(0,100,len(V1)) #creates percentages
    perc2 = np.linspace(0,100,len(V2))
    fig.add_trace(go.Scatter(x=V1, y=perc1,
                    mode='lines',
                    name='Vertical Load 1'))
    fig.add_trace(go.Scatter(x=V2, y=perc2,
                    mode='lines',
                    name='Vertical Load 2'))
    fig.update_layout(title='Vertical Loads',
                   xaxis_title='Peak Vertical Loads (kips)',
                   yaxis_title='Percent Exceeding')
    
    vert_plot_div = plot(fig, output_type='div', include_plotlyjs=False)
    return vert_plot_div


