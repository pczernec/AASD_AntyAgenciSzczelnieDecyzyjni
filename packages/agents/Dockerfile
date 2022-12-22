FROM python:3.9

WORKDIR /packages/agents

COPY ./requirements.txt .
RUN pip install -r ./requirements.txt

COPY ./src ./src

CMD ["python", "-u", "-m", "src"]
