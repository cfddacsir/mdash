#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 28 11:18:43 2025

@author: dac
"""

###############################################################################
# %% CFG 
SIZE = {
    'btn'   : 15 ,
    'drop'  : 15 ,
    'radio' : 15 ,
}

CFG = {
' ' : 0,
'MAIN_PATH'     : r'/Users/dac/qlab/testing/' ,
'EXE_PATH'      : r'/Users/dac/qlab/metash/'  ,
'VERB'          : [0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ],
'test-prefix'   : 'B' ,
'new-prefix'    : 'B' ,
'REC_LIMIT'     :  61, #  60,
'proofing'      :  1, ## set to 1 if adb is not connected
'def_osshell'   : 'Bash Shell (Mac/Linux)',
'init_shell'    : 'bsh',
};
###############################################################################

################################################################################
# %% IMPORTS 
import warnings;warnings.simplefilter(action='ignore', category=FutureWarning);# Suppress FutureWarning
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#import myfavs as my;
#import danpy as dan;
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# basics
import os;
from   os import listdir;
FSS = os.sep;
from   pathlib import Path;
import re ;
import argparse ;
## import linecach

import numpy as np;
import pandas as pd;
import matplotlib.pyplot as plt;
import matplotlib as mpl;
import seaborn as sns;
from   scipy import stats;
from   scipy.interpolate import interp1d;
from   scipy import interpolate;

# %matplotlib inline # uncomment only in jupyter

##############################
## Local class modules
import lib_temps as  ptt ;
import lib_thdash as dth ;
    
# plotly/dash libraries
import plotly.graph_objects as go;
import plotly.express as px;
import dash;
from   dash import dcc;
from   dash import html;
from   dash import ctx, callback ;
import dash_bootstrap_components as dbc ;
from   dash.dependencies import Input, Output ;
from   dash import Dash, dcc, html, Input, Output, callback, State ;

######################################################################
# stylesheet with the .dbc class to style  dcc, DataTable and AG Grid components with a Bootstrap theme
dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME, dbc_css])


header = html.H4(
    "Device Zone Temperatures", className="bg-primary text-white p-2 mb-2 text-center"
)
SIZE['btn_style'] =\
  {  
    'font-size': 15, #SIZE['btn'],
    'padding' :  15,
    'textAlign': 'center',
  }
MBT={
    'btn_newtestdir' :
        html.Button(
             "  New Test  ",
             id='make_newtestdir',
             n_clicks=0, 
             style=SIZE['btn_style'],
    ),
    'btn_monitortemp' :
        html.Button(
             "Record Monitor",
             id='rec_monitortemp',
             n_clicks=0,
             style=SIZE['btn_style'],
    ),
    'btn_stopmonitor' :
        html.Button(
             "Stop Monitor",
             id='stop_monitortemp',
             n_clicks=0,        
             style=SIZE['btn_style'],
    ),
    'btn_clear_stop' :
        html.Button(
             "Clearing Stop ",
             id='clear_stop',
             n_clicks=0,          
             style=SIZE['btn_style'],
    ),
}
dropdown = html.Div(
    [
        dbc.Label(" Select Dir "),
        dcc.Dropdown(
            options=ptt.searchdir( CFG['MAIN_PATH'] ),
            #["B-00001", "B-00002", "B-00003"],
            #"B-00001",
            value=ptt.searchdir( CFG['MAIN_PATH'] )[-1],
            id="sel-dir",
            clearable=False,
        ),
    ],
    className="mb-4",
)

btabs = dbc.Row(
    [
            dbc.Col(
                html.Div([
#                   'btn_newtestdir',
                     MBT['btn_newtestdir'],
                    ],
#               className='btname p.dotted',
                ),
#              width={'size':6, 'offset':3},
            ),
            html.Span(className="border rounded"),
            
            dbc.Col(
                html.Div([
#                       'btn_monitortemp' ,
                    MBT['btn_monitortemp'],                    
                    ],
                ),
#              width={'size':6, 'offset':3},
            ),
            dbc.Col(
                html.Div([
#                        'btn_stopmonitor',
                     MBT['btn_stopmonitor'],
                    ],
                ),
#              width={'size':6, 'offset':3},
            ),
            dbc.Col(
                html.Div( [
#                        'btn_clear_stop',
                     MBT['btn_clear_stop'],
                    ],      
                ),
#              width={'size':6, 'offset':3},
            ),
    ],
)

controls = dbc.Card(
    [dropdown, #checklist, slider
    ],
    body=True,
)

app.layout = dbc.Container(
    [
        header,
        dbc.Row([
            dbc.Col([ controls, ], 
                    width=4
                ),
            dbc.Col([ btabs,    ],
                    width=3
                ),
        ]),
        dbc.Row([
          html.Div( "something"),
        ],),

    ],
    fluid=True,
    className="dbc dbc-ag-grid",
)


###############################################################################
# %% Run the app

if __name__ == '__main__':
    ## OPTS = get_argparse()
    ## CFG  = read_cfg()
    app.run(
        port=8055, 
        host='127.0.0.1', 
        debug=True,
        # suppress_callback_exceptions=True,        
    ) ;
###############################################################################