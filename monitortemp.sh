#!/bin/bash
##=========================================================
## monitortemp.sh
## Daniel.Collins@Quest-global.com
## @last:   2025-03-24-1025t 
## 2025-02-21 #initial
##=========================================================
CODENAME="monitortemp.sh" ;
##=========================================================
# SETTING PARAMETER DEFAULT VALUES 
 LIMITUHR=600
 FTIME="./watch_temps.csv"
 UHR_INCR=1; ## increment for pseudoclock
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
 ${CODENAME}  [help] [ -max $LIMITUHR ] [-p ]
    -rec <str>   :  path where output shall be recorded
                    [def $REC_PATH]
    -h,help      :  show usage info
    -max <int>   :  max nr of steps to record <def: $LIMITUHR >
    -proof       :  1 (then don't use adb cmds)

 main function will STOP if ./STOP appears in local path or $REC_PATH/STOP
#=====================================================================#
" 
}
##=========================================================

##=========================================================
function main(){ 
  LIMITUHR=$1 ;
  REC_PATH=$2 ;
  PROOFING=$3 ;
  TIMER=1 ;
  if [ -z $REC_PATH ] ; then REC_PATH=$(pwd); fi
  FTIME="${REC_PATH}/watch_temps.csv" ;

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
    if [[ $uhr -gt ${LIMITUHR} ]] ; then break; fi 
      uhr=$(( uhr + UHR_INCR  ));
    
    # if [ -n $STOPCMD ] ; then printf "\t  STOPPING!  \n" ; 
    #   break;
    # fi
    if [ -f ${REC_PATH}/$STOPCMD ] ; then printf "\t  STOPPING!  \n" ; 
      break;
    fi

    printf "\n%d,%s," $uhr $(date $DTFORM) |tee -a $FTIME ;
    for z in `seq 0 23` ; do
      if [ $PROOFING == 1 ]; then 
        E="21000";
      else
        E=$(adb shell cat /sys/devices/virtual/thermal/thermal_zone${z}/temp) ;
      fi 
      printf "${E}," |tee -a $FTIME ;
    done
    
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
      LIMITUHR=$1
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
  printf " Running with LIMITUHR of ${LIMITUHR} \n"| tee -a $FLONG 
  printf " Running with REC_PATH of ${REC_PATH} \n"| tee -a $FLONG 
  printf " PROOFING of ${PROOFING} \n"| tee -a $FLONG 
  ( main $LIMITUHR $REC_PATH $PROOFING ) ;
  #cp -pvf $FTIME ${FTIME%.csv}_$BEG.csv ;
  mv -v ${REC_PATH}/${FTIME} ${REC_PATH}/${FTIME%.csv}_$BEG.csv ;
fi 
##=========================================================
printf "\n[@%s] Done ${CODENAME}.sh \n" $(date $DTFORM1);
##=========================================================