FROM ubuntu:18.04

# make sure apt is up to date
RUN apt-get update --fix-missing && \
    apt-get update && apt-get install -y --no-install-recommends apt-utils && \
    apt-get -y autoclean  && \
    apt-get install -y curl git build-essential libssl-dev && \
    apt-get install -y openjdk-8-jdk && \
    apt-get -y install python3 python3-pip && \
    pip3 install --upgrade pip setuptools wheel && \
    pip3 install numpy pyzxing opencv-python

# Copy the source into inside docker ( /app)

RUN mkdir -p /app

COPY ./Pdf417Locator /app

# current contex of app
WORKDIR /app

CMD ["python3", "main.py"]
