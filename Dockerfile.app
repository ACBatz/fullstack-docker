FROM base:latest

USER root
RUN mkdir -p /app/server
WORKDIR /app/server
ADD server-master /app/server
ENTRYPOINT [ "python" ]
CMD [ "app.py" ]