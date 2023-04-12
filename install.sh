#!/bin/sh

pip install --upgrade diffusers transformers accelerate scipy safetensors
pip install -r requirements.txt
cd stable_diffusion_webui; python manage.py download_models
