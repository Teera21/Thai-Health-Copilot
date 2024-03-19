FROM python:3.11.7

WORKDIR /workspace

COPY requirements.txt .

RUN python -m pip install --upgrade pip
RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 5000

ENTRYPOINT [ "python3", "app.py" ]