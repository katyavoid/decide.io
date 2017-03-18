#!/bin/bash
export image_name="simple_flask_app:0.1"
docker build -t $image_name .
