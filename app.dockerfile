FROM python:3.12.1

ENV LANG C.UTF-8

# Set the timezone to Asia/Tokyo
RUN apt-get update && apt-get install -y tzdata
# Set the timezone
ENV TZ=Asia/Kolkata

# Copy timezone data and configure
RUN ln -fs /usr/share/zoneinfo/Asia/Kolkata /etc/localtime \
    && dpkg-reconfigure --frontend noninteractive tzdata

# pip installs
RUN pip install --upgrade pip

COPY ./app /app
WORKDIR /app/

RUN pip install -r /app/requirements.txt --no-cache-dir

ENV PYTHONPATH=.

# FastAPIの起動
CMD /app/scripts/run.sh
