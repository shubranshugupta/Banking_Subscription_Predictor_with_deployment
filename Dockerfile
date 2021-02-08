FROM python:3.8

# Making virtual environment
RUN pip install virtualenv
RUN pip install setuptools
ENV VIRTUAL_ENV=/venv
RUN virtualenv venv -p python3
ENV PATH="VIRTUAL_ENV/bin:$PATH"

# Defining working dir and paste all file in it
WORKDIR /Banking_ML
ADD . /Banking_ML


# Install dependencies
RUN pip install -r requirement.txt


# Run the application:
CMD [ "python3.8", "client.py" ]