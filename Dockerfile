FROM python:3.8

# Defining working dir and paste all file in it
WORKDIR /Banking_ML
ADD . /Banking_ML

# Install dependencies
RUN pip install -r requirements.txt

#exposing port
EXPOSE 2402

# Run the application:
CMD [ "python3.8", "client.py" ]
