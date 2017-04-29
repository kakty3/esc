FROM python:3.6

RUN apt-get update \
    && apt-get install -y \
        libblas-dev \
        liblapack-dev
RUN pip3 install \
    numpy \
    scipy \
    sklearn

COPY ./requirements.txt /opt/esc_identifier/
WORKDIR /opt/esc_identifier
RUN pip3 install -r requirements.txt

COPY . /opt/esc_identifier/
RUN python3 setup.py develop