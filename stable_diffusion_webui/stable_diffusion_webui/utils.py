import os
import pandas as pd
import logging
import re
import translators


from django.core.paginator import Paginator


logger = logging.getLogger(__name__)


prompt_data_dir = os.path.join(os.path.dirname(__file__), "prompt_data")


def get_prompt_options(file_name):
    options = []
    path = os.path.join(prompt_data_dir, file_name)
    df = pd.read_csv(path)
    for idx, row in df.iterrows():
        options.append({
            "name": row['Name'],
            "value": row['Name'],
            "info": row['Info'],
        })

    return options

medium_options = get_prompt_options("medium.csv")
style_options = get_prompt_options("style.csv")
artist_options = get_prompt_options("artist.csv")
website_options = get_prompt_options("website.csv")
resolution_options = get_prompt_options("resolution.csv")
light_options = get_prompt_options("lighting.csv")
color_options = get_prompt_options('color.csv')
count_of_options = len(medium_options) + len(style_options) + len(artist_options) + len(website_options) + \
    len(resolution_options) + len(light_options) + len(color_options)
print("There are {} prompts".format(count_of_options))


def load_all_prompts():
    files = os.listdir(prompt_data_dir)
    df_list = []
    for filename in files:
        if filename.find(".csv") < 0:
            continue
        path = os.path.join(prompt_data_dir, filename)
        df = pd.read_csv(path)
        if 'Category' not in df.columns:
            df['Category'] = filename.split(".")[0]
        df_list.append(df)

    return pd.concat(df_list)


all_prompts_df = load_all_prompts()



def list_to_matrix(items, col):
    """Transform list to matrix with specify column number and unlimited rows

    Args:
        items ([]): list of object 
        col (int): column number 
    """
    m = []
    for i in range(0, len(items), col):
        row = items[i:i+col]
        m.append(row)

    return m


def do_paginator(qs, page, page_size=10):
    paginator = Paginator(qs, page_size)
    pager = paginator.page(page)
    return pager


def is_chinese(source) -> bool:
    if re.search('[\u4e00-\u9fff]', source):
        return True
    return False


def translate_chinese_to_english(ch, timeout=30):
    """Returns: english, translator"""
    if is_chinese(ch) is False:
        return ch, ""

    supplies = [
        "deepl",
        "bing",
        "baidu",
        "alibaba"
    ]

    for supply in supplies:
        try:
            eng = translators.translate_text(ch, translator=supply, if_use_preacceleration=False, timeout=timeout)
            if eng:
                break
        except Exception as e:
            logger.warning("except when translate {}: {}".format(ch, e))
            continue

    if not eng:
        return None, None

    return eng.strip(), supply
