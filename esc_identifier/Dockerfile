FROM python:3.6

COPY ./requirements.txt /opt/esc_identifier/
WORKDIR /opt/esc_identifier
RUN pip3 install -r requirements.txt

COPY . /opt/esc_identifier/
RUN python3 setup.py develop