import os, time, random
from SpeechRec import celery_app
from celery import platforms
from recognize import views as recViews
platforms.C_FORCE_ROOT = True

@celery_app.task
def xunfei_background(folderID, filepath, exist_cache):
    print(str(folderID) + ' 讯飞识别开始')
    if not exist_cache:
        return
    for wavID, value in exist_cache['wav'].items():
        wav_path = os.path.join(filepath, 'wav', wavID + '.wav')
        for try_times in range(3):
            if exist_cache['wav'][wavID]['errcode'] >= 0 and exist_cache['wav'][wavID]['errcode'] != 500:
                break
            exist_cache = recViews.getXunfeiResult(folderID, exist_cache, wavID, wav_path)
            print(str(wavID) + ' try_times: ' + str(try_times + 1))
            time.sleep(random.randint(1, 3))
    print(str(folderID) + ' 讯飞识别结束')
    return
