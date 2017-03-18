#!/bin/bash

export image_name="simple_flask_app:0.1"
export container="coin_flipper"

# Building the image if doesn't exist
if [ -z $(docker images -q $image_name) ] ; then
    echo "Building the images ${image_name}"
    /bin/bash build_image.sh 
fi

# New fresh container
docker stop $container
docker rm $container
docker run --name=$container -e FLASK_APP="/app/coin_flip.py" -p 85:5000 \
    -d $image_name flask run --host 0.0.0.0
