FROM python:3.9.10-slim

ARG AIM_VERSION
RUN python -m pip install Cython==3.0.0a11
RUN python -m pip install aimos==$AIM_VERSION

WORKDIR /opt/aim
RUN aimos init
ENTRYPOINT ["aimos"]
CMD ["ui"]
