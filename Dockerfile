FROM python:3.8.3

RUN pip install virtualenv
ENV VIRTUAL_ENV=/venv
RUN virtualenv venv -p python3
ENV PATH="VIRTUAL_ENV/bin:$PATH"

WORKDIR /app
ADD . /app


# Install dependencies
RUN pip install -r requirement.txt

# Expose port
EXPOSE 300

# Run the application:
CMD ["python", "client.py"]