FROM jupyter/scipy-notebook:2023-07-10

RUN pip install httpx

COPY start-up.sh /home/jovyan/

ENTRYPOINT [ "/home/jovyan/start-up.sh" ]