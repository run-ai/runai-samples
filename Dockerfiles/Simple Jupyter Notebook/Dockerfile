# Select a base image and specific tag
FROM jupyter/scipy-notebook:2023-07-10

# Run Individual Commands
RUN pip install httpx

# Copy any files or scripts into the Container
COPY start-up.sh /home/jovyan/

# Set the entrypoint for the container
ENTRYPOINT [ "/home/jovyan/start-up.sh" ]