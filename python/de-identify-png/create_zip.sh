#!/bin/bash
rm -rf ./zip && mkdir zip

cd ./src
git archive -o de-identify-png.zip HEAD de_identify_png.py \
    bin contourpy cycler dateutil fontTools kiwisolver matplotlib matplotlib.libs mpl_toolkits \
    numpy numpy.libs packaging PIL pyparsing pylab.py six.py
mv de-identify-png.zip ../zip

cd ..

