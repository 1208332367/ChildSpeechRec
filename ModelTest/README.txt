1.依赖环境安装
pip install -r requirements.txt

2. 执行统计脚本
python analyze.py

3. 权值矩阵选择
修改SpeechJudge.py/line15~16

v0：权值均为1
v1：权值包括0.5、1.5
v2：其他
