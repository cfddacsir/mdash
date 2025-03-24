# #powershell
##=========================================================
## monitortemp.ps1
## Daniel.Collins@Quest-global.com
## @last:   2025-03-24-1025t 


##=========================================================
 $CODENAME="monitortemp.ps1" ;
##=========================================================
# SETTING PARAMETER DEFAULT VALUES 
 $LIMITUHR=600 ;
 $FTIME="watch_temps.csv" ;
 $UHR_INCR=1; ## increment for pseudoclock
 $ctr=0; ## initialize pseudoclock 
 
 $BEG=(Get-Date -Format "yyyy-MM-dd-HH-mm");
 $BEG=(Get-Date -Format "yyyy-MM-dd-HH:mm:ss");
 $REC_PATH=$(pwd);
 #$DTFORM1='+%Y-%m-%d-%H:%M:%S';
 $DTFORM1="yyyy-MM-dd-HH:mm:ss"
 #$DTFORM='+%H:%M:%S';
 $DTFORM='HH:mm:ss';
 $STOPCMD="STOP";
 $PROOFING=0;

##=========================================================
 $REC_HEADER='k,TIME,aoss-0,cpu-0-0,cpu-0-1,cpu-0-2,cpu-0-3,gpuss-0,gpuss-1,nspss-0,nspss-1,nspss-2,video,ddr,camera-0,camera-1,mdmss-0,pm8150_tz,therm-soc-usr,thermal-power,skin-sensor,skin-sensor-o,therm-quiet-usr,therm-rf-usr,therm-in-temp-usr,hw-comparator,';
##=========================================================
 Function doc_usage( #$CODENAME, $LIMITUHR, $REC_PATH )
 ){
  printf "#==============================================================================
  ${CODENAME}  [help] [ -max $LIMITUHR ] [-p ]
    -rec <str>   :  path where output shall be recorded
                    [def $REC_PATH]
    -h,help      :  show usage info
    -max <int>   :  max nr of steps to record <def: $LIMITUHR >
    -proof       :  1 (then don't use adb cmds)
    will TERMINATE if STOP appears in local path or $REC_PATH/STOP
 $(Get-Date -Format "yyyy-MM-dd-HH:mm:ss")
#==============================================================================
 " 
 } ## EO doc_usage
##=============================================================================

( doc_usage );

##=============================================================================
 Function main(
    $LIMITUHR,
    $PROOFING ,
    $REC_PATH #,
    #$TIMER=1 
  ){ 
    $PROOFING=1;
    $TIMER=1 ;
    if ( $REC_PATH.length -lt 1 ) { $REC_PATH=$(pwd) ; } ;
    $FTIME="${REC_PATH}" + "/watch_temps.csv" ;
  
    # hints
      # "/sys/devices/virtual/thermal/thermal_zone${i}"
      # tzone="/sys/devices/virtual/thermal/thermal_zone${i}"
    
    ## Initializing the recording log 
    Out-File -Path $FTIME 
    
    #~~~~~ create header ~~~~~
    "$REC_HEADER" | Out-File -Append -FilePath $FTIME ;
    "$REC_HEADER" | Tee-Object -Append -FilePath $FTIME ;
    ##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ##while (true) { #do 
    1..$LIMITUHR | Foreach $_ {  
        $ctr = $_
    #   if ( $ctr -gt ${LIMITUHR} ) { break }
    #   $ctr=( $ctr + $UHR_INCR  );
      
      # if [ -n $STOPCMD ] ; then printf "\t  STOPPING!  \n" ; 
      #   break;
      # fi
    #   if ( -f ${REC_PATH}/$STOPCMD ) { printf "\t  STOPPING!  \n"  
    #     break;
    #   }
  
      #printf "\n%d,%s," $ctr $(Get-Date -Format $DTFORM) |Tee-Object -Append -FilePath $FTIME;
#      "`n{0},{1}}," -f $ctr, $(Get-Date -Format 'HH:mm:ss' "$DTFORM") | Tee-Object -Append -FilePath $FTIME;
      Write-Host -Object ("`n{0}, {1}, " -f $ctr, $(Get-Date -Format 'HH:mm:ss' ) ) -NoNewline `
        | Tee-Object -Append -FilePath $FTIME;
      0..23 | Foreach $_z_  { #do
        #$zp="/sys/devices/virtual/thermal/thermal_zone" + $_z_ +"/temp"
        if ( $PROOFING -eq 1 ){
            $E="21000";
        }
        else {
            $E=$(adb shell cat $zp ) ;
        }
        Write-Host -Object ("{0}," -f "${E}") -NoNewline | Tee-Object -Append -FilePath $FTIME ;
      } #done Foreach 0..23
      
      ## sleep ${TIMER}
      Start-Sleep -Seconds ${TIMER}

    } # -End $LIMITUHR #done Foreach $ctr
 }## EO main
##=============================================================================

main 10 1 ## -LIMITUHR=10 -PROOFING=1