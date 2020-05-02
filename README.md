# MindMapping
使用此工具，将平时积累的笔记一键转化为思维导图
## 1. 环境配置
&emsp;&emsp;本系统在Win10系统环境下进行开发，使用编程语言为Python=3.7.1，Python的具体环境如下:  

1. PyQt5=5.13.0进行用户界面的开发
2. Graphviz=0.13.2进行思维导图的设计
3. baidu-aip=2.2.18.0， 连接百度云智能平台创建的OCR API，进行高精度的图像文本识别
## 2. 代码目录说明
代码目录结构如下:  
```
thoughtmap
        |——main.py
        |——MainWindow.py
        |——Baidu.py
        |——icon
             |——Map.png
             |——......
             |——Exit.png
```
其中main.py为系统调用入口，在main.py所在路径下调用`python main.py`命令即可运行系统。  
MainWindow.py定义了MainWindow类，其集成了用户界面与文本分析、绘制思维导图等功能。  
BaiduOCR.py调用百度云智能的图像文本识别应用，实现了高精度的图像文本识别功能。  
icon文件夹下存放了用户主页面的图形图标。
## 3. 使用说明
### 3.1 笔记输入
&emsp;&emsp;考虑到笔记可为电子版和纸质版两种，输入笔记的格式可为txt文本文档或者图片格式。要注意，若是输入文本文档，则可选择一个文件输入，若是输入图片格式的笔记，可选择多个图片。
&emsp;&emsp;此软件根据开发者本人记笔记的习惯设计，对输入的笔记只有一个要求——按照以下格式组织，有无缩进对结果无影响。

```
题目
1. xxx
1.1 xxx
1.1.1 xxx
1.1.2 xxx
1.2 xxx
2. xxx
……
```
## 4. 界面说明
程序运行界面包括文件选择模块、普通属性选择模块、高级属性选择模型、绘图与输出模块。
![](https://github.com/yx3266/MindMapping/blob/master/images/interface.PNG)