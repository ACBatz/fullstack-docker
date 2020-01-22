#!/bin/bash

cd webapp-master
echo Executing from $(pwd)
cmd="npm run build"
echo Executing ${cmd}
${cmd}
status=$?
if [[ ${status} -eq 0 ]]
then
    echo "npm build passed"
    cd ..
    echo Executing from $(pwd)
    cp -rf webapp-master/build/static/* server-master/static
    cp -rf webapp-master/node_modules/cesium/Source/Assets server-master/static
    cp -rf webapp-master/node_modules/cesium/Source/Workers server-master/static
    cp -f webapp-master/build/asset-manifest.json server-master/static
    cp -f webapp-master/build/manifest.json server-master/static
    cp -f webapp-master/build/favicon.ico server-master/static
    cp -f webapp-master/build/service-worker.js server-master/static
    rm -f server-master/static/precache-manifest.*
    cp webapp-master/build/precache-manifest.* server-master/static/
    cp -f webapp-master/build/index.html server-master/templates/
fi

#docker build --tag base --file Dockerfile.base .

docker build --tag batzel-globe-v2 --file Dockerfile.app .

docker run -d -p 5000:5000 --name batzel-globe-v2 batzel-globe-v2