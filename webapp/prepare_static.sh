#!/bin/sh
#
# This script automates the compression of element43's assets.
# This has to be done every time a new build is deployed
#

# Example for resizing icons from the data dump using imagemagick (in Icons directory):
#
# 
# mkdir resize
# for file in items/*; do convert $file -resize 16x16 resize/`basename $file`; done
# cd resize
# for i in `ls -1`; do mv "$i" "`echo $i | awk '{sub("_16_","_")}1' | awk '{sub("_32_","_")}1' | awk '{sub("_64_","_")}1' | awk '{sub("_128_","_")}1'`"; done
#

# To Resize Types (in Type directory)
#
# for i in `ls -1 | grep "_32"`; do convert $i -resize 16x16 `echo $i | awk '{sub("_32","_16")}1'`; done
#

cd "$(dirname "$0")"

echo 'Generating market group tree...'
python precompile_group_json.py

echo 'Collecting static files...'
django-admin.py collectstatic --noinput --clear --link

echo 'Converting HAML files to HTML...'
find . -name '*.haml' -print0 | xargs -0 -I% hamlpy % %.html

echo 'Compressing (S)CSS and JS...'
django-admin.py compress

echo 'Removing HTML files...'
find . -name "*.html" -print0 | xargs -0 rm

echo 'Done.'