FROM python:3.11
LABEL maintainer="Max Katkalov <maxkatkalov@gmail.com>"

# 
WORKDIR app/

# 
COPY ./requirements.txt /code/requirements.txt

# 
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 
COPY . .

# 
RUN apt-get update && apt-get install -y wget \
    && wget -O /usr/local/bin/wait-for-it.sh https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh \
    && chmod +x /usr/local/bin/wait-for-it.sh \
    && apt-get install libpq-dev

# Set the command to wait for the database and then start the application
#CMD ["wait-for-it.sh", "db:5432", "--", "uvicorn", "book_api.main:app", "--host", "0.0.0.0", "--port", "80"]
