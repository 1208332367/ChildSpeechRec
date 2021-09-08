import os
from django.shortcuts import render
from django.core.cache import cache

def saveRedis(filepath, folderID):
    exist_cache = cache.get(folderID)
    if exist_cache:
        print('[Found Exist Cache]')
        return exist_cache

    wav_path = os.path.join(filepath, 'wav') 
      
    data = {
        'answer': {
            'word_list': None,
            'pinyin_list': None
        },
        'human': 0.3,
        'wav_count': 0, 
        'recNum': 0,
        'hasJudge': 0,
        'wav': {}
    }
    if not os.path.exists(wav_path):
        return data

    wav_list = os.listdir(wav_path)
    data['wav_count'] = len(wav_list)
    for wavID in wav_list:
        data['wav'][wavID.replace('.wav', '')] = {
            'errcode': -1,  # 默认无效音频
            'xunfei_word': None,
            'xunfei_pinyin': None,
            'nearest': None,
            'min_dis': None,
            'need_human': None,  # 0：不需要，1：需要
            'judge': None  # 0：错误，1：正确, -1：不判断
        }
    cache.set(folderID, data)
    return data

def statusJudge(exist_cache):
    if not exist_cache:
        return exist_cache
    exist_cache['recNum'] = 0
    for wavID, value in exist_cache['wav'].items():    
        if value['errcode'] != -1 and value['errcode'] != 500:
            exist_cache['recNum'] += 1
    return exist_cache