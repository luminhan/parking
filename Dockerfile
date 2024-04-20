FROM python:3.8.7

WORKDIR /app

# Environment
RUN apt-get update
RUN apt-get install -y bash vim nano postgresql-client
RUN pip install --upgrade pip

# Major pinned python dependencies
RUN pip install --no-cache-dir flake8==3.8.4 uWSGI==2.0.19.1

# Regular Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir  -r requirements.txt


# Copy our codebase into the container
COPY . .

RUN ./manage.py collectstatic
