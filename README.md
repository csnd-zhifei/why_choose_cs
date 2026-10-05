# CS-为啥选
“你为什么选择CS？”这是一个给CS学生、结合各自经历、分享CS思考、看法、观点的Web项目。旨在提供用户浏览与分享关于CS的思考。项目基于FastAPI、Vue、MySQL、ORM。

## 安装依赖项
- python 3.12
- pip

### 步骤
>建议使用虚拟环境
```txt
可以使用python自带的python3.12 -m venv venv
也可以使用uv, uv venv --python 3.12，之后使用uv pip install即可
创建完成后，记得激活虚拟环境
```

```bash
git clone <https://本项目链接/.git>
cd ...
pip install -r requirements.txt
```

>如果速度慢，可以使用镜像源加速下载，临时生效（powershell）
```bash
$env:UV_INDEX_URL="https://pypi.tuna.tsinghua.edu.cn/simple"
uv pip install -r requirements.txt
```

## 使用方法
使用linux系统
```bash
start.sh
```
使用window系统
```bash
start.bat
```

##项目结构
```
why_choose_cs
├─backend/
| ├─models/    #数据库模型     
| ├─routers/   #路由
| ├─services/  #业务函数，CRUD
| ├─config.py  #读取.env，以及其他配置项
| └─main.py
├─src/         #前端
├─.requirements.txt
├─.env         #api 密钥
└─start.bat    #项目启动（windows）
```