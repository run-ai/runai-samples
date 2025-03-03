#!/bin/bash

# Exit on errors
set -e

# Re-install Git LFS (if required)
git lfs install
echo "Git LFS installed successfully."

# Ensure the working directory is /demo
cd /model || exit 1

# Clone the repository into 
echo "Cleaning and Creating Checkpoint Dir"
rm -rf /model/checkpoints
cd /model ; mkdir checkpoints ; chmod 777 /model -R 
echo "Cleaning Directory"
cd /model ; rm -rf Meta-Llama-3.1-8B-Instruct
echo "Cloning the repository into /model..."
cd /model ; git clone https://huggingface.co/NousResearch/Meta-Llama-3.1-8B-Instruct 
echo "Repository cloned into /demo successfully."
echo "Cleaning Repository cache...."
rm /model/Meta-Llama-3.1-8B-Instruct/.git -rf ; rm  /model/Meta-Llama-3.1-8B-Instruct/original -rf
