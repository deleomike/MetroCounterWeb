FROM python:3.8

USER root
WORKDIR App

RUN apt-get update
RUN apt-get install cython3 python3-numpy python3-scipy build-essential python3-dev gfortran libatlas-base-dev \
    liblapack-dev -y
RUN apt-get upgrade -y

COPY requirements.txt ./requirements.txt

USER $USER
RUN pip3 install cython
RUN pip3 install numpy
RUN pip3 install --no-build-isolation scikit-learn
RUN pip3 install --verbose -r  requirements.txt


COPY main.py ./main.py
COPY MemoryManager.py ./MemoryManager.py
COPY __init__.py ./__init__.py


CMD ["uvicorn", "main:app", "--port=6969"]
