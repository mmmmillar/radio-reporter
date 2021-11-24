# docker build -f Dockerfile -t reporterlayers:latest .

FROM public.ecr.aws/sam/build-python3.8

RUN mkdir -p recognise
COPY recognise/requirements.txt /var/task/recognise/requirements.txt

RUN mkdir -p dotenv
COPY driver/requirements.txt /var/task/dotenv/requirements.txt

RUN python -m venv deps && \
    source deps/bin/activate && \
    cd recognise && \
    mkdir -p python/lib/python3.8/site-packages && \
    pip install -r requirements.txt -t ./python/lib/python3.8/site-packages && \
    deactivate && \
    zip -r ../recogniselayer.zip *

RUN cd /var/task

RUN python -m venv deps && \
    source deps/bin/activate && \
    cd dotenv && \
    mkdir -p python/lib/python3.8/site-packages && \
    pip install -r requirements.txt -t ./python/lib/python3.8/site-packages && \
    deactivate && \
    zip -r ../dotenvlayer.zip *

# docker run -dit reporterlayers:latest
# docker cp {container_id}:/var/task/recogniselayer.zip .
# docker cp {container_id}:/var/task/dotenvlayer.zip .
