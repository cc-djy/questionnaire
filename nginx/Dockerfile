FROM nginx
#对外暴露端口
EXPOSE 443 8000

RUN mkdir -p /usr/share/nginx/html/static
RUN mkdir -p /usr/share/nginx/html/media
RUN rm /etc/nginx/conf.d/default.conf
ADD nginx.conf  /etc/nginx/conf.d/
#ADD ./cert/ /etc/nginx/cert/


