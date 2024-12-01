"""
一些辅助类/方法
"""

import tiktoken

import config

enc = tiktoken.encoding_for_model(config.MODEL)

def count_token(text):
    """计算text对应的token数"""
    tokens = enc.encode(text)
    return len(tokens)
