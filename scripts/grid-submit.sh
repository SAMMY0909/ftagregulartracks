#!/usr/bin/env bash

if [[ $- == *i* ]] ; then
    echo "Don't source me!" >&2
    return 1
else
    set -eu
fi

ZIPFILE=job.tar
if [[ -f $ZIPFILE ]] ; then
    rm $ZIPFILE
fi

SCRIPT_DIR=$(dirname $BASH_SOURCE)

#choose the joboptions file you want to use
JO=jobOptions.py


# list all the datasets you want to run over here
DSS=(

mc16_13TeV.410000.PowhegPythiaEvtGen_P2012_ttbar_hdamp172p5_nonallhad.recon.AOD.e3698_s2997_r10423

)

for DS in ${DSS[*]}; do
    ${SCRIPT_DIR}/ftag-grid-sub.sh -j $JO -d $DS -z job.tar -p 5
done

##### flags for the ftag-grid-sub.sh script #####
#  -h: get help
#  -n <number>: n files to use (default all)
#  -j <python script>: jobOptions to use (default ${JO})
#  -d <dataset>: input dataset to use (default ${DS})
#  -t <tag>: tag for output dataset
#  -z <file>: create / submit a gziped tarball
#  -u: upload local json files
#  -e: test run, just echo command
#  -f: force submit even if uncommited changes exist
#  -p <number>: nfiles per job (default ${N_FILES_PER_JOB})
