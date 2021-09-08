from json import encoder
import os, xlrd, csv, json, re
import Levenshtein
from xpinyin import Pinyin
from likelyMat import likelyMat

root = os.getcwd()
srcFolder = os.path.join(root, '工作进展', '识别统计')
dstData = os.path.join(root, '工作进展', '识别统计', 'FinalJudge_All.csv')
errData = os.path.join(root, '工作进展', '识别错误音频.csv')
pinyin = Pinyin()  

class judge:
    def __init__(self, threshold=1.0, disType='single', ones=0.35, zeros=0.35, writeErr=False):
        self.threshold = threshold  #平均编辑距离阈值
        self.writeErr = writeErr
        p = likelyMat()
        self.sheng = p.getMat('声母距离权值矩阵v2.xlsx', 'sheng')
        self.yun = p.getMat('韵母距离权值矩阵v2.xlsx', 'yun')
        self.disType = disType
        self.allDistance = []
        self.allDataRows = []
        self.ones = ones
        self.zeros = zeros

        #print(self.sheng)
        #print(self.yun)

    def unitStandard(self, row, start=4, end=9):
        for i in range(start, end):
            if row[i] == '是':
                row[i] = 1
            if row[i] == '否' or row[i] == '':
                row[i] = 0
        return row

    def judgeAll(self):
        fileList = os.listdir(srcFolder)
        for file in fileList:
            if file.endswith('ModelTest_All.csv'):
                self.processTable(file)
                #print(file + ' ok')
                #break #执行一次

        self.divideAllDistance()
        self.writeCsv()
        if self.writeErr:
            self.writeError()

    def writeError(self):
        f = open(errData, 'w', encoding='utf-8', newline='')
        f_read = open(dstData, 'r', encoding='utf-8')
        csvRead = csv.reader(f_read, delimiter = ',')
        next(csvRead)

        csvWrite = csv.writer(f, dialect='excel')
        csvWrite.writerow(self.csvHead)
        total = 0
        err = 0
        for item in csvRead:
            # print(item)
            if item[13] == '-1' or item[7] == '0' or item[7] == '':
                continue

            if item[15] == '0':
                total += 1
                if item[14] != item[8]:
                    err += 1
                    csvWrite.writerow(item)

        # print('err %d' %err + ' / %d' %total)
        f_read.close()
        f.close()

    def writeCsv(self):
        f = open(dstData, 'w', encoding='utf-8', newline='')
        csvWrite = csv.writer(f, dialect='excel')
        self.csvHead.append('标准拼音')
        self.csvHead.append('讯飞数据')
        self.csvHead.append('讯飞判定(单threshold)')
        self.csvHead.append('讯飞判定(threshold区间)')
        self.csvHead.append('是否需要人工判断')

        csvWrite.writerow(self.csvHead)

        for item in self.allDataRows:
            row = item
            if item[13] == -1:
                row.append(-1)
                row.append(-1)
            else:
                res = self.judgeByTwoDis(row[12]['minDis'])
                row.append(res['xunfeiJudge'])
                row.append(res['needHuman'])

            csvWrite.writerow(row)

        f.close()

    def judgeByTwoDis(self, dis):
        res = {}
        if dis == 0:
            res['xunfeiJudge'] = 1
            res['needHuman'] = 0
            return res
        if dis < self.divideDis['start']:
            res['xunfeiJudge'] = 1
            res['needHuman'] = 0
            return res
        if dis >= self.divideDis['end']:
            res['xunfeiJudge'] = 0
            res['needHuman'] = 0
            return res
        res['xunfeiJudge'] = ''
        res['needHuman'] = 1
        return res

    def divideAllDistance(self):
        disList = self.allDistance
        disList.sort()
        n = len(disList)
        # print(n)
        startIndex = int(self.ones * n)
        # print(startIndex)
        endIndex = int((1 - self.zeros) * n)
        if startIndex == n:
            startIndex = n - 1
        if endIndex == n:
            endIndex = n - 1
        # print(endIndex)
        start = disList[startIndex]
        end = disList[endIndex]

        if startIndex >= 1 and startIndex <= n - 2 and n >= 3:
            start = (disList[startIndex - 1] + disList[startIndex] + disList[startIndex + 1]) / 3
        if endIndex >= 1 and endIndex <= n - 2 and n >= 3:
            end = (disList[endIndex - 1] + disList[endIndex] + disList[endIndex + 1]) / 3

        self.divideDis = {
            'start': start,
            'end': end
        }
        # print(self.divideDis)
        # print(self.allDistance)

    def getDivideDis(self):
        return self.divideDis

    def processTable(self, file):
        #优质音频
        '''
        dstData = os.path.join(srcFolder, file.replace("ModelTest_All.csv", "FinalJudge_All.csv"))
        #print(os.path.join(srcFolder, file))
        fin = open(os.path.join(srcFolder, file), 'r', encoding='utf-8-sig')
        csvRead = csv.reader(fin, delimiter = ',')
        head = next(csvRead)
        head.append('标准拼音')
        head.append('讯飞数据')
        head.append('讯飞判定(单threshold)')

        newtable = open(dstData, 'w', encoding='utf-8', newline='')
        csvWrite = csv.writer(newtable, dialect='excel')
        csvWrite.writerow(head)
        '''
        fin = open(os.path.join(srcFolder, file), 'r', encoding='utf-8-sig')
        csvRead = csv.reader(fin, delimiter = ',')
        self.csvHead = next(csvRead)

        index = 0

        for row in csvRead:    
            index += 1
            row = self.unitStandard(row)
            answerList = row[1].strip().split('、')
            pinyinAnswerList = list(map(lambda x: pinyin.get_pinyin(x), answerList))
            row.append(pinyinAnswerList)     
            # print(row)
            #讯飞
            # print(type(pinyinAnswerList))
            res = self.getSingleRec(pinyinAnswerList, row[9], row[10], 0)
            # row.append(json.dumps(res['data']))
            row.append(res['data'])
            row.append(res['label'])

            self.allDataRows.append(row)
            
            #csvWrite.writerow(row)
            
            #if index == 3:
            #    break #执行3次

        #newtable.close()

    def getSingleRec(self, pinyinAnswerList, word, pinyin, hasTone=0):
        res = {}
        #res['data'] = {'word': '', 'pinyin': '', 'nearest': '', 'minDis': -1}
        res['data'] = {}
        res['label'] = -1

        min = 999999
        if word is None or pinyin is None or '-' in word or '-' in pinyin:
            return res
        if not re.search('[a-zA-Z]', pinyin):
            return res
        res['data']['word'] = word
        res['data']['pinyin'] = pinyin
        pinyin = pinyin.replace("'", '"')
    
        finalList = []
        for pinyinAnswer in pinyinAnswerList:
            standardList = pinyinAnswer.strip().split('-')
            if '' in standardList:
                standardList.remove('')
            targetList = json.loads(pinyin)
            targetList = list(map(lambda x: x[0: (len(x) - hasTone)], targetList))
            if '' in targetList:
                targetList.remove('')
            #print(standardList)
            #print(targetList)
            #print('......')
            len1 = len(standardList)
            len2 = len(targetList)
            if len1 > len2 or len1 == 0 or len2 == 0:
                return res
            for i in range(0, len2 - len1 + 1):
                if self.disType == 'single':
                    score = self.simpleCompare(standardList, targetList[i: i + len1])
                if self.disType == 'complex':
                    score = self.complexCompare(standardList, targetList[i: i + len1])

                if score < min:
                    min = score
                    finalList = targetList[i: i + len1]
            
            res['data']['nearest'] = finalList  #拼音最近匹配
            res['data']['minDis'] = min         #最小编辑距离均值

            if min < self.threshold:                #距离小于阈值，则判定为正确
                res['label'] = 1                
            else:
                res['label'] = 0
            
            self.allDistance.append(min)

        return res

    #比较两个字符串列表的编辑距离均值，如['gu', 'tou']和['tou', 'tu']
    def simpleCompare(self, list1, list2):
        #print(list1)
        #print(list2)
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
            '''
            newstr1 = newstr1.replace('ing', 'in')
            newstr1 = newstr1.replace('eng', 'en')
            newstr1 = newstr1.replace('zh', 'z')
            newstr1 = newstr1.replace('ch', 'c')
            newstr1 = newstr1.replace('sh', 's')
            newstr2 = newstr2.replace('ing', 'in')
            newstr2 = newstr2.replace('eng', 'en')
            newstr2 = newstr2.replace('zh', 'z')
            newstr2 = newstr2.replace('ch', 'c')
            newstr2 = newstr2.replace('sh', 's')
            '''
            
            res1 = self.dividePinyin(newstr1)
            res2 = self.dividePinyin(newstr2)
            #print(res1)
            #print(res2)
            if res1['sheng'] == '' or res2['sheng'] == '':
                disSheng = Levenshtein.distance(res1['sheng'], res2['sheng'])
            else:
                disSheng = self.sheng[res1['sheng']][res2['sheng']] * Levenshtein.distance(res1['sheng'], res2['sheng'])
            disYun = self.yun[res1['yun']][res2['yun']] * Levenshtein.distance(res1['yun'], res2['yun'])
            #print(disSheng)
            #print(disYun)

            score = score + disSheng + disYun

            '''
            #添加惩罚机制
            if disSheng == 0 or disYun == 0:
                score = score + disSheng + disYun
            else:
                score = score + 1.5 * (disSheng + disYun)
            '''
        
        #print(score / len(list1))
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
    
if __name__ == '__main__':
    p = judge(1.5, 'complex')
    p.judgeAll()
    #print(p.dividePinyin('qin'))
