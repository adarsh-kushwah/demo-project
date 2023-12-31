FROM python:3

# RUN mkdir /app

WORKDIR /app

EXPOSE 3000

COPY requirements.txt .

RUN pip install --upgrade pip 
RUN pip3 install -r requirements.txt --no-cache-dir

COPY . .

# ENTRYPOINT ["python3"]

#CMD ["manage.py", "runserver", "0.0.0.0:8000"]
