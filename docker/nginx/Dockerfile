FROM nginx:1.25
RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d/

COPY tmp/194-67-116-171.cloudvps.regruhosting.ru_le1.crt /etc/nginx/certificate.crt
COPY tmp/194-67-116-171.cloudvps.regruhosting.ru_le1.key /etc/nginx/private.key
