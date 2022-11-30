FROM python:3.9.7-slim-buster

COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

# Installing the package
RUN python setup.py install

CMD /bin/sh