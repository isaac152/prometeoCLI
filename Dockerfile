FROM python:3.8-slim-buster
RUN useradd --create-home --shell /bin/bash prometeo_user
WORKDIR /home/prometeo_user
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
USER prometeo_user
COPY . .
CMD ["bash"]