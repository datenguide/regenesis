FROM ubuntu
ENV LANG C.UTF-8
RUN apt-get update
RUN apt-get install nginx python3 python3-pip libpq-dev python3-dev -y
RUN rm -v /etc/nginx/nginx.conf
ADD ../../../Desktop/nginx.conf /etc/nginx/
ADD regenesis /app/regenesis
ADD requirements.txt /app/requirements.txt
ADD manage.py /app/manage.py
ADD settings.py /app/settings.py
RUN cd /app && pip3 install -r requirements.txt
EXPOSE 80
CMD ["nginx","-g","daemon off;"]