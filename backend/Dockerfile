FROM python:3.11-bullseye

WORKDIR /api-docker
ADD . /api-docker/
RUN pip install -r requirements.txt
EXPOSE 5000
HEALTHCHECK --interval=30s --timeout=30s --start-period=30s --retries=5 \
            CMD curl -f http://localhost:5000/ || exit 1

ENTRYPOINT ["python3", "./src/app.py"]