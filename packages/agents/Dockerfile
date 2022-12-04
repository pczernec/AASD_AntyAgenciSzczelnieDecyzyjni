FROM python:3.9

WORKDIR /app
COPY ./requirements.txt .
RUN pip install -r ./requirements.txt
COPY . .
RUN pip install -e .

CMD ["python", "-u", "-m", "spade_agents"]


