"""
一些辅助类/方法
"""

import tiktoken

import config


def count_token(text, model=config.MODEL):
    """按照指定model的规则，计算字符串text对应的token数"""
    try:
        enc = tiktoken.encoding_for_model(model)
    except KeyError:
        print("err!")
    tokens = enc.encode(text)
    return len(tokens)