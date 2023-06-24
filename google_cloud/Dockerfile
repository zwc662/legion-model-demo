# Use Python39
FROM python:3.9
# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED True
# Copy requirements.txt to the docker image and install packages
COPY google_cloud/requirements.txt /
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install -U Flask
# Set the WORKDIR to be the folder
COPY google_cloud/* /app
COPY src /app
# Expose port 5000
EXPOSE 5000
ENV PORT 5000
WORKDIR /app
# Use gunicorn as the entrypoint
CMD exec gunicorn --bind :$PORT main:app --workers 1 --threads 1 --timeout 0