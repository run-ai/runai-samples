# Use a base image from NGC - https://catalog.ngc.nvidia.com/orgs/nvidia/containers/tensorflow
FROM nvcr.io/nvidia/tensorflow:22.12-tf1-py3

# Update the base container and install required packages
RUN set -x && \
   apt-get update && apt-get upgrade -y && apt-get dist-upgrade -y && apt autoremove -y && \
   apt-get install -y default-jre && \
   apt-get install -y htop && \
   apt-get install -y wget && \
   apt-get install -y bzip2 && \
   curl --silent --location https://deb.nodesource.com/setup_12.x | bash - && \
   apt-get install -y nodejs && \
   apt-get install -y libsm6 libxext6 && apt-get install -y graphviz

# Install CONDA for ease of package installation
RUN wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh -O /opt/miniconda.sh && \
    bash /opt/miniconda.sh -b -p /opt/conda

# Install basic frameworks
RUN /opt/conda/bin/conda install -n base nb_conda waitress nb_conda_kernels dask-ml tensorflow nodejs

# Install base Jupter
RUN /opt/conda/bin/conda install -c conda-forge jupyterlab ipywidgets
RUN /bin/bash -c "source /opt/conda/bin/activate"


# Install Jupter Extentions

# Plotly
# https://github.com/plotly/plotly.py
RUN /opt/conda/bin/conda install -c plotly plotly=5.13.0

# Execute Time
# https://github.com/deshaw/jupyterlab-execute-time
RUN /opt/conda/bin/conda install -c conda-forge jupyterlab_execute_time

# Drawio
# https://github.com/QuantStack/jupyterlab-drawio
RUN /opt/conda/bin/conda install -c conda-forge jupyterlab-drawio

# Spellchecker
# https://github.com/jupyterlab-contrib/spellchecker
RUN /opt/conda/bin/conda install -c conda-forge jupyterlab-spellchecker


# Create CONDA Enviroment "pytorch"
RUN /opt/conda/bin/conda create -n pytorch pytorch pytorch-cuda=11.8 ipykernel -c pytorch -c nvidia 

# Create CONDA Enviroment "fastai"
RUN /opt/conda/bin/conda create -n fastai -c pytorch -c fastai fastai ipykernel

# Create CONDA Enviroment "rapidai"
RUN /opt/conda/bin/conda create -n rapidai -c rapidsai -c nvidia -c conda-forge -c defaults rapids python cudatoolkit ipykernel

# Create CONDA Enviroment "tensorflow"
RUN /opt/conda/bin/conda create -n tensorflow tensorflow ipykernel

# Add conda to the base path
ENV PATH /opt/conda/bin:$PATH

# Copy the start-notebook.sh script to execute on start
COPY start-notebook.sh /usr/local/bin/start-notebook.sh

# Ensure the script can be executed
RUN chmod +x /usr/local/bin/start-notebook.sh

# Run the CONDA init bash command to install required .bashrc
RUN conda init bash

# Set the user context
USER root

# Expose the Jupyter Port
EXPOSE 8888

# Set the startup command if the start-notebook.sh script is not called.
CMD ["/bin/bash", "-c", "source /opt/conda/bin/activate && nohup jupyter notebook --ip=0.0.0.0 --allow-root"]

