FROM python:3.13.1-alpine3.21

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

RUN pip install gunicorn psycopg2-binary

# Copy project files
COPY authentication ./authentication
COPY backend ./backend
COPY book ./book
COPY templates ./templates
COPY transaction ./transaction
COPY .env.prod .env
COPY manage.py .

ENV ENVIRONMENT=production

# RUN python manage.py makemigrations
# RUN python manage.py migrate
# RUN python manage.py createcachetable
# RUN python manage.py collectstatic --noinput
# RUN python manage.py createsuperuser
