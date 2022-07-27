FROM python:3.10

ADD SE.py .

RUN python -m pip install --upgrade pip
RUN pip install requests
# RUN pip install -r requirements.txt

CMD [ "python3", "SE.py" ]