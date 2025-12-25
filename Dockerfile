FROM python:3.13

WORKDIR /EducationalPlanAPI

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY alembic.ini .