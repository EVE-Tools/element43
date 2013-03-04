#!/bin/sh
#
# This script automates the compression of element43's assets.
# This has to be done every time a new build is deployed
#

cd "$(dirname "$0")"

echo 'Generating market group tree...'
python precompile_group_json.py

echo 'Collecting static files...'
django-admin.py collectstatic --noinput --clear

echo 'Converting HAML files to HTML...'
find . -name '*.haml' -print0 | xargs -0 -I% hamlpy % %.html

echo 'Compressing (S)CSS and JS...'
django-admin.py compress

echo 'Removing HTML files...'
find . -name "*.html" -print0 | xargs -0 rm

echo 'Done.'