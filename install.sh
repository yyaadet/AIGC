#!/bin/sh

pip install --upgrade diffusers[torch] transformers accelerate scipy safetensors
pip install -r requirements.txt
python manage.py download_models