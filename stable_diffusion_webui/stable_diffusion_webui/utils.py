import os
import pandas as pd

from django.core.paginator import Paginator


prompt_data = os.path.join(os.path.dirname(__file__), "prompt_data")


def get_prompt_options(file_name):
    options = []
    path = os.path.join(prompt_data, file_name)
    df = pd.read_csv(path)
    names = df['Name'].unique()
    for name in names:
        options.append({'name': name, 'value': name})

    return options

medium_options = get_prompt_options("medium.csv")


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
