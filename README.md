# py2sec

[English Readme](https://github.com/cckuailong/py2sec/blob/master/README_en.md)

## 系统支持

Linux && MacOS && Windows

注意：Windows用户运行时可能会遇到如下错误

```
error: command 'cl.exe' failed: No such file or directory
```

请安装对应Win系统版本的Visual C++ Build Tools

## py2sec简介

1. py2sec是一款跨平台，快速敏捷的 python文件加密工具，可以将.py加密成.so(Linux && Mac)，或.pyd(Win)文件
2. py2sec可以用来加密python文件或项目
3. py2sec加密一个py文件，也可以直接加密一整个python项目
4. .py生成的.so（.pyd）文件可以被主文件通过 "from module import * " 调用
5. py2sec可以自动识别项目中的py文件, 如果项目中某些文件你不想加密，py2sec也可以实现你的目的
6. py2sec不影响源文件，加密后的文件或项目将被存放在新的路径
7. py2sec 支持 python2 and python3, 请使用 -p(--py)来切换要加密的代码的python版本
8. 支持多线程加密，加密文件较多时，速度提升明显

## 环境配置

```
pip install requirements.txt
```

## 使用说明

### 使用

```
python py2sec.py [选项] ...
```

### 选项

```
-v,  --version    显示py2sec_py3版本
-h,  --help       显示帮助菜单
-p,  --py         Python的版本, 默认值为 3
                  例: -p 3  (比如你使用python3)
-d,  --directory  Python项目路径 (如果使用-d参数, 将加密整个Python项目)
-f,  --file       Python文件 (如果使用-f, 将加密单个Python文件)
-m,  --maintain   标记你不想加密的文件或文件夹路径
                  注意: 文件夹路径需要使用'[]'包起来, 并且需要和-d参数一起使用 
                  例: -m __init__.py,setup.py,[poc,resource,venv,interface]
-x  --nthread     加密启用的线程数
```

```
python py2sec.py -f test.py
python py2sec.py -f example/test1.py
python py2sec.py -d example/ -m test1.py,[bbb/]
```

### 项目结构

- build/              临时文件夹, .o, .so 文件
- tmp_build/          临时文件夹, .c 文件
- result/             加密最终结果存放目录
- result/log.txt      加密日志
- py2sec.py           主函数文件
- setup.py.template   用于生成setup.py的模板文件
- requirements.txt    需要的环境

### 示例

整个Python项目加密前:

![demo1](https://github.com/cckuailong/py2sec/blob/master/img/1.png)

py2sec加密后效果:

![demo2](https://github.com/cckuailong/py2sec/blob/master/img/2.png)
