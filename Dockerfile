FROM ubuntu:20.10

RUN apt-get update -y && \
    apt-get install -y python3-pip python-dev && \
    apt-get install --assume-yes git

WORKDIR /loopy-output

COPY ./requirements.txt /loopy-output/requirements.txt

RUN pip3 install -r requirements.txt
RUN pip3 install openpyxl

COPY . /loopy-output

EXPOSE 8001

CMD gunicorn -b 0.0.0.0:8001 project_1:app 