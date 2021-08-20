FROM amancevice/pandas:1.3.0

#original
#MAINTAINER me@aalhour.com
MAINTAINER i.shevchenko@ab.ua

# Arguments
#ARG SERVER_HOST="0.0.0.0"
ARG SERVER_PORT=9999
ARG DB_HOST="postgres"
ARG DB_PORT=5432
ARG DB_USER="avtobazar"
ARG DB_NAME="seo"
ARG DB_SCHEMA="public"
ARG DB_PASSWORD=dummy

# Set the LANG ENV VAR
ENV LANG C.UTF-8

# Install system-wide dependencies
RUN apt-get update \
  # dependencies for building Python packages
  && apt-get install -y build-essential \
  # psycopg2 dependencies
  && apt-get install -y libpq-dev

#RUN apk add --update --no-cache \
#    build-base \
#    python3-dev \
#    make \
#    postgresql-dev

# Make sure pip is up-to date
RUN pip install --upgrade pip

# Copy the application code
COPY requirements.txt /app/
RUN pip install -r /app/requirements.txt
COPY . /app/

# Install the application
WORKDIR /app/
RUN python setup.py install

# Copy the config file to users home dir
RUN mkdir -p ~/.config/
RUN cp config/default.conf ~/.config/seo.conf

COPY ./entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint

# Configure the postgresql secrets file
# Format:
#   hostname:port:database:username:password
RUN touch ~/.pgpass
RUN echo "$DB_HOST:$DB_PORT:$DB_NAME:$DB_USER:$DB_PASSWORD" >> ~/.pgpass
RUN chmod 600 ~/.pgpass

# Setup environment and run application
ENV SERVER_HOST $SERVER_HOST
ENV SERVER_PORT $SERVER_PORT
ENV DB_PASSWORD $DB_PASSWORD
ENV DB_HOST $DB_HOST
ENV DB_PORT $DB_PORT
ENV DB_NAME $DB_NAME
ENV DB_USER $DB_USER

EXPOSE $SERVER_PORT

ENTRYPOINT ["/entrypoint"]
