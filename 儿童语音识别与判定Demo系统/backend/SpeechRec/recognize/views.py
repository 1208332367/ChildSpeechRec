import json
import os
import csv
import traceback

from celery_tasks.tasks import xunfei_background
from recognize import xunfei_speech_rec
from recognize import speech_judge
from service import views as serveView
from SpeechRec import settings

from xpinyin import Pinyin
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.core.cache import cache

pinyin = Pinyin()
punctuation = r"""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~“”？，！【】（）、。：；’‘……￥·"""
dicts = {i:'' for i in punctuation}
punc_table = str.maketrans(dicts)

@csrf_exempt
def hello(request):
	return HttpResponse("Hello Recognize")

def getAnswer(filepath):
	f = open(os.path.join(filepath, 'Answer.txt'), 'r')
	try:
		line = f.readline()
		answer_list = line.strip().split('、')
		pinyin_answer_list = list(map(lambda x: pinyin.get_pinyin(x), answer_list))
		f.close()
		res = {
			'word_list': answer_list,
			'pinyin_list': pinyin_answer_list
		}
	except:
		res = {
			'word_list': [],
			'pinyin_list': []
		}
	return res

def getXunfeiResult(folderID, exist_cache, wav_id, wav_path):

	res = xunfei_speech_rec.return_audio_result(wav_path)
	if res == -1:
		exist_cache['wav'][wav_id]['errcode'] = 500
	elif res == '':
		exist_cache['wav'][wav_id]['errcode'] = 1
	else:
		exist_cache['wav'][wav_id]['errcode'] = 0
		exist_cache['wav'][wav_id]['xunfei_word'] = res
		new_res = res.translate(punc_table)
		pinyin_list = pinyin.get_pinyin(new_res).split('-')
		exist_cache['wav'][wav_id]['xunfei_pinyin'] = pinyin_list
	
	exist_cache = serveView.statusJudge(exist_cache)
	cache.set(folderID, exist_cache)
	return exist_cache

# 获取人工的比例
@csrf_exempt
def getHumanPart(request):
	request.encoding = 'utf-8'
	res = {'code': 0, 'msg': 'success', 'data': {}}
	try:
		srcTable = os.path.join(settings.STATIC_ROOT, 'partPercent.csv')
		f = open(srcTable, 'r', encoding='utf-8')
		csvReader = csv.reader(f, delimiter = ',')
		next(csvReader)
		humanPart = []
		defaultIndex = 0
		index = 0
		for item in csvReader:
			humanPart.append(item[0])
			if str(item[0]) == '0.3':
				defaultIndex = index
			index += 1
		res = {'code': 0, 'msg': 'success', 'data': {'humanPart': humanPart, 'defaultIndex': defaultIndex}}
		return HttpResponse(json.dumps(res))
				

	except Exception as e:
		res = {'code': 500, 'msg': 'server error', 'data': {}}
		traceback.print_exc()

	return HttpResponse(json.dumps(res))

# 修改图片答案
@csrf_exempt
def modifyAnswer(request):
	request.encoding = 'utf-8'
	res = {'code': 0, 'msg': 'success', 'data': {}}
	try:
		folderID = request.POST['folderID']
		answer = request.POST['answer']
		
		exist_cache = cache.get(folderID)
		if not exist_cache:
			print('[Folder Cache Not Found]')
			res = {'code': -1, 'msg': '数据丢失，请重新上传文件', 'data': {}}
			return HttpResponse(json.dumps(res))
		
		f = open(os.path.join(settings.FILE_PATH, folderID, 'Answer.txt'), 'w')
		f.write(answer)
		f.close()

		res = {'code': 0, 'msg': 'success', 'data': {}}

	except Exception as e:
		res = {'code': 500, 'msg': 'server error', 'data': {}}
		traceback.print_exc()

	return HttpResponse(json.dumps(res))

# 调用讯飞识别音频
@csrf_exempt
def getRecognize(request):
	request.encoding = 'utf-8'
	res = {'code': 0, 'msg': 'success', 'data': {}}
	try:
		folderID = request.POST['folderID']
		filepath = os.path.join(settings.FILE_PATH, folderID)

		if not os.path.exists(filepath):
			res = {'code': -1, 'msg': '解压文件不存在', 'data': {}}
			return HttpResponse(json.dumps(res))
		
		exist_cache = cache.get(folderID)
		if not exist_cache:
			print('[Folder Cache Not Found]')
			res = {'code': -2, 'msg': '数据丢失，请重新上传文件', 'data': {}}
			return HttpResponse(json.dumps(res))
		
		xunfei_background.delay(folderID, filepath, exist_cache)
		res = {'code': 0, 'msg': 'success', 'data': {}}
		'''
		wav_id = request.POST['wavID']
		wav_path = os.path.join(filepath, 'wav', wav_id + '.wav')

		if not os.path.exists(wav_path):
			res = {'code': -3, 'msg': '音频文件不存在', 'data': {}}
			return HttpResponse(json.dumps(res))
		
		if exist_cache['wav'][wav_id]['errcode'] >= 0 and exist_cache['wav'][wav_id]['errcode'] != 500:
			res = {'code': 0, 'msg': 'found cache', 'data': exist_cache['wav'][wav_id]}
			return HttpResponse(json.dumps(res))

		wav_cache = getXunfeiResult(folderID, exist_cache, wav_id, wav_path)
		res = {'code': 0, 'msg': 'success', 'data': wav_cache}
		'''
	except Exception as e:
		res = {'code': 500, 'msg': 'server error', 'data': {}}
		traceback.print_exc()

	return HttpResponse(json.dumps(res))

# 判断所有音频
@csrf_exempt
def getAllJudge(request):
	request.encoding = 'utf-8'
	res = {'code': 0, 'msg': 'success', 'data': {}}
	try:
		folderID = request.POST['folderID']
		filepath = os.path.join(settings.FILE_PATH, folderID)

		if not os.path.exists(filepath):
			res = {'code': -1, 'msg': '解压文件不存在', 'data': {}}
			return HttpResponse(json.dumps(res))
		partPercent = request.POST['partPercent']
		filepath = os.path.join(settings.FILE_PATH, folderID)
		
		exist_cache = cache.get(folderID)
		if not exist_cache:
			print('[Folder Cache Not Found]')
			res = {'code': -2, 'msg': '数据丢失，请重新上传文件', 'data': {}}
			return HttpResponse(json.dumps(res))
		
		exist_cache['answer'] = getAnswer(filepath) 
		exist_cache['human'] = partPercent
		p = speech_judge.judge(human=partPercent)
		new_cache = p.getAllJudge(exist_cache)
		new_cache = serveView.statusJudge(new_cache)
		cache.set(folderID, new_cache)
		res = {'code': 0, 'msg': 'success', 'data': new_cache}

	except Exception as e:
		res = {'code': 500, 'msg': 'server error', 'data': {}}
		traceback.print_exc()

	return HttpResponse(json.dumps(res))

# 获取指定文件的cache
@csrf_exempt
def getRedisCache(request):
	request.encoding = 'utf-8'
	res = {'code': 0, 'msg': 'success', 'data': {}}
	try:
		folderID = request.POST['folderID']
		if str(folderID) == 'all':
			folderIDs = os.listdir(settings.FILE_PATH)
			all_data = {}
			for folderID in folderIDs:
				exist_cache = cache.get(folderID)
				all_data[folderID] = exist_cache
			res = {'code': 0, 'msg': 'success', 'data': all_data}
			return HttpResponse(json.dumps(res))
				
		exist_cache = cache.get(folderID)
		if not exist_cache:
			res = {'code': -1, 'msg': '数据不存在', 'data': {}}
		else:
			res = {'code': 0, 'msg': 'success', 'data': {folderID: exist_cache}}

	except Exception as e:
		res = {'code': 500, 'msg': 'server error', 'data': {}}
		traceback.print_exc()

	return HttpResponse(json.dumps(res))

# 清除指定文件的cache
@csrf_exempt
def clearCache(request):
	request.encoding = 'utf-8'
	res = {'code': 0, 'msg': 'success', 'data': {}}
	try:
		folderID = request.POST['folderID']

		if str(folderID) == 'all':
			cache.clear()
			res = {'code': 0, 'msg': '数据清空成功', 'data': {}}
			return HttpResponse(json.dumps(res))
		
		exist_cache = cache.get(folderID)
		if not exist_cache:
			res = {'code': -1, 'msg': '数据不存在', 'data': {}}
		else:
			cache.delete(folderID)
			res = {'code': 0, 'msg': '数据删除成功', 'data': {}}

	except Exception as e:
		res = {'code': 500, 'msg': 'server error', 'data': {}}
		traceback.print_exc()

	return HttpResponse(json.dumps(res))

# 获取指定题目的所有信息
@csrf_exempt
def getInfo(request):
	request.encoding = 'utf-8'
	res = {'code': 0, 'msg': 'success', 'data': {}}
	try:
		folderID = request.POST['folderID']
		filepath = os.path.join(settings.FILE_PATH, folderID)

		if not os.path.exists(filepath):
			res = {'code': -1, 'msg': '解压文件不存在', 'data': {}}
			return HttpResponse(json.dumps(res))
		
		exist_cache = cache.get(folderID)
		exist_cache = serveView.statusJudge(exist_cache)
		filepath = os.path.join(settings.FILE_PATH, folderID)
		if not exist_cache:
			exist_cache = serveView.saveRedis(filepath, folderID)	
		exist_cache['answer'] = getAnswer(filepath)
		cache.set(folderID, exist_cache)
		res = {'code': 0, 'msg': 'success', 'data': exist_cache}

	except Exception as e:
		res = {'code': 500, 'msg': 'server error', 'data': {}}
		traceback.print_exc()

	return HttpResponse(json.dumps(res))