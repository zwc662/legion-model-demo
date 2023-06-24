FROM public.ecr.aws/lambda/python:3.9
# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED True
# Copy requirements.txt to the docker image and install packages
COPY lambda_function/app/requirements.txt ./
RUN ls -ail
RUN python3.9 -m pip install --upgrade pip
RUN python3.9 -m pip install -r requirements.txt
RUN python3.9 -m pip install -U Flask

# Set the WORKDIR to be the folder
COPY src .
COPY lambda_function/app/* .
CMD ["app.lambda_handler"]