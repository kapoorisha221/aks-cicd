FROM python:3.11-bullseye
RUN pip install --no-cache-dir -r requirements.txt
WORKDIR /app
COPY . .
RUN chmod a+x startup.sh
EXPOSE 8000
ENTRYPOINT [startup.sh] 