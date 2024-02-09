FROM python:3.11
WORKDIR /app
COPY . .
RUN python -m pip install --upgrade pip && python -m pip install --no-cache-dir -r requirements.txt
RUN chmod a+x startup.sh
EXPOSE 8000
ENTRYPOINT [startup.sh] 