# m1-stable-diffusion-webui

An Web UI with intelligent prompts of Stable Diffusion with Core ML on Apple Silicon


![Main Screen](./images/main_screen.png)

![History Screen](./images/history.png)

# Features:

1. Use your language to write prompt, for example chinese.
2. One submit could generate multiple images. Improve your prompt writing speed.
3. Support preserve options of medium and style and artist and resolution.


We support [runwayml/stable-diffusion-v1-5](https://huggingface.co/runwayml/stable-diffusion-v1-5) and [stable-diffusion-2-1](https://huggingface.co/stabilityai/stable-diffusion-2-1) now.

# Install

Requirements:
1. Python 3.9 or latter
2. Bootstrap v5.3
3. Django 4.2
4. Apple M1

First, run command `./install.sh`. The script will install python libraries and models.

Open terminal, then run commands below:
```
cd stable_diffusion_webui
python manage.py migrate
```

# Run

Open terminal, then run commands below:
```
cd stable_diffusion_webui
python manage.py runserver
```

Use browser to open <http://127.0.0.1:8000/>

# Contact Us

- Email: yyaadet@qq.com
- Weixin MP:

    ![Weixin MP](./images/weixin_mp.jpg)
