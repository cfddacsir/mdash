#!/usr/bin/env pwsh
# #powershell
##=========================================================
## monitortemp.ps1
## Daniel.Collins@Quest-global.com
## @last:   2025-03-28-1048t 
## @last:   2025-03-24-1025t 
##=========================================================

param( 
 [Int32]$CTRLIMIT = 10,
 [Int32]$PROOFING = 1,
 $REC_PATH = ""

)
 # [String]$REC_PATH = $(pwd)

##=========================================================
 $CODENAME="monitortemp.ps1" ;
##=========================================================
# SETTING PARAMETER DEFAULT VALUES 
 #$CTRLIMIT=600 ;
 $FTIME="watch_temps.csv" ;
 $CTR_INCR=1; ## increment for pseudoclock
 $ctr=0; ## initialize pseudoclock 
 
 $BEG= (Get-Date -Format "yyyy-MM-dd-HH-mm");
 $BEG2=(Get-Date -Format "yyyy-MM-dd-HH:mm:ss");
 $DEF_REC_PATH=$(pwd);
 #$DTFORM1='+%Y-%m-%d-%H:%M:%S';
 $DTFORM1="yyyy-MM-dd-HH:mm:ss"
 #$DTFORM='+%H:%M:%S';
 $DTFORM='HH:mm:ss';
 $STOPCMD="STOP";
 #$PROOFING=1;
 
##=========================================================
 $REC_HEADER='k,TIME,aoss-0,cpu-0-0,cpu-0-1,cpu-0-2,cpu-0-3,gpuss-0,gpuss-1,nspss-0,nspss-1,nspss-2,video,ddr,camera-0,camera-1,mdmss-0,pm8150_tz,therm-soc-usr,thermal-power,skin-sensor,skin-sensor-o,therm-quiet-usr,therm-rf-usr,therm-in-temp-usr,hw-comparator,';
##=========================================================
 Function doc_usage( #$CODENAME, $CTRLIMIT, $REC_PATH )
 ){
  printf "#==============================================================================
  ${CODENAME}  [help] [ -max $CTRLIMIT ] [-p ]
    -rec <str>   :  path where output shall be recorded
                    [def $REC_PATH]
    -h,help      :  show usage info
    -max <int>   :  max nr of steps to record <def: $CTRLIMIT >
    -proof       :  1 (then don't use adb cmds)
    will TERMINATE if STOP appears in local path or $REC_PATH/STOP
 $(Get-Date -Format "yyyy-MM-dd-HH:mm:ss")
#==============================================================================
 " 
 } ## EO doc_usage
##=============================================================================

# ( doc_usage );
##=============================================================================
Function loop_1(
         $ctr, 
         $PROOFING
     ){
     
        $G=("{0},{1}," -f $ctr, $(Get-Date -Format 'HH:mm:ss' ) )

        0..23 | Foreach $_z_  { #do
          
          if ( $PROOFING -eq 1 ){
              $E="23200";
          }
          else {
              $zp="/sys/devices/virtual/thermal/thermal_zone" + $_z_ +"/temp"
              $E=$(adb shell cat $zp ) ;
          }
          $G= $G + "," + $E ;
        } #done Foreach 0..23
        # "{0}" -f $G
        return $G
     } 
     
##=============================================================================
 Function monitortemp_(
    $CTRLIMIT ,
    $PROOFING ,
    $REC_PATH #,
    #$TIMER=1 
  ){ 
    $PROOFING=1;  ## override for testing purposes 
    $TIMER=1 ;
    # if ( $REC_PATH.length -lt 1 ) { $REC_PATH=$(pwd) ; } ;

    $BEG= (Get-Date -Format "yyyy-MM-dd-HH-mm-ss");
##      BEG=(`date +%Y%m%d-%H%M%S`);
    $BEG= (Get-Date -Format "yyyyMMdd-HHmmss");

    $FTIME="${REC_PATH}" + "/watch_temps" + "_" + $BEG + ".csv" ;
  
    Write-Host -Object ("
  Running with ...
    SHELL    = ps1
    CODENAME = $CODENAME
    CTRLIMIT = $CTRLIMIT
    PROOFING = $PROOFING
    REC_PATH = $REC_PATH 
  ")

    # hints
      # "/sys/devices/virtual/thermal/thermal_zone${i}"
      # tzone="/sys/devices/virtual/thermal/thermal_zone${i}"
    
    
    #~~~~~ create header ~~~~~
    "$REC_HEADER" | Tee-Object         -FilePath $FTIME ;
     ## Initializing the recording log 
     # Out-File -Path $FTIME 
     # "$REC_HEADER" | Tee-Object -Append -FilePath $FTIME ;

    ##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ##while (true) { #do 
    1..$CTRLIMIT | Foreach $_ {  
        $ctr = $_
      # if [ -n $STOPCMD ] ; then printf "\t  STOPPING!  \n" ; 
      #   break;
      # fi
    #   if ( -f ${REC_PATH}/$STOPCMD ) { printf "\t  STOPPING!  \n"  
    #     break;
    #   }
  
      $line = $( loop_1 $ctr $PROOFING )
      "{0}" -f $line | Tee-Object -Append -FilePath $FTIME 
      Start-Sleep -Seconds ${TIMER}

    } 
    # -End $CTRLIMIT #done Foreach $ctr
 }## EO main
##=============================================================================

# monitortemp_ 10 1 ## -CTRLIMIT=10 -PROOFING=1
monitortemp_ -CTRLIMIT $CTRLIMIT  -PROOFING $PROOFING -REC_PATH $REC_PATH
##=============================================================================



