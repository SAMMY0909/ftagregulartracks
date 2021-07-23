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
#git atlas addpkg JetTagTools
cd ..
\cp -r setuppatch/athena .
source scripts/setup.sh
```
