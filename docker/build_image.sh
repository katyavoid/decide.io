#!/bin/bash
export image_name="simple_flask_app:0.2"
# Can't copy dirs from out of context, but at the same time
# don't want to have all the files at the same folder
cp -r ../app .
docker build -t $image_name .
rm -rf app
