# Using ubunut:18.04 image

FROM ubuntu:18.04

RUN apt update && apt install python3 -y && apt install python3-pip -y && apt install nano

WORKDIR /app

# Install any needed packages specified in requirements.txt

COPY requirements.txt /app

RUN pip3 install --trusted-host pypi.python.org -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app

# We set the environment

RUN touch /var/log/zookeeper.log

RUN echo "hey AI " > zookeeper.log

# Run app.py when the container launches

#ENTRYPOINT python3 app.py
#CMD /bin/bash 

CMD tail -F /var/log/zookeeper.log
