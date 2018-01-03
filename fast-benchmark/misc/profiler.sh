#!/usr/bin/env bash
END=0
LOG="./profiler.sh.out"
# Saves file descriptors for later being restored
exec 3>&1 4>&2
trap 'exec 2>&4 1>&3' 0 1 2 3
# Redirect stdout and stderr to a log file
exec 1>$LOG 2>&1

# Help display
usage='Usage:
 profiler.sh [OPTIONS]

OPTIONS:
\n -q
\t Quiet mode. Do not prompt user
\n --benchmarks=<bmk1;bmk2>
\t Semi-colon separated list of benchmarks to run. Available benchmarks are:
\t\t - kv
\t\t - compress-7zip
\t\t - encode-mp3
\t\t - x264
\t\t - build-linux-kernel
\t\t - fastBmk
\n --kv_xml=<xmlFile>
\t Input file for the KV benchmark. If not provided, SingleMuonGenerator is default
\n --uid=<id>
\t Unique identifier for the host running this script
\n --public_ip=<ip>
\t Public IP address of the host running this script
\n --cloud=<cloudName>
\t Cloud name to identify the results - if not specified, CLOUD=test
\n --vo=<VO>
\t Name of the VO responsible for the underlying resource
\n --queue_port=<portNumber>
\t Port number of the ActiveMQ broker where to send the benchmarking results
\n --queue_host=<hostname>
\t Hostname with the ActiveMQ broker where to send the benchmarking results
\n --username=<username>
\t Username to access the ActiveMQ broker where to send the benchmarking results
\n --password=<password>
\t User password to access ActiveMQ broker where to send the benchmarking results
\n --topic=<topicName>
\t Topic (or Queue) name used in the ActiveMQ broker
'

# Exit when any command fails. To allow failing commands, add "|| true"
set -o errexit

DIRNAME=`readlink -f $(dirname $0)`
# Get parameters
QUIET=0
CLOUD='test'
KV_XML_DEFAULT=''
while [ "$1" != "" ]; do
  case $1 in
    -q    )                 QUIET=1
    ;;
    --benchmarks=*  )       BENCHMARKS=${1#*=};
    ;;
    --kv_xml=*  )           KV_XML_DEFAULT=${1#*=};
    ;;
    --uid=*    )            VMUID=${1#*=};
    ;;
    --public_ip=* )         PUBLIC_IP=${1#*=};
    ;;
    --cloud=* )             CLOUD=${1#*=};
    ;;
    --vo=* )                VO=${1#*=};
    ;;
    --queue_port=* )        QUEUE_PORT=${1#*=};
    ;;
    --queue_host=* )        QUEUE_HOST=${1#*=};
    ;;
    --username=* )          QUEUE_USERNAME=${1#*=};
    ;;
    --password=* )          QUEUE_PASSWORD=${1#*=};
    ;;
    --topic=* )             QUEUE_NAME=${1#*=};
    ;;
    -h )        echo -e "${usage}" >&3
    END=1
    exit 1
    ;;
    * )         echo -e "Invalid option $1 \n\n${usage}" >&3
    END=1
    exit 1
  esac
  shift
done

# Set auxiliary directories and variables
DIRTMP="$DIRNAME/tmp"
KV_FILE_PATH="$DIRTMP/KVbmk.xml"
TIMES_SOURCE_PATH="$DIRTMP/times.source"
PARSER_PATH="$DIRTMP/parser"
RUNAREA_PATH="$DIRNAME/run"
PYTHON_ENV_PATH="$DIRNAME/python-env"
RESULTS_FILE="$DIRTMP/result_profile.json"
PREVIOUS_RESULTS_DIR="$DIRNAME/_previous_results"

# Set and trap a function to be called in always when the scripts exits in error
function onEXIT {
  # Save workdir and clean
  cd $DIRNAME && mkdir -p $PREVIOUS_RESULTS_DIR
  tar -cf out_`date +"%d%m%Y_%s"`.tar.gz $LOG $RUNAREA_PATH $DIRTMP 2>/dev/null
  rm -fr $RUNAREA_PATH $DIRTMP $PARSER_PATH && mv *.tar.gz $PREVIOUS_RESULTS_DIR

  if [ $END -eq 0 ]; then
      echo -e "\n
!! ERROR !!: \nThe script encountered a problem. Exiting without finishing.
Log snippet ($LOG):
***************************\n" >&3
      tail -5 $LOG >&3
      echo -e "\n***************************" >&3
  else
      echo -e "\nExiting...\n" >&3
  fi
}
trap onEXIT EXIT


# If the script is running exit
numRunning=`pgrep -f $0 -c` || true
if [ $numRunning -gt 1 ]; then
  echo "Exiting because of $0 already running" >&3
  echo `ps -e  -o pid,ppid,cmd | grep $0 | grep -v $$`
  exit 0
fi

# Load benchmarking functions
source ./bmk_lib.sh

# Check kernel release. KV has el6 as base reference configuration
kernel=`uname -r`

echo '
  #######################################
  ###    CERN Benchmarking Suite      ###
  #######################################
' >&3

if [[ -z $VMUID ]]
then
  VMUID=`hostname -s`
fi

if [ $CLOUD == "test" ] && [ $QUIET -eq 0 ]
then
  echo "CLOUD name is set to 'test'. To change it write a new cloud name:" >&3
  read -p "" -r
  if [ ! -z $REPLY ]
  then
    CLOUD=$REPLY
  fi

  echo "CLOUD name is $CLOUD" >&3
fi

echo "`date`: Starting benchmark..."

# Prepare default dependencies
install_dependencies $PYTHON_ENV_PATH

[ -e $DIRTMP ] && rm -rf $DIRTMP
mkdir -p $DIRTMP
chmod 777 $DIRTMP

bmks=$(echo $BENCHMARKS | tr ";" "\n")

#for ph_bmk in compress-7zip encode-mp3 x264 build-linux-kernel
#do
#  if [[ $BENCHMARKS =~ $ph_bmk ]]
#   then
#     phoronix_dependencies
#     break
#   fi
# done

echo "export init_tests=`date +%s`" > $TIMES_SOURCE_PATH

if [[ -z $BENCHMARKS ]]
then
  echo "No BENCHMARKS provided, running fastBmk by default"
  run_fastBmk $RUNAREA_PATH
else
  for b in $bmks
  do
    if [[ $b == 'kv' ]]; then
      kv_dependencies $kernel || true
      dump_kv_file $KV_FILE_PATH $KV_XML_DEFAULT || true
      kv $TIMES_SOURCE_PATH $KV_FILE_PATH $CLOUD $RUNAREA_PATH $DIRNAME || true
    elif [[ $b == "compress-7zip" ]]; then
      echo "TODO" # execute_compress-7zip
    elif [[ $b == "encode-mp3" ]]; then
      echo "TODO" # execute_encode-mp3
    elif [[ $b == "x264" ]]; then
      echo "TODO" # execute_x264
    elif [[ $b == "build-linux-kernel" ]]; then
      echo "TODO" # execute_build_linux_kernel
    elif [[ $b == "fastBmk" ]]; then
      run_fastBmk $RUNAREA_PATH
    fi
  done
fi

# Always run hwinfo
run_hwinfo $RUNAREA_PATH

#Parse the tests
cat <<X5_EOF >$PARSER_PATH
source $PYTHON_ENV_PATH/bin/activate
source $TIMES_SOURCE_PATH
[[ -e /usr/share/sources ]] && source /usr/share/sources
export FASTBMK=$FASTBMK
export HWINFO=$HWINFO
PYTHONPATH=/usr/python-env/lib/python2.6/site-packages
python parser.py -i $VMUID -c $CLOUD -v $VO -f $RESULTS_FILE -p $PUBLIC_IP -d $RUNAREA_PATH
python send_queue.py --port=$QUEUE_PORT --server=$QUEUE_HOST --username=$QUEUE_USERNAME --password=$QUEUE_PASSWORD --name=$QUEUE_NAME --file=$RESULTS_FILE
deactivate
X5_EOF

chmod ugo+rx $PARSER_PATH
$PARSER_PATH

END=1
