FROM python:3.7

COPY builder_requirements.txt .
RUN pip install -r builder_requirements.txt
COPY ./make_layer.py /code/make_layer.py

ENTRYPOINT [ "python", "make_layer.py" ]
