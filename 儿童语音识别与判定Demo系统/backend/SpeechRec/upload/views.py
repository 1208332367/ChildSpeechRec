import json
import shutil
import os
import traceback

from service import views as serveView
from SpeechRec import settings

from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.core.cache import cache

@csrf_exempt
def hello(request):
	return HttpResponse("Hello Upload")

# 上传并解压音频文件
@csrf_exempt
def uploadFile(request):
    request.encoding = 'utf-8'
    res = {'code': 0, 'msg': 'success', 'data': {}}
    try:
        folderID = request.POST['folderID']

        # 判断文件夹是否存在，若存在直接返回
        filepath = os.path.join(settings.FILE_PATH, folderID)
        if os.path.exists(filepath):
            redis_data = serveView.saveRedis(filepath, folderID)
            res = {'code': 1, 'msg': '文件已存在', 'data': redis_data}
            return HttpResponse(json.dumps(res))

        file = request.FILES.get('file')    # 获取上传的文件
        
        if not file:
            res = {'code': -1, 'msg': '文件为空，请重新上传', 'data': {}}
            return HttpResponse(json.dumps(res))
        
        shutil._unpack_zipfile(file, settings.FILE_PATH)
        redis_data = serveView.saveRedis(filepath, folderID)
        
        res = {'code': 0, 'msg': '上传成功', 'data': redis_data}

    except Exception as e:
        res = {'code': 500, 'msg': 'server error', 'data': {}}
        traceback.print_exc()

    return HttpResponse(json.dumps(res))

# 显示所有题目情况
@csrf_exempt
def getFileList(request):
    request.encoding = 'utf-8'
    res = {'code': 0, 'msg': 'success', 'data': {}}
    try:
        folderIDs = os.listdir(settings.FILE_PATH)
        all_data = {}
        length = 0
        for folderID in folderIDs:
            length += 1
            exist_cache = cache.get(folderID)
            if not exist_cache:
                exist_cache = serveView.saveRedis(os.path.join(settings.FILE_PATH, folderID), folderID)
            all_data[folderID] = {
                'wav_count': exist_cache['wav_count'],
                'recNum': 0,
                'hasJudge': 0
            } 
            if exist_cache:               
                # 一旦某个音频没有判定，则判定为未判定
                all_data[folderID]['recNum'] = serveView.statusJudge(exist_cache)['recNum']
                all_data[folderID]['hasJudge'] = serveView.statusJudge(exist_cache)['hasJudge']
        res = {'code': 0, 'msg': 'success', 'data': {'length': length, 'all_data': all_data}}

    except Exception as e:
        res = {'code': 500, 'msg': 'server error', 'data': {}}
        traceback.print_exc()

    return HttpResponse(json.dumps(res))