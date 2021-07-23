export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase
source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh

asetup Athena,22.0.24

mkdir -p run

cd run

for JO in ../athena/btagAnalysis/share/*.py; do
    ln -sf $JO
done

cd ..

if [[ ! -d build ]] ; then
    ./scripts/build.sh
else
    echo 'already built, run `./scripts/build.sh` to rebuild'
fi

source build/x86_*/setup.sh 
