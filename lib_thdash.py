#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###############################################################################
# %% header
__doc__='''
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  post_temps.py
[-figsave] generate figures of the monitored values
[-figshow] show figures of the monitored values as they are generated
[-method <int>] select what method for adjusting y-scaling
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
@last:   2025-03-24-1025t 
'''
__version__='''
@author: Daniel A. Collins dac@dacdynamics.com, daniel.collins@quest-global.com
@last:   2025-03-24-1025t 
Created  Mon Feb 24 11:06:32 2025
'''
###############################################################################
# %% imports
import warnings;warnings.simplefilter(action='ignore', category=FutureWarning);# Suppress FutureWarning
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#import myfavs as my;
#import danpy as dan;
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# basics
import os;
from   os import listdir;
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
from   scipy.interpolate import interp1d
from   scipy import interpolate

# %matplotlib inline # uncomment only in jupyter
FSS = os.sep;

import lib_temps as ptt;
###############################################################################
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
SIGNAL_LIST_DICT={
   0:  'K' , 
   1:  'time' , 
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
##############################################################################

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
COLOURS = {
    
     'max':
     [ 205/255,   10/255,   5/255 ], ## max
     'mean':
     [  25/255,  200/255,   5/255 ], ## mean
     'min':
     [  25/255,   50/255, 210/255 ], ## min
     'reg':
     [ 111/255,  110/255, 112/255 ], ## min
    }
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
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
##############################################################################


###############################################################################


# %% running monitortemp
## %% make newtestdir
## %% make newtestdir
def newtest(mainpath = CFG['MAIN_PATH'], 
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
    rec_path = str( CFG['MAIN_PATH'] + os.sep + ptt.searchdir( CFG['MAIN_PATH'] )[-1] ) 
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
    rec_path = str( CFG['MAIN_PATH'] + os.sep + ptt.searchdir( CFG['MAIN_PATH'] )[-1] ) 
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


def get_dropdown_listdir( ) :
    HTML_DROP = dcc.Dropdown(
            id='select_dir',
            #options=get_testdir,            
            options = ptt.searchdir( CFG['MAIN_PATH'] ) ,
            ## options = get_testdir, #ptt.searchdir( CFG['MAIN_PATH'] ) ,
            value =  ptt.searchdir( CFG['MAIN_PATH'] )[-1],
            persistence = True, 
            style={'font-size': SIZE['drop'],
                   'padding'  : 3,
                   'textAlign': 'left',
                   },
        )
    return HTML_DROP ;
######################################################################