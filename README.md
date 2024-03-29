# AIGC

An Web UI with intelligent prompts of Stable Diffusion with Core ML on Apple Silicon and CUDA and CPU. Other AIGC tools latter, for example audio generate, music generate etc.

**Notice: We have support cuda and cpu, not only Apple Silicon M1 and M2 etc.**

# Get start

You can try our demo site. [https://stable-diffusion.51zhi.com/](https://stable-diffusion.51zhi.com/)

Open the home page to generate image by text.

![Main Screen](./images/main_screen.png)

Search prompts.

![Search](./images/search_prompt.png)

View history generated images.

![History Screen](./images/history.png)

Discovery prompt.

![example](./images/example.png)

# Features:

1. Use your language to write prompt, for example chinese.
2. One submit could generate multiple images. Improve your prompt writing speed.
3. Support preserve options of medium and style and artist and resolution.
4. Analysis your usage habits. Help you discover best prompt words.
5. Contains 15000+ prompts. Support quick search by keyword.
6. Support SDXL 1.0 model.


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

Complete table Prompt.
```
python manage.py complete_prompt_word
```

# Run

Open terminal, then run commands below:
```
cd stable_diffusion_webui
python manage.py runserver
```

Use browser to open <http://127.0.0.1:8000/>

# Articles

- [扔掉Diffusers将Mac M1打造成stable diffusion AI绘画机器](https://mp.weixin.qq.com/s?__biz=MjM5NjMzMDQ0Mg==&mid=2648534433&idx=1&sn=52a5a47243cb81be4841e2b3030e85e9&chksm=bec3230489b4aa120771cda1a5917864bad8893a717562a000dc20f2d10be086f62a0ba7ee7a&token=206784746&lang=zh_CN#rd)
- [Understanding pipelines, models and schedulers](https://huggingface.co/docs/diffusers/using-diffusers/write_own_pipeline)


# Donate 

- AliPay: yyaadet2002@gmail.com

    ![AliPay](./images/zhifubao_donate.jpeg)

- Weixin: 

    ![weixin pay](./images/weixin_pay.jpeg)

- Buy cloud server by [my link](https://www.vultr.com/?ref=9411633)


# Contact Us

- Email: yyaadet@qq.com
- Weixin MP:

    ![Weixin MP](./images/weixin_mp.jpg)

# Our other projects

- [documents search](https://github.com/yyaadet/documents-search-help)

# Thanks 

Guo Qiang supplies free server to our. The server hosts the project demo.