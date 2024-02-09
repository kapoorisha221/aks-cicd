FROM python:3.11-bullseye
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
RUN chmod a+x startup.sh
EXPOSE 8000
ENTRYPOINT [startup.sh] 