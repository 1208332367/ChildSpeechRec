import re
import Levenshtein 
import os, csv
from recognize import likelyMat
from SpeechRec import settings

srcTable = os.path.join(settings.STATIC_ROOT, 'partPercent.csv')

class judge:
    def __init__(self, disType='single', human=0.3):
        mat = likelyMat.likelyMat()
        self.sheng = mat.getMat('sheng_v2.xlsx', 'sheng')
        self.yun = mat.getMat('yun_v2.xlsx', 'yun')
        self.disType = disType
        self.getThres(human)
 
    def getThres(self, human):
        f = open(srcTable, 'r', encoding='utf-8')
        csvReader = csv.reader(f, delimiter = ',')
        next(csvReader)
        thres = {}
        for item in csvReader:
            thres[item[0]] = {
                'left': item[7],
                'right': item[8]
            }
        self.left_thres = float(thres[str(human)]['left'])
        self.right_thres = float(thres[str(human)]['right'])
        #print('left: ' + str(self.left_thres))
        #print('right: ' + str(self.right_thres))

    def getAllJudge(self, exist_cache):
        pinyinAnswerList = exist_cache['answer']['pinyin_list']
        exist_cache['hasJudge'] = 1
        for wavID, value in exist_cache['wav'].items():
            if exist_cache['wav'][wavID]['errcode'] != 0:
                exist_cache['wav'][wavID]['judge'] = -1
                continue
            res = self.getSingleJudge(pinyinAnswerList, value['xunfei_pinyin'])
            exist_cache['wav'][wavID]['nearest'] = res['nearest']
            exist_cache['wav'][wavID]['min_dis'] = res['min_dis']
            exist_cache['wav'][wavID]['need_human'] = res['need_human']
            exist_cache['wav'][wavID]['judge'] = res['judge']
        return exist_cache

    def getSingleJudge(self, pinyinAnswerList, pinyin):
        res = {'nearest': None, 'min_dis': None, 'need_human': None, 'judge': -1}
        finalList = []
        min = 999999

        if not pinyin:
            return res

        if not re.search('[a-zA-Z]', str(pinyin)):
            return res
        if '' in pinyin:
            pinyin.remove('')
        len2 = len(pinyin)

        for pinyinAnswer in pinyinAnswerList:
            standardList = pinyinAnswer.strip().split('-')
            if '' in standardList:
                standardList.remove('')
            len1 = len(standardList)
            
            if len1 > len2 or len1 == 0 or len2 == 0:
                continue
            for i in range(0, len2 - len1 + 1):
                if self.disType == 'single':
                    score = self.simpleCompare(standardList, pinyin[i: i + len1])
                if self.disType == 'complex':
                    score = self.complexCompare(standardList, pinyin[i: i + len1])
                if score < min:
                    min = score
                    finalList = pinyin[i: i + len1]
            
        res['nearest'] = finalList  #拼音最近匹配
        res['min_dis'] = min         #最小编辑距离均值

        judge = self.judgeByTwoDis(min)
        res['need_human'] = judge['need_human']
        res['judge'] = judge['judge']

        return res

    def judgeByTwoDis(self, dis):
        res = {}
        if dis == 0:
            res['judge'] = 1
            res['need_human'] = 0
            return res
        if dis < self.left_thres:
            res['judge'] = 1
            res['need_human'] = 0
            return res
        if dis >= self.right_thres:
            res['judge'] = 0
            res['need_human'] = 0
            return res
        res['judge'] = -1
        res['need_human'] = 1

        return res

    #比较两个字符串列表的编辑距离均值，如['gu', 'tou']和['tou', 'tu']
    def simpleCompare(self, list1, list2):
        score = 0
        for i in range(0, len(list1)):
            score += Levenshtein.distance(list1[i], list2[i])
        return score / len(list1)  

    #距离分为声母、韵母，分别求 权值 * 编辑距离
    def complexCompare(self, list1, list2):
        score = 0
        for i in range(0, len(list1)):
            newstr1 = list1[i]
            newstr2 = list2[i]
            
            res1 = self.dividePinyin(newstr1)
            res2 = self.dividePinyin(newstr2)

            if res1['sheng'] == '' or res2['sheng'] == '':
                disSheng = Levenshtein.distance(res1['sheng'], res2['sheng'])
            else:
                disSheng = self.sheng[res1['sheng']][res2['sheng']] * Levenshtein.distance(res1['sheng'], res2['sheng'])
            disYun = self.yun[res1['yun']][res2['yun']] * Levenshtein.distance(res1['yun'], res2['yun'])

            score = score + disSheng + disYun
        
        return score / len(list1)
    
    #寻找拼音中的第一个元音字母（包括v）
    def getFirstYuanyinPos(self, pinyin):
        yuanyinList = ['a', 'e', 'i', 'o', 'u', 'v']
        for i in range(0, len(pinyin)):
            ch = pinyin[i]
            if ch in yuanyinList:
                return i
        return -1
    
    #分离拼音的声母和韵母
    def dividePinyin(self, pinyin):
        res = {'sheng': '', 'yun': ''}
        pos = self.getFirstYuanyinPos(pinyin)
        if pos < 0:
            return res
        if pos == 0:
            res['sheng'] = ''
        else:
            res['sheng'] = pinyin[0: pos]
        res['yun'] = pinyin[pos: len(pinyin)]
        return res