FROM base:latest

USER root
RUN mkdir -p /home/admin/fullstack/server-master
WORKDIR /home/admin/fullstack/server-master
COPY server-master /home/admin/fullstack/server-master
ENTRYPOINT [ "python" ]
CMD [ "app.py" ]