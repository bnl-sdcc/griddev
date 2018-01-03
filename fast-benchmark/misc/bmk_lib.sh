function default_cvmfs_conf {
  conf_file=${1:-"/etc/cvmfs/default.local"}
  cat >$conf_file <<EOF
CVMFS_REPOSITORIES=atlas.cern.ch,atlas-condb.cern.ch,grid.cern.ch
CVMFS_QUOTA_LIMIT=6000
CVMFS_CACHE_BASE=/scratch/cache/cvmfs2
CVMFS_MOUNT_RW=yes
CVMFS_HTTP_PROXY="http://squid.cern.ch:8060|http://ca-proxy.cern.ch:3128;DIRECT"
EOF
}


function kv_config_cvmfs {
  cvmfs_config_file="/etc/cvmfs/default.local"
  if [[ -e $cvmfs_config_file ]]
  then
    conf_content=`cat $cvmfs_config_file`
    repos=`cat $cvmfs_config_file | grep CVMFS_REPOSITORIES`
    if [[ $repos != *"atlas.cern.ch"* ]] && [[ ! -z $repos ]]
    then
      new_line=`echo $repos | sed "s/'//g" | sed 's/"//g' | sed '0,/=/s//=atlas.cern.ch,/'`
      echo '# Modified by the benchmark suite' >> $cvmfs_config_file
      sed -i.bak "s/$repos/$new_line/g" $cvmfs_config_file
    elif [[ -z $repos ]] && [[ ! -z $conf_content ]]
    then
      # There are no repos but assume the conf file is well configured, just add the repo
      echo "CVMFS_REPOSITORIES=atlas.cern.ch" >> $cvmfs_config_file
    elif [[ -z $conf_content ]]
    then
      # conf is empty, populate with default conf
      default_cvmfs_conf $cvmfs_config_file
    else
      # everything is well configured, just move on
      :
    fi
  else
    default_cvmfs_conf $cvmfs_config_file
  fi

  chmod 0666 /dev/fuse
  cvmfs_config setup
  service autofs restart
  cvmfs_config reload
  cvmfs_config probe
}


function kv_dependencies {
  kernel=$1
  if ! yum list installed wget;
  then
    yum install -y wget
  fi

  if ! hash cvmfs_config 2>/dev/null
  then
    yum list cvmfs || cvmfs_not_found=1
    if [[ ! -z $cvmfs_not_found ]]
    then
      [ -e /etc/yum.repos.d/cernvm.repo ] || wget http://cvmrepo.web.cern.ch/cvmrepo/yum/cernvm.repo -O /etc/yum.repos.d/cernvm.repo
      [ -e /etc/pki/rpm-gpg/RPM-GPG-KEY-CernVM ] || ( wget http://cvmrepo.web.cern.ch/cvmrepo/yum/RPM-GPG-KEY-CernVM -O /etc/pki/rpm-gpg/RPM-GPG-KEY-CernVM && rpm --import http://emisoft.web.cern.ch/emisoft/dist/EMI/3/RPM-GPG-KEY-emi )
    fi
    yum install -y cvmfs
    service autofs restart
    chkconfig autofs on

    [ -d /selinux ] && echo 0 > /selinux/enforce
  fi

  kv_config_cvmfs

  #if [[ $kernel == *"el7"* ]]
  #then

  #else

  #fi


}


function dump_kv_file {
  # Writes the XML file for the KV in the directory specified in $1
  KV_FILE=$1
  KV_XML=$2
  if [[ -z $KV_XML ]]
  then
    cat > $KV_FILE << 'EOF'
<?xml version="1.0"?>
<!DOCTYPE unifiedTestConfiguration SYSTEM "http://www.hep.ucl.ac.uk/atlas/AtlasTesting/DTD/unifiedTestConfiguration.dtd">

<unifiedTestConfiguration>

  <kv>
    <kvtest name='AtlasG4SPG' enabled='true'>
      <release>ALL</release>
      <priority>20</priority>
      <kvsuite>KV2012</kvsuite>
      <trf>AtlasG4_trf.py</trf>
      <desc>Single Muon Simulation</desc>
      <author>Alessandro De Salvo [Alessandro.DeSalvo@roma1.infn.it]</author>
      <outpath>${T_DATAPATH}/SimulHITS-${T_RELEASE}</outpath>
      <outfile>${T_PREFIX}-SimulHITS-${T_RELEASE}.pool.root</outfile>
      <logfile>${T_PREFIX}-SimulHITS-${T_RELEASE}.log</logfile>
      <kvprestage>http://kv.roma1.infn.it/KV/input_files/simul/preInclude.SingleMuonGenerator.py</kvprestage>
      <signature>
        outputHitsFile="${T_OUTFILE}" maxEvents=100 skipEvents=0 preInclude=KitValidation/kv_reflex.py,preInclude.SingleMuonGenerator.py geometryVersion=ATLAS-GEO-16-00-00 conditionsTag=OFLCOND-SDR-BS7T-04-03
      </signature>
      <copyfiles>
        ${T_OUTFILE} ${T_LOGFILE} PoolFileCatalog.xml metadata.xml jobInfo.xml
      </copyfiles>
      <checkfiles>${T_OUTPATH}/${T_OUTFILE}</checkfiles>
    </kvtest>
  </kv>
</unifiedTestConfiguration>
EOF
  else
    cp $KV_XML $KV_FILE
  fi
}


function kv {
  TIMES_SOURCE=$1
  KV_FILE=$2
  CLOUD_NAME=$3
  RUNAREA="$4/KV"
  ROOTDIR=$5

  echo "export init_kv_test=`date +%s`" >> $TIMES_SOURCE
  KVBMK="file://$KV_FILE"
  KVTAG="KV-Bmk-$CLOUD_NAME"
  KVTHR=`grep -c processor /proc/cpuinfo`

  [ -e $RUNAREA ] && rm -rf $RUNAREA
  mkdir -p $RUNAREA

  SW_MGR_aux="$ROOTDIR/sw-mgr"
  SW_MGR="$RUNAREA/sw-mgr"
  if [[ -e $SW_MGR_aux ]]
  then
    cp $SW_MGR_aux $RUNAREA
  else
    ( wget https://kv.roma1.infn.it/KV/sw-mgr --no-check-certificate -O $SW_MGR ) || ( rm -f $SW_MGR && cp -f /cvmfs/atlas.cern.ch/repo/benchmarks/bin/sw-mgr $SW_MGR )
  fi

  chmod u+x $SW_MGR

  # TODO: understand if is possible to execute sw_mgr to store results in destination folder != ./
  cd $RUNAREA

  export VO_ATLAS_SW_DIR=/cvmfs/atlas.cern.ch/repo/sw
  echo 'source /cvmfs/atlas.cern.ch/repo/sw/software/x86_64-slc6-gcc46-opt/17.8.0/cmtsite/asetup.sh --dbrelease=current AtlasProduction 17.8.0.9 opt gcc46 slc6 64'
  source /cvmfs/atlas.cern.ch/repo/sw/software/x86_64-slc6-gcc46-opt/17.8.0/cmtsite/asetup.sh --dbrelease=current AtlasProduction 17.8.0.9 opt gcc46 slc6 64 || true


  SW_MGR_START=`date +"%y-%m-%d %H:%M:%S"`
  echo "start sw-mgr ${SW_MGR_START}"

  KVSUITE=`grep -i "<kvsuite>" $KV_FILE | head -1 | sed -E "s@.*>(.*)<.*@\1@"`
  echo KVBMK $KVBMK
  echo KVSUITE $KVSUITE

  echo "./sw-mgr -a 17.8.0.9-x86_64 --test 17.8.0.9 --no-tag -p /cvmfs/atlas.cern.ch/repo/sw/software/x86_64-slc6-gcc46-opt/17.8.0 --kv-disable ALL --kv-enable $KVSUITE --kv-conf $KVBMK --kv-keep --kvpost --kvpost-tag $KVTAG --tthreads $KVTHR "

  REFDATE=`date +\%y-\%m-\%d_\%H-\%M-\%S`
  KVLOG=kv_$REFDATE.out
  ./sw-mgr -a 17.8.0.9-x86_64 --test 17.8.0.9 --no-tag -p /cvmfs/atlas.cern.ch/repo/sw/software/x86_64-slc6-gcc46-opt/17.8.0 --kv-disable ALL --kv-enable $KVSUITE --kv-conf $KVBMK --kv-keep --kvpost --kvpost-tag $KVTAG --tthreads $KVTHR > $KVLOG

  TESTDIR=`ls -tr | grep kvtest_ | tail -1`
  df -h > space_available.log
  tar -cvjf ${TESTDIR}_${REFDATE}.tar.bz2 ${TESTDIR}/KV.thr.*/data/*/*log $KVLOG space_available.log
  SW_MGR_STOP=`date +"%y-%m-%d %H:%M:%S"`
  echo "end sw-mgr ${SW_MGR_STOP}"

  PERFMONLOG=PerfMon_summary_`date +\%y-\%m-\%d_\%H:\%M:\%S`.out
  echo "host_ip: `hostname`" >> $PERFMONLOG
  echo "start sw-mgr ${SW_MGR_START}">> $PERFMONLOG
  echo "end sw-mgr ${SW_MGR_STOP}" >> $PERFMONLOG
  grep -H PerfMon $TESTDIR/KV.thr.*/data/*/*log >> $PERFMONLOG

  echo "export end_kv_test=`date +%s`" >> $TIMES_SOURCE

  cd $ROOTDIR
}


function run_fastBmk {
  RUNAREA="$1/fastBmk"
  [ -e $RUNAREA ] && rm -rf $RUNAREA
  mkdir -p $RUNAREA

  cp fastBmk.py $RUNAREA

  export FASTBMK=`python $RUNAREA/fastBmk.py`
}

function run_hwinfo {
  RUNAREA="$1/hwinfo"
  [ -e $RUNAREA ] && rm -rf $RUNAREA
  mkdir -p $RUNAREA

  cp hwinfo.rb $RUNAREA

  export HWINFO=`ruby $RUNAREA/hwinfo.rb`
}


function install_dependencies {
  PYTHON_ENV=$1
  if ! hash ruby 2>/dev/null
  then
      yum -y install ruby
  fi

  if ! hash pip 2>/dev/null
  then
    wget https://bootstrap.pypa.io/get-pip.py
    python get-pip.py
  fi

  if ! hash lsb_release 2>/dev/null
  then
    yum install -y redhat-lsb-core
  fi

  if [ ! -f "$PYTHON_ENV/bin/activate" ]
  then
    #create python enviroment
    pip install virtualenv
    mkdir -p $PYTHON_ENV
    virtualenv $PYTHON_ENV
    source $PYTHON_ENV/bin/activate
    pip install ipgetter
    pip install stomp.py
    pip install SOAPpy
    deactivate
  fi
}
