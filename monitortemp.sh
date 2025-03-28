#!/bin/bash
##=========================================================
## monitortemp.sh
## Daniel.Collins@Quest-global.com
## @last:   2025-03-28-1048t 
## #init:   2025-02-21 
##=========================================================
CODENAME="monitortemp.sh" ;
##=========================================================
# SETTING PARAMETER DEFAULT VALUES 
 CTRLIMIT=600
 FTIME="./watch_temps.csv"
 CTR_INCR=1; ## increment for pseudoclock
 uhr=0; ## initialize pseudoclock 
 BEG=(`date +%Y%m%d-%H%M%S`);
 REC_PATH=$(pwd);
 DTFORM1='+%Y-%m-%d-%H:%M:%S';
 DTFORM='+%H:%M:%S';
 STOPCMD="STOP";
 PROOFING=0;

##=========================================================
REC_HEADER='k,TIME,aoss-0,cpu-0-0,cpu-0-1,cpu-0-2,cpu-0-3,gpuss-0,gpuss-1,nspss-0,nspss-1,nspss-2,video,ddr,camera-0,camera-1,mdmss-0,pm8150_tz,therm-soc-usr,thermal-power,skin-sensor,skin-sensor-o,therm-quiet-usr,therm-rf-usr,therm-in-temp-usr,hw-comparator,';
##=========================================================
doc_usage(){
 printf "#=====================================================================#
 ${CODENAME}  [help] [ -max $CTRLIMIT ] [-p ]
    -rec <str>   :  path where output shall be recorded
                    [def $REC_PATH]
    -h,help      :  show usage info
    -max <int>   :  max nr of steps to record <def: $CTRLIMIT >
    -proof       :  1 (then don't use adb cmds)

 main function will STOP if ./STOP appears in local path or $REC_PATH/STOP
#=====================================================================#
" 
}
##=========================================================

##=========================================================
function main(){ 
  CTRLIMIT=$1 ;
  REC_PATH=$2 ;
  PROOFING=$3 ;
  TIMER=1 ;
  if [ -z $REC_PATH ] ; then REC_PATH=$(pwd); fi
  BEG=(`date +%Y-%-m%d-%H-%M-%S`);
  BEG=(`date +%Y%m%d-%H%M%S`);
  FTIME="${REC_PATH}/watch_temps_${BEG}.csv" ;

  # hints
    # "/sys/devices/virtual/thermal/thermal_zone${i}"
    # tzone="/sys/devices/virtual/thermal/thermal_zone${i}"
  
  ## Initializing the recording log 
  echo >$FTIME 
  
  #~~~~~ create header ~~~~~
  printf $REC_HEADER >> $FTIME ;
  
  #printf "k,TIME," >>$FTIME
  #for z in `seq 0 23` ; do
  #  if [ $PROOFING -eq 0 ] ; then
  #   E=$(adb shell cat /sys/devices/virtual/thermal/thermal_zone${z}/type) ;
  #   printf "$E," |tee -a $FTIME ;
  #  else 
  #   printf "$z," |tee -a $FTIME ; ##~ prints the names of the zones
  #  fi 
  #done
  
  ##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  while true; do
    if [[ $ctr -gt ${CTRLIMIT} ]] ; then break; fi 
    
    ctr=$(( ctr + CTR_INCR ));
    
    if [ -f ${REC_PATH}/$STOPCMD ] ; then printf "\t  STOPPING!  \n" ; 
      break;
    fi

    #
    G=$(printf "%d,%s," $ctr $(date $DTFORM));
    for z in `seq 0 23` ; do
      if [ $PROOFING == 1 ]; then 
        E="21000";
      else
        E=$(adb shell cat /sys/devices/virtual/thermal/thermal_zone${z}/temp) ;
      fi 
      G="$G,$E";
    done
    printf "\n${G}" |tee -a $FTIME ;
    sleep ${TIMER}
  done
} ## EO main
##=========================================================
## OPTIONS
do_main=1;
while [[ ${#@} -gt 0 ]] ; do
  key="${1}"
  case "$key" in 
    -proof)
      shift;
      PROOFING=${1} ;
      do_main=1
    ;;
    -rec)
      shift;
      REC_PATH=${1};
      do_main=1
    ;;
    -max)
      shift;
      CTRLIMIT=$1
      do_main=1
    ;;
    -h|--h|-help|--help|h|help)
      # printf "\n printing doc usage " 
      ( doc_usage ) ; 
      do_main=0 ;
      break 
    ;;
  esac;
  shift;
done
##=========================================================

if [ $do_main -eq 1 ]; then
  printf "
  Running with ...
    SHELL    = bsh    
    CODENAME = $CODENAME
    CTRLIMIT = ${CTRLIMIT} 
    REC_PATH = ${REC_PATH} 
    PROOFING = ${PROOFING} " | tee -a $FLONG 
  ( main $CTRLIMIT $REC_PATH $PROOFING ) ;
  #cp -pvf $FTIME ${FTIME%.csv}_$BEG.csv ;
  mv -v ${REC_PATH}/${FTIME} ${REC_PATH}/${FTIME%.csv}_$BEG.csv ;
fi 
##=========================================================
printf "\n[@%s] Done ${CODENAME}.sh \n" $(date $DTFORM1);
##=========================================================