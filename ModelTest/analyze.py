import os, csv
from re import escape
import numpy as np
from SpeechJudge import judge
import matplotlib.pyplot as plt

root = os.getcwd()
srcTable = os.path.join(root, '工作进展', '识别统计')
dstData = os.path.join(root, '工作进展', '正确率统计.csv')

class Analyze:
    def __init__(self):
        self.initial_reset('singleThres')

    def initial_reset(self, judgeType='singleThres'):
        self.judgeType = judgeType

        self.threshold = 0
        self.divideDis = {
            'start': 0,
            'end': 0
        }

        self.total = 0
        self.useful = 0
        self.highQ = 0
        self.best = {
            'single': {
                'all': {
                    'accuracy': {'thres': 0, 'thres_start': 0, 'thres_end': 0, 'value': 0}, 
                    'precision': {'thres': 0, 'thres_start': 0, 'thres_end': 0, 'value': 0}, 
                    'recall': {'thres': 0, 'thres_start': 0, 'thres_end': 0, 'value': 0}, 
                    'F1': {'thres': 0, 'thres_start': 0, 'thres_end': 0, 'value': 0} 
                }, 
                'highQ': {
                    'accuracy': {'thres': 0, 'thres_start': 0, 'thres_end': 0, 'value': 0}, 
                    'precision': {'thres': 0, 'thres_start': 0, 'thres_end': 0, 'value': 0}, 
                    'recall': {'thres': 0, 'thres_start': 0, 'thres_end': 0, 'value': 0}, 
                    'F1': {'thres': 0, 'thres_start': 0, 'thres_end': 0, 'value': 0} 
                } 
            }, 
            'complex': {
                'all': {
                    'accuracy': {'thres': 0, 'thres_start': 0, 'thres_end': 0, 'value': 0}, 
                    'precision': {'thres': 0, 'thres_start': 0, 'thres_end': 0, 'value': 0}, 
                    'recall': {'thres': 0, 'thres_start': 0, 'thres_end': 0, 'value': 0}, 
                    'F1': {'thres': 0, 'thres_start': 0, 'thres_end': 0, 'value': 0} 
                }, 
                'highQ': {
                    'accuracy': {'thres': 0, 'thres_start': 0, 'thres_end': 0, 'value': 0}, 
                    'precision': {'thres': 0, 'thres_start': 0, 'thres_end': 0, 'value': 0}, 
                    'recall': {'thres': 0, 'thres_start': 0, 'thres_end': 0, 'value': 0}, 
                    'F1': {'thres': 0, 'thres_start': 0, 'thres_end': 0, 'value': 0} 
                } 
            }
        }
        self.x = []
        self.y = {
            'single': {
                'all':{'accuracy': [], 'precision': [], 'recall': [], 'F1': []}, 
                'highQ': {'accuracy': [], 'precision': [], 'recall': [], 'F1': []} 
            }, 
            'complex': {
                'all':{'accuracy': [], 'precision': [], 'recall': [], 'F1': []} , 
                'highQ': {'accuracy': [], 'precision': [], 'recall': [], 'F1': []} 
            } 
        }
        
        self.reset()

    def reset(self):  
        self.Y_prediction_train = []
        self.Y_train = []
        self.acc = {}
        
    def analyzeOneThreshold(self, disType='single', ones=0.35, zeros=0.35, writeErr=True):
        p = judge(self.threshold, disType, ones=ones, zeros=zeros, writeErr=writeErr)
        p.judgeAll()

        self.divideDis = p.getDivideDis()

        self.analyzeOneQuality(disType, 1)
        self.analyzeOneQuality(disType, 4)
    
    def analyzeOneQuality(self, disType='single', minQuality=1):
        self.reset()
        quantity = self.getData(minQuality)
        self.total = quantity['total']
        self.getAcc()

        quality = 'all'
        if minQuality >= 4:
            quality = 'highQ'
            self.highQ = quantity['useful']
        else:
            self.useful = quantity['useful']
     
        self.addAccToVec(disType, quality, 'accuracy')
        self.addAccToVec(disType, quality, 'precision')
        self.addAccToVec(disType, quality, 'recall')
        self.addAccToVec(disType, quality, 'F1')
        
    def addAccToVec(self, disType='single', quality='all', accType='accuracy'):
        self.y[disType][quality][accType].append(self.acc[accType])
        if self.acc[accType] > self.best[disType][quality][accType]['value']:
            self.best[disType][quality][accType]['value'] = self.acc[accType]
            if self.judgeType == 'singleThres':
                self.best[disType][quality][accType]['thres'] = self.threshold
            else:
                self.best[disType][quality][accType]['thres_start'] = self.divideDis['start']
                self.best[disType][quality][accType]['thres_end'] = self.divideDis['end']

    def showBest(self, disType='single', quality='all', accType='accuracy'):
        if self.judgeType == 'singleThres':
            print('[' + disType + '] threshold: ' + '%.2f' % self.best[disType][quality][accType]['thres'] + ' , ' + accType + ': ' + '%.2f' % (100 * self.best[disType][quality][accType]['value']) + '%')
        else:
            print('[' + disType + '] threshold: ' + '[%.2f, ' % self.best[disType][quality][accType]['thres_start'] + '%.2f]' % self.best[disType][quality][accType]['thres_end'] + ' , ' + accType + ': ' + '%.2f' % (100 * self.best[disType][quality][accType]['value']) + '%')

    def oneThresSolve(self):
        step = 0.05
        end = 3.0

        while True:
            if self.threshold > end:
                break
            self.threshold += step
            self.x.append(self.threshold)

            self.analyzeOneThreshold('single')
            self.analyzeOneThreshold('complex')      
            
            percent = int(self.threshold / end * 100)
            if percent % 20 == 0:
                print(str(percent) + '% ok')
        
        self.showAndDrawAll()
    
    def showAndDrawAll(self):
        print('---------All Data Best Performance---------')
        '''
        self.showBest('single', 'all', 'accuracy')
        self.showBest('complex', 'all', 'accuracy')
        print('\n')
        '''
        
        #self.showBest('single', 'all', 'F1')
        self.showBest('complex', 'all', 'accuracy')
        self.showBest('complex', 'all', 'F1')
        print('\n')

        '''
        print('---------HighQ Data Best Performance---------')
        self.showBest('single', 'highQ', 'accuracy')
        self.showBest('complex', 'highQ', 'accuracy')
        print('\n')
        self.showBest('single', 'highQ', 'F1')
        self.showBest('complex', 'highQ', 'F1')
        print('\n')
        '''

        ax1 = plt.subplot(4, 1, 1)
        ax2 = plt.subplot(4, 1, 2)
        ax3 = plt.subplot(4, 1, 3)
        ax4 = plt.subplot(4, 1, 4)
        
        plt.sca(ax1)
        plt.plot(self.x, self.y['single']['all']['accuracy'], label='[single] Useful Data(' + str(self.useful) + '/' + str(self.total) + ') Accuracy')
        plt.plot(self.x, self.y['complex']['all']['accuracy'], label='[complex] Useful Data(' + str(self.useful) + '/' + str(self.total) + ') Accuracy')
        plt.legend()

        plt.sca(ax2)
        plt.plot(self.x, self.y['single']['all']['F1'], label='[single] Useful Data(' + str(self.useful) + '/' + str(self.total) + ') F1')
        plt.plot(self.x, self.y['complex']['all']['F1'], label='[complex] Useful Data(' + str(self.useful) + '/' + str(self.total) + ') F1')
        plt.legend()

        plt.sca(ax3)
        plt.plot(self.x, self.y['single']['highQ']['accuracy'], label='[single] highQ Data(' + str(self.highQ) + '/' + str(self.total) + ') Accuracy')
        plt.plot(self.x, self.y['complex']['highQ']['accuracy'], label='[complex] highQ Data(' + str(self.highQ) + '/' + str(self.total) + ') Accuracy')
        plt.legend()

        plt.sca(ax4)
        plt.plot(self.x, self.y['single']['highQ']['F1'], label='[single] highQ Data(' + str(self.highQ) + '/' + str(self.total) + ') F1')
        plt.plot(self.x, self.y['complex']['highQ']['F1'], label='[complex] highQ Data(' + str(self.highQ) + '/' + str(self.total) + ') F1')
        plt.legend()

        plt.show()

    def getAcc(self):
        Add_train = np.array(self.Y_prediction_train) + np.array(self.Y_train)
        Sub_train = np.array(self.Y_prediction_train) - np.array(self.Y_train)
    
        TP = np.sum(np.where(Add_train==2,1,0))
        TN = np.sum(np.where(Add_train==0,1,0))
        FP = np.sum(np.where(Sub_train==1,1,0))
        FN = np.sum(np.where(Sub_train==-1,1,0))

        res = {}
        res['accuracy']  = (TP + TN) / (TP + TN + FP + FN)  #所有样本中，预测正确（1-1，0-0）的比例
        if TP + FP == 0:
            res['precision'] = 0
        else:
            res['precision']  = TP / (TP + FP)   #在所有预测为1的样本中，样本确实为1的比例
        if TP + FN == 0:
            res['recall'] = 0
        else:
            res['recall']  = TP / (TP + FN)    #在所有确实为1的样本中，预测为1的比例
        if res['precision'] + res['recall'] == 0:
            res['F1'] = 0
        else:
            res['F1']  = 2 * res['precision'] * res['recall'] / (res['precision'] + res['recall'])    #precision和recall的调和均值

        self.acc = res


    def write(self):
        newtable = open(dstData, 'w', encoding='utf-8', newline='')
        csvWrite = csv.writer(newtable, dialect='excel')
        total = self.total
        useful = self.useful
        acc = self.acc

        csvWrite.writerow(['有效数据', '讯飞准确率', '讯飞精准率', '讯飞召回率'])
        csvWrite.writerow([str(useful) + ' / ' + str(total), acc['accuracy'], acc['precision'], acc['recall']])

        newtable.close()

    def getData(self, minQuality):
        quantity = {'total': 0, 'useful': 0}
        file = os.path.join(srcTable, 'FinalJudge_All.csv')

        fin = open(file, 'r', encoding='utf-8-sig')
        csvRead = csv.reader(fin, delimiter = ',')
        next(csvRead)

        for row in csvRead:    
            if '-' in row[2]:
                continue
            quantity['total'] += 1

            if row[7] == '':
                continue
            if int(row[7]) == 0:
                continue
            if int(row[13]) == -1:
                continue

            if int(row[7]) >= minQuality:
                
                if self.judgeType == 'singleThres':
                    quantity['useful'] += 1
                    self.Y_train.append(int(row[8]))
                    self.Y_prediction_train.append(int(row[13]))
                else:
                    if int(row[15]) == 0:
                        quantity['useful'] += 1
                        self.Y_train.append(int(row[8]))
                        self.Y_prediction_train.append(int(row[14]))

        fin.close()

        return quantity
    
    def twoThresSolve(self, human=0.3, start=0, end=0, step=0.02):     
        if human > 0.7:
            print("人的参与度必须介于[0, 0.7]")
            return -1
        
        if start > end:
            print("请设置 start <= end")
            return -2
        
        if step < 0.01:
            print("请设置 step >= 0.01")
            return -3
        
        if step > 0.1:
            print("请设置 step <= 0.1")
            return -4

        self.initial_reset('doubleThres')

        while True:
            ones = start
            zeros = 1 - human - ones
            
            if zeros <= 0.01:
                break    

            self.x.append(ones)            
            self.analyzeOneThreshold('single', ones=ones, zeros=zeros)
            self.analyzeOneThreshold('complex', ones=ones, zeros=zeros, writeErr=True)  

            print("ones: %.2f" % ones + " , zeros: %.2f" % zeros + ' , start: %.2f' % self.divideDis['start'] + ' , end: %.2f' % self.divideDis['end'])

            start += step
            if start > end:
                break
        
        self.showAndDrawAll()
        return 0

#[0, 0, 1.0, 1.0, ……, 4.0, 4.0]

if __name__ == '__main__':
    p = Analyze()
    #p.oneThresSolve()
    p.twoThresSolve(human=0.3, start=0.42, end=0.42, step=0.02)

