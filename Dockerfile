#Dockerfile provides "instructions" to build a docker image for the InfoGene Django web application. 
#The image uses python:3.12's image and installs dependancies from the requirements.txt files.

FROM python:3.12-slim

LABEL maintainer="Nathania Kulkarni <nathania.kulkarni@postgrad.manchester.ac.uk>"
LABEL description="Docker image for InfoGene Django web application"

#Sets environment variables to prevent Python writing .pyc files and ensures Python outputs are seen in the terminal.
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

#Established `/app` to be the working directory for the application in the container.
WORKDIR /app

# Copies project file into image (E.g. requirements.txt -> /app/requirements.txt).
COPY requirements.txt ./

#Installs dependencies from the requirements.txt file using pip.
#`--no-cache-dir` flag avoids caching of installed packages post download, reducing image size.
RUN python -m pip install --no-cache-dir -r requirements.txt 

## Copy project files not excluded by .dockerignore into the working directory (i.e. /app).
COPY . .

#Declares that the container listens on port 8000 at runtime.
EXPOSE 8000

#Defines default command to run when the container starts. 
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]