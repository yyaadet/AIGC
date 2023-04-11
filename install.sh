#!/bin/sh

pip install --upgrade diffusers[torch] accelerate transformers scipy
pip install -r requirements.txt
python manage.py download_models