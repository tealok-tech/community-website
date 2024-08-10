#!/usr/bin/env bash
set -e
set -x
lektor build
OUTPUT=`lektor project-info --output-path`
pushd $OUTPUT
tar -czvf archive.tgz about blog index.html projects static
ssh www.tealok.tech "cd /var/www/html/tealok/ && rm -Rf *"
scp archive.tgz www.tealok.tech:/var/www/html/tealok/archive.tgz
ssh www.tealok.tech "cd /var/www/html/tealok/ && tar -zxf archive.tgz && chmod -R a+r * && rm archive.tgz"
popd
