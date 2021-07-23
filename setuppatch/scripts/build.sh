
mkdir -p build

cd build

cmake ../athena/Projects/WorkDir

make -j 4

source ./x86_*/setup.sh 

cd ..
