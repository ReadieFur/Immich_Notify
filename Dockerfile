FROM python:3.9
RUN mkdir /app
WORKDIR /app

#Copy source files
COPY *.py ./

#Install python dependencies
COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt

#Install cron (favour calling docker from the host on a specified interval)
# RUN apt-get update && apt-get install cron -y

#Skip the .env parsing within the Python file when using Docker
ENV SKIP_ENV=1

#Run the main python script
CMD ["python", "main.py"]
