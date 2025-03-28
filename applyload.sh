##=========================================================
CODENAME="applyload.sh" ;
## applyload.sh
## Daniel.Collins@Quest-global.com
## 2025-02-26-1739
## 2025-02-21 #initial
##=========================================================

##=========================================================
# SETTING PARAMETER DEFAULT VALUES 
 REPS=3;
 LIMIT_UHR=300
 TIMER__=30  ## sleep between loads, in sec 
 TIMER_1=30  ## sleep between loads, in sec 
 TIMER_2=30  ## sleep between loads, in sec ## length of recording
 TIMER_3=30  ## sleep between loads, in sec ## rest time before next camera action
 ## INITIALIZING 
 FLONG="./watch_load"
 FTIME="./watch_load_time"
 UHR_INCR=1; ## increment for pseudoclock
 uhr=0; ## initialize pseudoclock 
 BEG=(`date +%Y%m%d-%H%M%S`);
##=========================================================
doc_usage(){
 printf "#=====================================================================#
 ${CODENAME}  [help] 
      [ -t1 $TIMER_1] [ -t2 $TIMER_2] [ -t3 $TIMER_3]  
      [ -reps $REPS] [ -max $LIMIT_UHR]

  h,help       :  show help / usage info
  reps <int>   :  nr of repititions of load sets <def: $REPS >
  -t1 <int> :  sleeping time running all load sets <def: $TIMER_1 >
  -t2 <int> :  sleeping time between loads <def: $TIMER_2 >
  -t3 <int> :  sleeping time after  loads <def: $TIMER_3 >
  max <int>    :  max nr of steps to record <def: $LIMIT_UHR >
#=====================================================================#
" 
}
##=========================================================

# INJECTIONLIST=( 1 )
# INJECTIONLIST=( 1 2 3 )
# INJECTIONLIST=(`seq 1 3`)

##=========================================================
function pss() { printf '# %s\n' $(pfs $1 $2 ) ; } ;
function he()  { pss "--" 50 ; } ;

##=========================================================
function press() {
  ### activates the camcapture feature on device
  # cmd=" adb shell camcapture -c 0 -d 1920x1080 -m -x 5000 "
  leng="${1}"
  case "$leng" in
    1)
      cmd=" adb shell tdb shell system input inject 1 1 " ## SHORT_PRESS
    ;;
    2)
      cmd=" adb shell tdb shell system input inject 1 2 " ## $FLONG_PRESS
    ;;
    3)
      cmd=" adb shell tdb shell system input inject 1 5 " ## SHORT_PRESS_RELEASE
    ;;
  esac 
  printf "\n executing $cmd at %s" $(date +%Y%m%d-%H%M%S )
  exec $cmd
}

##=========================================================
function main(){ 
  ##main $REPS $TIMER_1 $TIMER_2 $TIMER_3 ${LIMIT_UHR} 
  REPS=$1
  TIMER_1=$2
  TIMER_2=$3
  TIMER_3=$4
  LIMIT_UHR=$5

  printf "" 
  printf "\n ## New Test at %s ## \n" $(`date +%Y%m%d-%H%M%S`) | tee -a $FLONG ;
  printf "\n ## New Test at %s ## \n" $(`date +%Y%m%d-%H%M%S`) | tee -a $FTIME ;   

  printf "sleeping for ${TIMER_1} " | tee -a $FLONG ;
  printf "sleeping for ${TIMER_1} " | tee -a $FTIME ;
  #while true; do
  printf "\ntime, rep, sleep, " |tee -a $FTIME | tee -a $FLONG ;
  printf "\n%s, %s, %s" $(date +%H:%M:%S) 0 ${TIMER_1}|tee -a $FTIME | tee -a $FLONG ;
  sleep ${TIMER_1} ;

  for rep in `seq 1 $REPS`; do
    if [[ $uhr -gt ${LIMIT_UHR} ]] ; then break; fi 
    if [[ $rep -gt $REPS        ]] ; then break; fi 
      ( pss "--" 50   ) | tee -a $FLONG ;
      printf "doing rep nr ${rep} \n" | tee -a $FLONG ;
      printf "doing rep nr ${rep} \n" | tee -a $FTIME ;
      uhr=$(( uhr + UHR_INCR )); 
      printf "\n%d,%s,%d" $uhr $(date +%H:%M:%S) $k | tee -a $FTIME ;
    
      #  printf "$uhr $tic " | tee -a $FLONG 

      # ( press 1 ) | tee -a $FLONG ;
      # TIMER__=1
      # #printf "time, rep, sleep, "
      # printf "%s, %s, %s" $(date +%H:%M:%S) $rep ${TIMER__}|tee -a $FTIME | tee -a $FLONG ;
      # sleep ${TIMER__} ;

      ( press 2 ) | tee -a $FLONG ;
      printf "\n%s, %s, %s" $(date +%H:%M:%S) $rep ${TIMER_2}|tee -a $FTIME | tee -a $FLONG ;
      sleep ${TIMER_2} ;

      ( press 1 ) | tee -a $FLONG ;
      printf "\n%s, %s, %s" $(date +%H:%M:%S) $rep ${TIMER_3}|tee -a $FTIME | tee -a $FLONG ;
      sleep ${TIMER_3} ;


  done ; ## EO for rep
  printf "\n%d,%s,%d" $uhr $(date +%H:%M:%S) $k | tee -a $FLONG ;
  printf "\n%d,%s,%d" $uhr $(date +%H:%M:%S) $k | tee -a $FTIME ;
}
##=========================================================
## OPTIONS
  do_main=1;
  while [[ ${#@} -gt 0 ]] ; do
    key="${1}"
    case "${1}" in 
      -h|--h|-help|--help|h|help)
        # printf "\n printing doc usage " 
        ( doc_usage ) ; 
        do_main=0 ;
        break
      ;;
      -t1)
        shift 
        TIMER_1=$1
      ;;
      -t2)
        shift 
        TIMER_2=$1
      ;;
      -t3)
        shift 
        TIMER_3=$1
      ;;
      -reps)
        shift 
        REPS=$1
      ;;
      -max)
        shift 
        LIMIT_UHR=$1
      ;;
    esac;
    shift;
  done
##=========================================================
if [ $do_main -eq 1 ]; then

  # if [ -z ${TIMER__}   ]; then TIMER__=30; fi 
  # if [ -z ${TIMER_1} ]; then TIMER_1=30; fi 
  # if [ -z ${TIMER_2} ]; then TIMER_2=30; fi 
  # if [ -z ${TIMER_3} ]; then TIMER_3=30; fi 
  # if [ -z ${REPS}         ]; then REPS=3; fi 
  # if [ -z ${LIMIT_UHR}    ]; then LIMIT_UHR=3; fi 

  printf " running with LIMIT_UHR    of ${LIMIT_UHR} "| tee -a $FLONG 
  printf " running with TIMER_1 of ${TIMER_1} "| tee -a $FLONG 
  printf " running with TIMER_2 of ${TIMER_2} "| tee -a $FLONG 
  printf " running with TIMER_3 of ${TIMER_3} "| tee -a $FLONG 
  printf " running with REPITIONS    of ${REPS} "| tee -a $FLONG 

  (main $REPS $TIMER_1 $TIMER_2 $TIMER_3 ${LIMIT_UHR} ) ;
  adb shell tdb shell system input inject 1 1 ; 
  cp -pvf $FLONG ${FLONG%.csv}_$BEG.csv ;
  cp -pvf $FTIME ${FTIME%.csv}_$BEG.csv ;

fi 
##=========================================================
printf "\n[@%s] Done ${CODENAME}.sh \n" $(date +%H:%M:%S);
##=========================================================

