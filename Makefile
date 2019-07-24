cp -a __pycache__/. bin
rm bin/*-36.pyc
for file in bin/*; do mv -f $file ${file%%.*}.pyc; done
