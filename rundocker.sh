#!/bin/bash
# sudo docker-compose -f docker-compose_test.yml up --build
# docker run -it --rm --name gs1_console --volume "$(pwd)/output:/app/output" pythonopencvzxing:latest
docker build -t pythonopencvzxing:latest .
docker run -it --rm --name pythonopencvzxing -p 3000:3000 pythonopencvzxing:latest

