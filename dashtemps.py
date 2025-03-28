#!/usr/bin/env python3
# -*- coding: utf-8 -*-

CODENAME="dashtemps.py"
__doc__='''
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
 {CODENAME}
 @author: Daniel A. Collins 

 boot up this dashboard python {CODENAME}
 then open browser at https://127.0.0.1:8051 

## @last:   2025-03-28-1048t 

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
'''
__version__='''
@init:   2025-03-05-1436t
@last:   2025-03-24-1025t
'''
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

DEF = CFG[' '] ; ## example
MAIN_PATH = CFG['MAIN_PATH']; ## MAIN_PATH = r'/Users/dac/qlab/testing/'; 
EXE_PATH  = CFG['EXE_PATH'] ; ## r'/Users/dac/qlab/metash/'
VERB      = CFG['VERB'] ; 
REC_LIMIT = CFG['REC_LIMIT'] ;
###############################################################################

# %% DICTIONARY LISTS FOR SIGNALS
SIGNAL_DICT={
   0:  'K' , 
   1:  'TIME' , 
   2:  'aoss-0' , 
   3:  'cpu-0-0' , 
   4:  'cpu-0-1' , 
   5:  'cpu-0-2' , 
   6:  'cpu-0-3' , 
   7:  'gpuss-0' , 
   8:  'gpuss-1' , 
   9:  'nspss-0' , 
   10: 'nspss-1' , 
   11: 'nspss-2' , 
   12: 'video' , 
   13: 'ddr' , 
   14: 'camera-0' , 
   15: 'camera-1' , 
   16: 'mdmss-0' , 
   17: 'pm8150_tz' , 
   18: 'therm-soc-usr' , 
   19: 'skin-sensor' , 
   20: 'skin-sensor-o' , 
   21: 'therm-quiet-usr' , 
   22: 'therm-rf-usr' , 
   23: 'therm-in-temp-usr' ,
}   
SIGNAL_LIST=[
    'aoss-0' , 
    'cpu-0-0' , 
    'cpu-0-1' , 
    'cpu-0-2' , 
    'cpu-0-3' , 
    'gpuss-0' , 
    'gpuss-1' , 
    'nspss-0' , 
    'nspss-1' , 
    'nspss-2' , 
    'video' , 
    'ddr' , 
    'camera-0' , 
    'camera-1' , 
    'mdmss-0' , 
    'pm8150_tz' , 
    'therm-soc-usr' , 
    'skin-sensor' , 
    'skin-sensor-o' , 
    'therm-quiet-usr' , 
    'therm-rf-usr' , 
    'therm-in-temp-usr' ,
]

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
    
# Import required libraries
import pandas as pd;
import dash;
from   dash import dcc;
#from dash import dbc 
from   dash import html;
from   dash.dependencies import Input, Output 
import plotly.graph_objects as go;
import plotly.express as px;
from   dash import ctx, callback

##############################
## Local class modules
#import post_temps as ptt ;
import lib_temps as ptt ;

######################################################################
# %% Dashboard 
# Create a dash application
from dash import Dash, dcc, html, Input, Output, callback, State

app = dash.Dash(__name__, 
                # paramters calling cssfile=....something.css,
                # external_stylesheets=[ ],
                
                suppress_callback_exceptions=True,
);

'''
Loading CSS Files
For the CSS to work as expected, the stylesheets need to be added in the correct order. 
However, Dash loads the stylesheets in a certain way. Here's the order:
1. Files included as external stylesheets in the app constructor 
        app=Dash(__name__, external_stylesheets=[])
2. .css files in the /assets folder, in alphanumerical order by filename
3. The grid's stylesheets when you import dash_ag_grid
It's important to keep this in mind when modifying or creating your own themes 
for dash-ag-grid. For more information, on adding .css and .js files with Dash, 
see Adding CSS & JS.

https://dash.plotly.com/dash-ag-grid/styling-themes
'''

###############################################################################
# %% searching dir    


###############################################################################

# %% running monitortemp
## %% make newtestdir
## %% make newtestdir
def newtest(mainpath = MAIN_PATH, 
            prefix   = CFG['test-prefix'],
            splitter = '-' ,
    ):
    #mainpath = MAIN_PATH; # r'/Users/dac/qlab/testing/' ; 
    import re;
    
    nameoftests = ptt.searchdir ( mainpath );
    lasttestdir = nameoftests[-1];
    # print( lasttestdir) ;
    f  = lasttestdir.split( splitter );
    
    f0 = lasttestdir.split( splitter )[0] ;
    f1 = lasttestdir.split( splitter )[1] ;
    
    # if len(f)>1: f1 = f[1];
    # else: f1 = f[0] ;
    f1 = f[0] ;
    if len(f)>1: f1 = f[1];
    ##w = int( 1 + float( lasttestdir.lstrip( dirpattern ) ));
    
    w = int( 1 + float( f1 ));
    
    nexttestdir = \
        str( prefix ) + str( splitter) +\
        '0'*(w<10000) +'0'*(w<1000) +'0'*(w<100) +'0'*(w<10) +\
        str(w);
    print( f' Last testdir {lasttestdir}.  ' , end='\t' ) ; 
    print( f' Making now testdir {nexttestdir}' ) ; 
    nexttestdir_full = mainpath + os.sep + nexttestdir ;
    os.mkdir( mainpath + os.sep + nexttestdir );
    
    return nexttestdir, nexttestdir_full;

def newtest__(mainpath = MAIN_PATH, 
            dirpattern = CFG['test-prefix'],
            newpattern = CFG['new-prefix'],
    ):
    #mainpath = MAIN_PATH; # r'/Users/dac/qlab/testing/' ; 
    import re;
    
#if 1:
    nameoftests = ptt.searchdir ( mainpath );
    lasttestdir = nameoftests[-1];
    # print( lasttestdir) ;    
    w = int( 1 + float( lasttestdir.lstrip( dirpattern ) ));
    nexttestdir = \
        str( newpattern ) +\
        '0'*(w<10000) +'0'*(w<1000) +'0'*(w<100) +'0'*(w<10) +\
        str(w);
    print( f' Last testdir {lasttestdir}.  ' , end='\t' ) ; 
    print( f' Making now testdir {nexttestdir}' ) ; 
    nexttestdir_full = mainpath + os.sep + nexttestdir ;
    os.mkdir( mainpath + os.sep + nexttestdir );
    
    return nexttestdir, nexttestdir_full;
#if 0: ## testing
#    n,f = newtest( r'/Users/dac/qlab/testing/' ) ;

####~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
## %%
def check_sh():
    t = os.system("sh -c echo ' ' ");
    if t==0: shtype="bsh";
    else:    shtype="ps1";
    return shtype;
    
def cmd_monitortemp(
        rec_path, 
        exe_path, 
        shtype=CFG['init_shell'], # "bsh", 
        proof=1, 
        maxlimit=10, 
    ):
    #exe_path=CFG['EXE_PATH']
#    shtype="bsh";
#    shtype="ps1";
    shtype=CFG['init_shell'];
    exe_path = r'/Users/dac/qlab/metash/';
    if rec_path == None:
       rec_path = str( MAIN_PATH + os.sep + ptt.searchdir( MAIN_PATH )[-1] ) ;
    if shtype==None:
        shtype = check_sh();
    if shtype=="bsh":
        code="monitortemp.sh"
        cmd = f'''
 echo "running with Bash {code}" 
 sh {exe_path}/{code} -rec {rec_path} -max {maxlimit} -proof {proof} &
    '''
    else:
        code="monitortemp.ps1"
        options=f'''-CTRLIMIT {maxlimit} -PROOFING {proof} -REC_PATH {rec_path} ''' ;
        powershell = "/usr/local/microsoft/powershell/7/pwsh" ;
        cmd = f'''
 {powershell} -Command {exe_path}/{code} {options} 
 ''';
    #proof = 1 ; ## dont run adb commands 
    #maxlimit = 5; ## for proofing
    print( f'executing: \n {cmd}')
    os.system( cmd );
 
####~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
## %% stop_recording
def stop_recording(  ):
    #mainpath = MAIN_PATH; # r'/Users/dac/qlab/testing/' ; 
    rec_path = str( MAIN_PATH + os.sep + ptt.searchdir( MAIN_PATH )[-1] ) 
    stop_path = str( rec_path + os.sep + "STOP" );
    print( "now stopping !" )
    cmd = f'''
    printf "now stopping !"; 
    echo "" > {stop_path}  
    ''';    
    print( f'executing: \n {cmd}') ;
    os.system( cmd );

####~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def clear_stop_recording( shtype="bsh" ):
    #mainpath = MAIN_PATH; # r'/Users/dac/qlab/testing/' ; 
    rec_path = str( MAIN_PATH + os.sep + ptt.searchdir( MAIN_PATH )[-1] ) 
    stop_path = str( rec_path + os.sep + "STOP" );
    print( "Clearing STOP " );
    if shtype==None:
        shtype = check_sh();
    if shtype=="bsh":
        cmd = f''' rm -fv {stop_path} ''';
    else: 
        powershell = "/usr/local/microsoft/powershell/7/pwsh" ;
        cmd = f''' {powershell} -Command Remove-Item -Force {stop_path} ''';
    print( f'executing: \n {cmd}') ;
    os.system( cmd );


def get_dir( ) :
    
    return dcc.Dropdown(
            id='select_dir',
            #options=get_testdir,            
            options = ptt.searchdir( MAIN_PATH ) ,
            ## options = get_testdir, #ptt.searchdir( MAIN_PATH ) ,
            value =  ptt.searchdir( MAIN_PATH )[-1],
            persistence = True, 
            style={'font-size': SIZE['drop'],
                   'padding'  : 3,
                   'textAlign': 'left',
                   },
        )

######################################################################
## %%
######################################################################
# %% SETTING PATHS 

if VERB[3]: ## Testing the response for ptt.searchdir ...
    get_testdir = ptt.searchdir( MAIN_PATH );
    get_lasttest = get_testdir[-1] ;
    print(f'\n Test Directories found in {MAIN_PATH} are ');
    for e in get_testdir: print( f" {e}, ", end='' );
    print(f'\n LAST Test Directory is {get_lasttest}''');
      
##--> data, inppfile = ptt.get_dfread( inppath ) <---#

######################################################################
# %% Dashboard: styples and layouts 
# 



# data =  pd.read_csv(
#         inppfile ,
# );
STYLE={  
    'Div' : {'display':     'flex'},
    'Div2': {'font-size':   80} ,
    'Wid' : {'width':'      65%'},
    'eng' : {'width':'40%', 'height':'30%'},
};
# %% Dashboard Headers
HTX = {
       
    0: html.H1(
        str( 10*' '),
        style={ 'textAlign': 'left', 
                'color': '#d69224',
                'font-size': 30 }
    ),
    1: html.H1(
        ' REGISTER TEMPERATURES ',
        style={ #'textAlign': 'center', 
                'textAlign': 'left', 
                'color': '#503D36',
                'font-size': 36 }
    ),
    11: html.H1(
        'Select Test:',
        style={ 'textAlign': 'left', 
                'color': '#24d639',
                'font-size': 18 }
    ),
    21: html.H1(
        'Select Signal:',
        style={ 'textAlign': 'left', 
                'color': '#24d639',
                'font-size': 18 }
    ),

    51: html.H1(
        ' Max & Min of all Temperatures ',
        style={ 'textAlign': 'left', 
                'color': '#111111',
                'font-size': 20 }
    ),
 

}
# %% Dashboard  INPUTS

# SIZE['btn']
INP = {

    'sel_signal': 
        dcc.Dropdown(
            id='sel_signal',
            options=SIGNAL_LIST,
            value='cpu-0-0',  #DROP[0][1],
            #placeholder='cpu-0-0', #DROP[0][2],
            style={'font-size': SIZE['drop'],
                   'padding'  : 3,
                   'textAlign': 'left',
                   },
    ),
    'sel_dir': 
        dcc.Dropdown(
            id='select_dir',
            #options=get_testdir,            
            options = ptt.searchdir( MAIN_PATH ) ,
            ## options = get_testdir, #searchdir( MAIN_PATH ) ,
            value =  ptt.searchdir( MAIN_PATH )[-1],
            persistence = True, 
            style={'font-size': SIZE['drop'],
                   'padding'  : 3,
                   'textAlign': 'left',
                   },
    ),
    ## checkbox input to select last-file or all-files in testdir
    #RadioSelection = \
    #31: 
    'btn_refresh_dir' :
           html.Button(
                "Refresh List dir",
                id='refresh_list',
                n_clicks=0,  
                style={'font-size': SIZE['btn'],
                       'padding'  : 15,
                       'textAlign': 'center',
                       },
    ),     
    'sel_dir_refreshed': 
        dcc.Dropdown(
            id='select_dir_refreshed',
            options = ptt.searchdir( MAIN_PATH ) ,
            value  =  ptt.searchdir( MAIN_PATH )[-1],
            style={'fontsize': SIZE['drop'],},
    ),
    'radio_osshell' : 
            dcc.RadioItems(
                [
                 'Bash Shell (Mac/Linux)',
                 'Powershell (Winddows)' , 
                 ], 
                #'Bash Shell (Mac/Linux)', 
                CFG['def_osshell'],
                id='sel_osshell',
                inline=True,
                 style={'fontsize': SIZE['radio'],},
        ),
    'radio_files' : 
        dcc.RadioItems(
            ['Last File Only', 'All Files in Test Dir'], 
            'Last File Only', 
            id='sel_files',
            inline=True,
             style={'fontsize': SIZE['radio'],},
    ),
    #3:
    'checklist_files' : 
        dcc.Checklist(
            options=['Last File Only', 'All Files in Test Dir'], 
            #value='Last File Only', 
            id='sel_files',
            inline=True,
            style={'font-size': 20 },
    ),  
    'btn_newtestdir' :
        html.Button(
             "  New Test  ",
             id='make_newtestdir',
             n_clicks=0,
             style={'font-size': SIZE['btn'],
                    'padding' : 15,
                    'textAlign': 'left',
                    },
             
    ),
    'btn_monitortemp' :
        html.Button(
             "Record Monitor",
             id='rec_monitortemp',
             n_clicks=0,
             style={'font-size': SIZE['btn'],
                    'padding' : 15,
                    'textAlign': 'center',
                    },
             
    ),
    'btn_stopmonitor' :
        html.Button(
             "Stop Monitor",
             id='stop_monitortemp',
             n_clicks=0,
             style={'font-size': SIZE['btn'],
                    'padding' : 15,
                    'textAlign': 'center',
                    },
             
    ),
    'btn_clear_stop' :
        html.Button(
             "Clearing Stop ",
             id='clear_stop',
             n_clicks=0,
             style={'font-size': SIZE['btn'],
                    'padding' : 15,
                    'textAlign': 'center',
                    },
             
    ),

};
    
# INP[1] = INP['sel_dir'] ;
# INP[2] = INP['sel_signal'] ;
# INP[3] = INP['radio_files'] ;
# INP[4] = INP['btn_newtestdir'];
# INP[5] = INP['btn_monitortemp'] ;
# INP[6] = INP['btn_stopmonitor'] ;
# FIG ={
#     1:  dcc.Graph( id='fig-plot1' ),
# ##  2:  dcc.Graph( id='plot2' ), #HTX[3],## not ready yet #

# }

###############################################################################
# %% Layout-Styles


# %% LAYOUT SERVE

def serve_layout():
    
    # def search_dir():
    #     return ptt.searchdir( MAIN_PATH );

    # sel_dir = \
    #     dcc.Dropdown(
    #         id='select_dir',
    #         #options=get_testdir,            
    #         options = searchdir( MAIN_PATH ) ,
    #         ## options = get_testdir, #searchdir( MAIN_PATH ) ,
    #         value =  searchdir( MAIN_PATH )[-1],
    #         persistence = True, 
    # ), f
    MENU =\
      html.Div([
        html.Div([

            INP['btn_newtestdir'], ##  INP[4] ,
            #html.Div( [""], 
            #    style={'width': '45px'}),
            ## record_temps
            INP['btn_monitortemp'], ##  INP[5], 
            
            ## stop recording
            INP['btn_stopmonitor'], ##  INP[6],

            ## stop recording
            INP['btn_clear_stop'],
            
            ## select_dir
                HTX[11] ,                
                # dcc.Dropdown(
                #     id='select_dir',
                #     options = ptt.searchdir( MAIN_PATH ) ,
                #     value  =  ptt.searchdir( MAIN_PATH )[-1],
                #     persistence = False, 
                # ),
                
                INP['btn_refresh_dir'],
                dcc.Dropdown(
                    id='list-dir',
                    options = []    ,
                    value  =  None  ,
                    persistence = False, 
                ),
                
                
                dcc.Store('store-dir', 
                          storage_type='session',
                          data='list'
                ),
                dcc.Store('store-lastdir', 
                          storage_type='session',
                          data='string'
                ),
                
#                 html.Div(id='container-dirs',
# #                         storage_type='session',
# #                         data='list',
#                          className='chart-grid' ,
#                              #'children' 
#                 ),

                # dcc.Store('this-dir'),
            
            ## select all-files or last file
                # INP['radio_files'], ## INP[3] ,
            ## select_signal
                HTX[21] , INP['sel_signal'], ## INP[2]  ,        

                

            ],style={
              'textAlign':'left',  
              'width':'40%',
              'height':'%40%',
              }            
        ),
        ]
    )
    import dash_bootstrap_components as dbc
    MENU_1 = html.Div(
      [ 
        dbc.Row(
          [
            dbc.Col(
                html.Div('btn_newtestdir',
                         width={'size':6, 'offset':3},
                )
            ),                
            dbc.Col(
                html.Div('btn_monitortemp',
                         width={'size':6, 'offset':3},
                )
            ),
            dbc.Col(
                html.Div('btn_stopmonitor',
                         width={'size':6, 'offset':3},
                )
            ),
            dbc.Col(
                html.Div('btn_clear_stop',
                         width={'size':6, 'offset':3},
                )
            ),
          ],
          align='start',
          
        )
      ]  
    )
        
        
    MENU_CFG= \
        html.div(
            
            
            INP['radio_osshell'],  ## 
            dcc.Store('set_shell', storage_type='session', data='string'),
        )
                
    return html.Div(children=[ 
    
        html.Table([
            HTX[1], 
            html.Table(
              html.Td(
                [  
    #             html.Div(), ## blank,
                 MENU,
     #            html.Div(), ## blank,
                ],
                style={
                    'width'  : '1000px' ,
                    #'height' : '1000px' ,
                }
              )
            ),
            
            dcc.Graph( id='fig-plot1' ), 
            
            html.Div(
                id='container-button',
                style={'height':'35px', 'font-size': 25},
                
            ),            
            
            html.Div(
                id='output-container' , 
                className='chart-grid' ,
                style={'display': 'flex'}
            ),    
            
        ],style={
            'width'  : '1000px' ,
            #'height' : '1000px' ,
        }
        ), ## </table>
            
    ]) ## </DivChildren>

## app.layout = app_layout304 ;
app.layout = serve_layout ;

######################################################################
@app.callback( 
  Output( 'set_shell',   'data'   ),
  Input(  'sel_osshell', 'value'  ),

)
def update_shell(
        which_osshell,
):
    if which_osshell=='Powershell (Winddows)':
        set_shell = 'ps1';
    if which_osshell=='Bash Shell (Mac/Linux)':
        set_shell = 'bsh';
   #R =dcc.Store('set_shell', storage_type='session', data='string')        
    R = set_shell ; 
    return [ R ];

######################################################################
# %% callback - buttons
@app.callback( 
 [
    Output( 'container-button', 'children' ),
    # Output( 'container-path', 'value' ),
 ],
 [
    Input(component_id='make_newtestdir',  component_property='n_clicks'),
    Input(component_id='rec_monitortemp',  component_property='n_clicks'),
    Input(component_id='stop_monitortemp', component_property='n_clicks'),
    Input(component_id='clear_stop',       component_property='n_clicks'),
    Input( 'set_shell',   'data'  ),
 ]
)
 
######################################################################
def button_menu(
        btn_make_newtestdir,
        btn_rec_monitortemp,
        btn_stop_monitor,  
        btn_clear_stop,
        set_shell,
):
    msg = "";
    rec_path = str( MAIN_PATH + os.sep + ptt.searchdir( MAIN_PATH )[-1] ) ;
    if 'make_newtestdir' == ctx.triggered_id :
        nexttestdir, nexttestdir_full = newtest( mainpath = MAIN_PATH );
        msg = ( f' making new test dir .... {nexttestdir} ');
        print ( msg );

    if 'rec_monitortemp' == ctx.triggered_id :
        msg = ( f' Recording Monitortemp ');
        print ( msg );
        ## cmd_monitortemp()
        rec_path = str( MAIN_PATH + os.sep + ptt.searchdir( MAIN_PATH )[-1] ) 
        cmd_monitortemp( rec_path, 
                         exe_path=EXE_PATH, 
                         maxlimit=REC_LIMIT,
                         #shtype="bsh",
                         shtype=set_shell,
                         proof=CFG['proofing'],  ## doesn't do adb 
        );

    if 'stop_monitortemp' == ctx.triggered_id :
        msg = ( f' Stop recording Monitortemp ');
        print ( msg );
        ## cmd_monitortemp()
        rec_path = str( MAIN_PATH + os.sep + ptt.searchdir( MAIN_PATH )[-1] ) 
        stop_recording( ## rec_path
         );
    if 'clear_stop' == ctx.triggered_id :
        msg = ( f' Clearing Stop ');
        print ( msg );
        ## cmd_monitortemp()
        rec_path = str( MAIN_PATH + os.sep + ptt.searchdir( MAIN_PATH )[-1] ) 
        clear_stop_recording( 
            # shtype="bsh",
              shtype=set_shell,
              ## rec_path
         );
    
    # return [ html.Div(msg). nexttestdir_full  ] ;
    return [ html.Div(msg)                    ] ;

# ######################################################################
if 0:
    pass
# %% dropdown
    dcc.Dropdown(
        id='select_dir',
        options = ptt.searchdir( MAIN_PATH ) ,
        value  =  ptt.searchdir( MAIN_PATH )[-1],
        persistence = True, 
        style={'font-size': SIZE['drop'],
               'padding'  : 3,
               'textAlign': 'left',
               },
        )

# ######################################################################
# %% callback - sel_dir

# # # ######################################################################

# # ######################################################################
# # %% callback - sel_dir
# @app.callback( 
#     Output( 'drop_sel_dir', 'children' ),
#     # Input(component_id='select_dir', component_property='value'),
#     Input(  'refresh_list', component_property='n_clicks'),
# )

# def make_sel_dir(   ):
#     HTML_DROP = dcc.Dropdown(
#         id='select_dir',
#         options = ptt.searchdir( MAIN_PATH ) ,
#         value =  ptt.searchdir( MAIN_PATH )[-1],
#         persistence = True, 
#         style={'font-size': SIZE['drop'],
#                'padding'  : 3,
#                'textAlign': 'left',
#                },
#     )
#     return HTML_DROP  
        
# ######################################################################
# %% callback - update_dir --> html_drop 
@app.callback( 
  [ 
    Output( 'list-dir', 'options' ),
    Output( 'list-dir', 'value' )
#    Output( 'last-dir', 'value' )
  ],
  [
    Input( 'refresh_list', 'n_clicks'),
  ]
)

def refresh_list_dir( btn_refresh_dir ):
    # HTML_DROP= dcc.Dropdown(
    #         id='select_dir',
    #         options =  ptt.searchdir( MAIN_PATH ) ,
    #         value   =  ptt.searchdir( MAIN_PATH )[-1],
    #         persistence = True, 
    #     )
    # # if 'refresh_list' == ctx.triggered_id :
    #     return HTML_DROP
    # else: 
    #     return no.update ;
    return [ ptt.searchdir( MAIN_PATH ) ,
             ptt.searchdir( MAIN_PATH )[-1] 
           ]
    #HTML_DROP

# # ######################################################################


# ######################################################################


######################################################################
# %% callback: update_graph: sel_signal --> fig-plot
@app.callback( 
 [ 
    Output( 'fig-plot1', 'figure'),
 #   Output( 'output-container', 'children' ),
 ],
 [
#    Input( 'container-dirs', component_property='children'),
    # Input( 'select_dir',     component_property='value'),
    # Input( 'store-lastdir',  'data' ),
    Input( 'list-dir', 'value'  ) ,
    Input( 'sel_signal', 'value') ,
#   Input( 'sel_files',  'value') ,
 ]
)
 
# %% get_graph
######################################################################
def update_graph( 
#        list_dir, 
        sel_dir,
#        last_dir,
        select_signal, 
#        sel_files,
    ):  
    msg = "";
    # if btn_make_newtestdir == ctx.triggered_id :
    #     msg = ( f' make_newtestdir ');
    #     print ( msg );
    last_file_opt = True ; #default:True
    all_files_opt = False; #default:False
    
    # if sel_files == 'Last File Only':
    #     last_file_opt = True ; #default:True
    #     all_files_opt = False; #default:False
    # if sel_files == 'All Files in Test Dir':
    #     last_file_opt = False ;
    #     all_files_opt = True ;
    
    
    inppath = MAIN_PATH + os.sep + sel_dir ; 
    msg = f''' reading inside directory {sel_dir} ''';
    #if VERB[1]: 
    print( msg ) ;

    inpfile = ptt.getFiles(inppath,
                 #def: LASTFILE=True,
                 LASTFILE=last_file_opt, 
                 #def: ALLFILES=False,
                 ALLFILES=all_files_opt,
                 KW_BEG='watch_temp', 
                 KW_END='csv', 
                 SHOW=False ,
                 # SHOW=True,
    );
    msg = f''' reading from file {inpfile} ''';
    if VERB[1]: print( msg ) ;
    data, _ = ptt.get_dfread( 
        inpfile 
        #inppath, SHOWFILES=True, SHOW=False
    ) ;
    
    dfcor = ptt.build_dfcor( data, APPLYSMOOTH=False )
    
    #cmp  = compute_info( data, select_signal  ) ;
    
    colsigns  = list(dfcor.columns);colsigns.remove('k');colsigns.remove('time');
    #colsignst = list(dfcor.columns);colsigns.remove('k');
    
    df_max = dfcor[ colsigns ].max( axis=1 );
    df_ave = dfcor[ colsigns ].mean( axis=1 );
    df_min = dfcor[ colsigns ].min( axis=1 );
    
    dfstat = pd.DataFrame( [dfcor['time'], df_max, df_ave, df_min] ) ;
    dfstat = dfstat.T ;
    dfstat.columns = ['time','max','mean','min'];
    #print (dfstat.head );
        
    
    green = '#16a15c' ;
    red   = '#f56642' ;
    blue  = '#008abd' ;  
       
    fig1 = go.Figure();
    fig1.add_trace(go.Scatter( 
        x=dfcor['time'],
        y=dfstat['max'],
        #mode='lines',    
        name='max',
        line_color='#bd230f', # red,
        line_width=2.3,
        #line_dash='5 7 3',
        line_dash='dot',
        opacity=0.7,
    ))
    
    fig1.add_trace(go.Scatter( 
        x=dfcor['time'],
        y=dfstat['min'],
        mode='lines',    
        name='min',
        line_color=blue,
        line_width=1.8,
        line_dash='dot',
        opacity=0.7,
    ))
    
    if 1:
       fig1.add_trace(go.Scatter( 
           x=dfcor['time'] ,     
           y=dfcor['cpu-0-0'],
           line_color='#eb3480' , #'#34e8eb' ,
           line_width=2.5,
           mode='lines',
           name='cpu-0-0',
       ));
    if 1:
       fig1.add_trace(go.Scatter( 
          x=dfcor['time'] ,     
          y=dfcor['skin-sensor'],
          line_color='#eb9e34' ,
          line_width=2.5,
          mode='lines',
          name='skin-sensor',
      ));
    
    if 1:
     #if len( select_signal )>0:
        ss=""
        ss=str('{}\n(selected)'.format( select_signal ) )
        fig1.add_trace(go.Scatter( 
            x=dfcor['time'] ,     
            y=dfcor[select_signal],
            line_color=green,
            line_width=3.6,
            mode='lines',
            name=ss,
            #dash='5 3 2 5',
            #fgopacity=0.7,            
        )); 
    fig1.update_layout(
    xaxis_title=" Time (sec) ",  # Set the x-axis label here
    yaxis_title=" Temperature (℃) ",  
    )
    if len(inpfile) > 0:
        return [ fig1 ] ;
    elif len(inpfile)==0:
#        return dadsh.no_update;
        raise dash.exceptions.PreventUpdate 
#    return [ fig1, html.Div(msg) ]
  
###############################################################################
# %% Run the app
if __name__ == '__main__':
    ## OPTS = get_argparse()
    ## CFG  = read_cfg()
    app.run_server(
        port=8050, 
        host='127.0.0.1', 
        debug=True,
        # suppress_callback_exceptions=True,        
    ) ;
###############################################################################


#%% ERRORS / WARNINGS:
feedback = {
    '2025-03-19T10:50' : '''
    Callback error updating ..fig-plot1.figure..
        TypeError: can only concatenate str (not "dict") to str
    ''',
    
    
    }