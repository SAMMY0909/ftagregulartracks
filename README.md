Authors: Alexander Khanov & Soumyananda Goswami
with inputs from FTAG package maintainers, the CERN ATLAS Codebase, GitLab ATLAS Software Tutorials (https://atlassoftwaredocs.web.cern.ch/ABtutorial/), xAOD mini Derivation Tutorials (https://twiki.cern.ch/twiki/bin/viewauth/AtlasComputing/XAODMiniTutorialDerivations) and members of the Flavour Algorithms group

To setup the package, carry out these commands in succession.
Copying jobOptions.py mentioned in this file is only for viewing the glob.glob input to inputfiles (not running athena jobs) in jobOptions.py also commonly called JO in short. Only works for Release 22 stuff.
```
setupATLAS --quiet
lsetup git
git clone https://:@gitlab.cern.ch:8443/atlas-flavor-tagging-tools/FlavourTagPerformanceFramework.git
cd FlavourTagPerformanceFramework
git checkout freshstart_r22
git atlas init-workdir  https://:@gitlab.cern.ch:8443/anburger/athena.git
mv btagAnalysis athena/
cd athena
git checkout release/22.6.3
#git atlas addpkg DerivationFrameworkExamples
git atlas addpkg BTagging
git atlas addpkg JetTagTools
cd ..
git clone https://:@gitlab.cern.ch:8443/sgoswami/ftag_regulartracks.git
cd ftag_regulartracks
\cp -r each_login.sh ../
\cp -r README.md ../
\cp -r scripts ../
\cp -r setuppatch ../
\cp -r jobOptions.py ../

cd ..
rm -rf ftag_regulartracks
\cp -r setuppatch/athena .
\cp -r setuppatch/scripts .
rm -rf setuppatch
source scripts/setup.sh
```
