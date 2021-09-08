import os, xlrd
from SpeechRec import settings

srcTable = os.path.join(settings.STATIC_ROOT, 'disWeightMat')

class likelyMat:
    def __init__(self):
        self.mat = { 
            'sheng': { 
                'b':{}, 'p':{}, 'm':{}, 'f':{}, 'd':{}, 't':{}, 
                'n':{}, 'l':{}, 'g':{}, 'k':{}, 'h':{}, 'j':{}, 
                'q':{}, 'x':{}, 'r':{}, 'z':{}, 'c':{}, 's':{}, 
                'y':{}, 'w':{}, 'zh':{}, 'ch':{}, 'sh':{} 
            }, 
            'yun':{ 
                'a':{}, 'e':{}, 'i':{}, 'o':{}, 'u':{}, 'v':{}, 
                'ai':{}, 'ao':{}, 'an':{}, 'ang':{}, 
                'ou':{}, 'ong':{}, 
                'ei':{}, 'er':{}, 'en':{}, 'eng':{}, 
                'iu':{}, 'ie':{}, 'in':{}, 'ing':{}, 'ia':{}, 'iao':{}, 'ian':{}, 'iang':{}, 'iong':{}, 
                'ui':{}, 'un':{}, 'ua':{}, 'uai':{}, 'uan':{}, 'uang':{}, 'uo':{}, 'ue':{}, 
            }
        }
    
    def getMat(self, filename, matType='sheng'):
        file = os.path.join(srcTable, filename)
        wb = xlrd.open_workbook(file)
        sh = wb.sheet_by_name('Sheet1')
        for i in range(1, sh.nrows):
            for j in range(1, sh.ncols):
                x = sh.cell(i, 0).value
                y = sh.cell(0, j).value
                if sh.cell(i, j).value == '':
                    self.mat[matType][x][y] = 1
                else:
                    self.mat[matType][x][y] = sh.cell(i, j).value
        
        return self.mat[matType]

if __name__ == '__main__':
    p = likelyMat()
    print(p.getMat('sheng_v0.xlsx', 'sheng'))
    print(p.getMat('yun_v0.xlsx', 'yun'))

    