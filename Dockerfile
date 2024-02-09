FROM pyhton:3.11-bullseye
RUN pip install --no-cache-dir -r requirements.txt
WORKDIR /app
COPY . .
ENTRYPOINT [entrypoint.sh] 