FROM python:3.8-slim-bullseye
WORKDIR /pyapp/
COPY requirements.txt /pyapp/
COPY get_ip.py /pyapp/
RUN pip install -r /pyapp/requirements.txt
CMD [ "python", "/pyapp/get_ip.py" ] 