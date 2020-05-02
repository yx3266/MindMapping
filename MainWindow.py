from PyQt5.QtCore import Qt,pyqtSignal
from PyQt5.QtGui import QColor, QFont, QIcon
from PyQt5.QtWidgets import *
from scapy.all import *
import sys, time, copy, os
from graphviz import Graph, Digraph
import BaiduOCR

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        #全局变量
        self.TypeGraph_List = ["Graph", "Digraph"]
        self.TypeEngine_List = ["dot", "neato", "fdp", "sfdp", "twopi", "circo"]
        self.FontSize_List = [2.0, 4.0, 6.0, 8.0, 10.0, 12.0, 14.0, 16.0, 18.0, 20.0, 22.0, 24.0, 26.0, 28.0, 30.0]
        self.TypeEdge_List = ["solid", "dashed", "dotted", "bold"]
        self.TypeTree_List = ["LR", "TB"]
        self.TypeTree_ListChange = ["水平", "竖直"]
        self.TypeFace_List = ["SimHei", "SimSun", "Kaiti", "Times-Roman", "Microsoft YaHei", "FangSong", "Microsoft JHengHei"]
        self.TypeFace_ListChange = ["黑体", "宋体", "楷体", "Times-Roman", "微软雅黑", "仿宋", "微软正黑体"]
        self.TypeBbox_List = ["none", "box", "ellipse", "underline", "rarrow", "circle", "cds"]
        self.TypeBbox_ListChange = ["无", "矩形", "椭圆形", "下划线", "箭头", "圆形", "标签"]
        self.CharColor_List = ["Black", "Red", "Yellow", "Blue", "Brown", "Purple", "Orange"]
        self.CharColor_ListChange = ["黑色", "红色", "黄色", "蓝色", "棕色", "紫色", "橘黄色"]
        self.BboxColor_List = ["Black", "Red", "Yellow", "Blue", "Brown", "Purple", "Orange"]
        self.BboxColor_ListChange = ["黑色", "红色", "黄色", "蓝色", "棕色", "紫色", "橘黄色"]
        self.EdgeColor_List = ["Black", "Red", "Yellow", "Blue", "Brown", "Purple", "Orange"]
        self.EdgeColor_ListChange = ["黑色", "红色", "黄色", "蓝色", "棕色", "紫色", "橘黄色"]
        self.TypeNote_List = ["All", "Part", "None"]
        self.TypeNote_ListChange = ["全部", "部分", "不显示"]
        self.NoteColor_List = ["Black", "Red", "Yellow", "Blue", "Brown", "Purple", "Orange"]
        self.NoteColor_ListChange = ["黑色", "红色", "黄色", "蓝色", "棕色", "紫色", "橘黄色"]

        self.Files = []
        self.typegraph = self.TypeGraph_List[0]
        self.engine = self.TypeEngine_List[0]
        self.fontsize = self.FontSize_List[6]
        self.typeedge = self.TypeEdge_List[0]

        self.initUI()


    def initUI(self):
        # 程序窗口
        self.setWindowTitle("Mind Mapping")
        self.setWindowIcon(QIcon("icon/Map.png"))
        self.setGeometry(200,100,1000,500)
        self.Layout = QVBoxLayout()

        # 菜单栏中打开文件
        self.action_OpenFile = QAction(QIcon("icon/File.png"), "&Open File", self)
        self.action_OpenFile.setStatusTip("Open one txt file or several images")
        self.action_OpenFile.setShortcut('Ctrl+O')
        self.action_OpenFile.triggered.connect(self.OpenFile)

        # 菜单栏中退出
        self.action_Exit = QAction(QIcon("icon/Exit.png"), "&Exit", self)
        self.action_Exit.setStatusTip("Exit")
        self.action_Exit.setShortcut('Ctrl+Q')
        self.action_Exit.triggered.connect(self.Exit)

        # 菜单栏中有向图还是无向图
        self.action_TypeGraph_List = []
        for i in range(len(self.TypeGraph_List)):
            self.DefineTypeGraph(i)
        self.action_TypeGraph_List[0].setChecked(True)

        # 菜单栏中思维导图布局方式
        self.action_Engine_List = []
        for i in range(len(self.TypeEngine_List)):
            self.DefineEngine(i)
        self.action_Engine_List[0].setChecked(True)

        # 菜单栏中高级属性之字体
        self.action_FontSize_List = []
        for i in range(len(self.FontSize_List)):
            self.DefineFontSize(i)
        self.action_FontSize_List[6].setChecked(True)

        # 菜单栏中高级属性之边类型
        self.action_TypeEdge_List = []
        for i in range(len(self.TypeEdge_List)):
            self.DefineTypeEdge(i)
        self.action_TypeEdge_List[0].setChecked(True)

        # 菜单栏中帮助
        self.action_Help = QAction(QIcon("icon/Help.png"), "&Help", self)
        self.action_Help.setStatusTip("Help")
        self.action_Help.setShortcut('Ctrl+H')
        self.action_Help.triggered.connect(self.Help)

        # 菜单
        self.menubar = self.menuBar()

        # 菜单栏"File"
        self.menu_File = self.menubar.addMenu("File(&F)")
        self.menu_File.addAction(self.action_OpenFile)
        self.menu_File.addAction(self.action_Exit)

        # 菜单栏"Settings"
        self.menu_AdvancedSettings = self.menubar.addMenu("Settings(&T)")
        self.TypeGraph = QMenu("Graph Type", self)
        for i in range(len(self.action_TypeGraph_List)):
            self.TypeGraph.addAction(self.action_TypeGraph_List[i])
        self.Engine = QMenu("Engine", self)
        for i in range(len(self.action_Engine_List)):
            self.Engine.addAction(self.action_Engine_List[i])
        self.FontSize = QMenu("Font Size", self)
        for i in range(len(self.action_FontSize_List)):
            self.FontSize.addAction(self.action_FontSize_List[i])
        self.TypeEdge = QMenu("Edge Type", self)
        for i in range(len(self.action_TypeEdge_List)):
            self.TypeEdge.addAction(self.action_TypeEdge_List[i])
        self.menu_AdvancedSettings.addMenu(self.TypeGraph)
        self.menu_AdvancedSettings.addMenu(self.Engine)
        self.menu_AdvancedSettings.addMenu(self.FontSize)
        self.menu_AdvancedSettings.addMenu(self.TypeEdge)

        # 菜单栏"Help"
        self.menu_Help = self.menubar.addMenu("Help(&H)")
        self.menu_Help.addAction(self.action_Help)


        # 主界面中文件选择
        self.layout_file = QHBoxLayout()
        self.label_select = QLabel("选择文件:")
        self.label_select.setFont(QFont("Myriad Pro", 10))
        self.FilePath = QLineEdit(self)
        self.FilePath.setFont(QFont("Myriad Pro", 10))
        self.SelectButton = QPushButton("浏览", self)
        self.SelectButton.setCheckable(False)
        self.SelectButton.clicked.connect(self.OpenFile)
        self.action_SelectFile = QAction(QIcon("icon/File.png"), "&SelectFile", self)
        self.action_SelectFile.setStatusTip("Select one txt file or several images")
        self.action_SelectFile.triggered.connect(self.OpenFile)
        self.FilePath.addAction(self.action_SelectFile, QLineEdit.TrailingPosition)
        self.layout_file.addWidget(self.label_select)
        self.layout_file.addWidget(self.FilePath)
        self.layout_file.addWidget(self.SelectButton)

        self.attribute = QGridLayout()
        self.attribute.setSpacing(20)

        # 主界面中思维导图方向选择
        self.TypeTree_Label = QLabel("方向:")
        self.attribute.addWidget(self.TypeTree_Label, 0, 0)
        self.TypeTree_Group = QButtonGroup()
        self.TypeTree = {}
        for i in range(len(self.TypeTree_List)):
                self.TypeTree[self.TypeTree_List[i]] = QRadioButton(self.TypeTree_ListChange[i], self)
                self.TypeTree_Group.addButton(self.TypeTree[self.TypeTree_List[i]])
                self.attribute.addWidget(self.TypeTree[self.TypeTree_List[i]], 0, i + 1)
        self.TypeTree[self.TypeTree_List[0]].setChecked(True)

        # 主界面中字体选择
        self.TypeFace_Label = QLabel("字体:")
        self.attribute.addWidget(self.TypeFace_Label, 1, 0)
        self.TypeFace_Group = QButtonGroup()
        self.TypeFace_Com = QComboBox()
        self.TypeFace_Com.addItem("更多")
        self.TypeFace = {}
        for i in range(len(self.TypeFace_List)):
            if i < 4:
                self.TypeFace[self.TypeFace_List[i]] = QRadioButton(self.TypeFace_ListChange[i], self)
                self.TypeFace_Group.addButton(self.TypeFace[self.TypeFace_List[i]])
                self.attribute.addWidget(self.TypeFace[self.TypeFace_List[i]], 1, i+1)
        self.TypeFace_ex = QRadioButton("extra", None)
        self.TypeFace_Group.addButton(self.TypeFace_ex)
        self.TypeFace_Com.addItems(self.TypeFace_ListChange[4:])
        self.TypeFace_Com.currentIndexChanged.connect(self.TypeFace_Mutex)
        self.attribute.addWidget(self.TypeFace_Com, 1, 5)
        self.TypeFace[self.TypeFace_List[0]].setChecked(True)

        # 主界面中边界框格式选择
        self.TypeBbox_Label = QLabel("边界框:")
        self.attribute.addWidget(self.TypeBbox_Label, 2, 0)
        self.TypeBbox_Group = QButtonGroup()
        self.TypeBbox_Com = QComboBox()
        self.TypeBbox_Com.addItem("更多")
        self.TypeBbox = {}
        for i in range(len(self.TypeBbox_List)):
            if i < 4:
                self.TypeBbox[self.TypeBbox_List[i]] = QRadioButton(self.TypeBbox_ListChange[i], self)
                self.TypeBbox_Group.addButton(self.TypeBbox[self.TypeBbox_List[i]], i)
                self.attribute.addWidget(self.TypeBbox[self.TypeBbox_List[i]], 2, i+1)
        self.TypeBbox_ex = QRadioButton("extra", None)
        self.TypeBbox_Group.addButton(self.TypeBbox_ex)
        self.TypeBbox_Com.addItems(self.TypeBbox_ListChange[4:])
        self.TypeBbox_Com.currentIndexChanged.connect(self.TypeBbox_Mutex)
        self.attribute.addWidget(self.TypeBbox_Com, 2, 5)
        self.TypeBbox[self.TypeBbox_List[0]].setChecked(True)

        # 主界面中文字颜色选择
        self.CharColor_Label = QLabel("文字颜色:")
        self.attribute.addWidget(self.CharColor_Label, 3, 0)
        self.CharColor_Group = QButtonGroup()
        self.CharColor_Com = QComboBox()
        self.CharColor_Com.addItem("更多")
        self.CharColor = {}
        for i in range(len(self.CharColor_List)):
            if i < 4:
                self.CharColor[self.CharColor_List[i]] = QRadioButton(self.CharColor_ListChange[i], self)
                self.CharColor_Group.addButton(self.CharColor[self.CharColor_List[i]])
                self.attribute.addWidget(self.CharColor[self.CharColor_List[i]], 3, i+1)
        self.CharColor_ex = QRadioButton("extra", None)
        self.CharColor_Group.addButton(self.CharColor_ex)
        self.CharColor_Com.addItems(self.CharColor_ListChange[4:])
        self.CharColor_Com.currentIndexChanged.connect(self.CharColor_Mutex)
        self.attribute.addWidget(self.CharColor_Com, 3, 5)
        self.CharColor[self.CharColor_List[0]].setChecked(True)

        # 主界面中边界框颜色选择
        self.BboxColor_Label = QLabel("边界框颜色:")
        self.attribute.addWidget(self.BboxColor_Label, 4, 0)
        self.BboxColor_Group = QButtonGroup()
        self.BboxColor_Com = QComboBox()
        self.BboxColor_Com.addItem("更多")
        self.BboxColor = {}
        for i in range(len(self.BboxColor_List)):
            if i < 4:
                self.BboxColor[self.BboxColor_List[i]] = QRadioButton(self.BboxColor_ListChange[i], self)
                self.BboxColor_Group.addButton(self.BboxColor[self.BboxColor_List[i]])
                self.attribute.addWidget(self.BboxColor[self.BboxColor_List[i]], 4, i+1)
        self.BboxColor_ex = QRadioButton("extra", None)
        self.BboxColor_Group.addButton(self.BboxColor_ex)
        self.BboxColor_Com.addItems(self.BboxColor_ListChange[4:])
        self.BboxColor_Com.currentIndexChanged.connect(self.BboxColor_Mutex)
        self.attribute.addWidget(self.BboxColor_Com, 4, 5)
        self.BboxColor[self.BboxColor_List[0]].setChecked(True)

        # 主界面中边颜色选择
        self.EdgeColor_Label = QLabel("边颜色:")
        self.attribute.addWidget(self.EdgeColor_Label, 5, 0)
        self.EdgeColor_Group = QButtonGroup()
        self.EdgeColor_Com = QComboBox()
        self.EdgeColor_Com.addItem("更多")
        self.EdgeColor = {}
        for i in range(len(self.EdgeColor_List)):
            if i < 4:
                self.EdgeColor[self.EdgeColor_List[i]] = QRadioButton(self.EdgeColor_ListChange[i], self)
                self.EdgeColor_Group.addButton(self.EdgeColor[self.EdgeColor_List[i]])
                self.attribute.addWidget(self.EdgeColor[self.EdgeColor_List[i]], 5, i + 1)
        self.EdgeColor_ex = QRadioButton("extra", None)
        self.EdgeColor_Group.addButton(self.EdgeColor_ex)
        self.EdgeColor_Com.addItems(self.EdgeColor_ListChange[4:])
        self.EdgeColor_Com.currentIndexChanged.connect(self.EdgeColor_Mutex)
        self.attribute.addWidget(self.EdgeColor_Com, 5, 5)
        self.EdgeColor[self.EdgeColor_List[0]].setChecked(True)

        # 主界面中内容格式选择
        self.TypeNote_Label = QLabel("内容格式:")
        self.attribute.addWidget(self.TypeNote_Label, 6, 0)
        self.TypeNote_Group = QButtonGroup()
        self.TypeNote = {}
        for i in range(len(self.TypeNote_List)):
            self.TypeNote[self.TypeNote_List[i]] = QRadioButton(self.TypeNote_ListChange[i], self)
            self.TypeNote_Group.addButton(self.TypeNote[self.TypeNote_List[i]])
            self.attribute.addWidget(self.TypeNote[self.TypeNote_List[i]], 6, i + 1)
        self.TypeNote[self.TypeNote_List[0]].setChecked(True)

        # 主界面中内容颜色选择
        self.NoteColor_Label = QLabel("内容颜色:")
        self.attribute.addWidget(self.NoteColor_Label, 7, 0)
        self.NoteColor_Group = QButtonGroup()
        self.NoteColor_Com = QComboBox()
        self.NoteColor_Com.addItem("更多")
        self.NoteColor = {}
        for i in range(len(self.NoteColor_List)):
            if i < 4:
                self.NoteColor[self.NoteColor_List[i]] = QRadioButton(self.NoteColor_ListChange[i], self)
                self.NoteColor_Group.addButton(self.NoteColor[self.NoteColor_List[i]])
                self.attribute.addWidget(self.NoteColor[self.NoteColor_List[i]], 7, i + 1)
        self.NoteColor_ex = QRadioButton("extra", None)
        self.NoteColor_Group.addButton(self.NoteColor_ex)
        self.NoteColor_Com.addItems(self.NoteColor_ListChange[4:])
        self.NoteColor_Com.currentIndexChanged.connect(self.NoteColor_Mutex)
        self.attribute.addWidget(self.NoteColor_Com, 7, 5)
        self.NoteColor[self.NoteColor_List[0]].setChecked(True)

        # 主界面中生成及退出按钮
        self.layout_decision = QHBoxLayout()
        self.image_button = QPushButton("生成图片")
        self.image_button.clicked.connect(self.Generate_Image)
        self.pdf_button = QPushButton("生成PDF")
        self.pdf_button.clicked.connect(self.Generate_PDF)
        self.exit_button = QPushButton("退出")
        self.exit_button.clicked.connect(self.Exit)
        self.layout_decision.addStretch(3)
        self.layout_decision.addWidget(self.image_button)
        self.layout_decision.addStretch(1)
        self.layout_decision.addWidget(self.pdf_button)
        self.layout_decision.addStretch(1)
        self.layout_decision.addWidget(self.exit_button)
        self.layout_decision.addStretch(1)

        # 主界面总体布局
        self.Layout.addStretch(1)
        self.Layout.addLayout(self.layout_file)
        self.Layout.addLayout(self.attribute)
        self.Layout.addStretch(1)
        self.Layout.addLayout(self.layout_decision)
        self.Layout.addStretch(1)
        #self.setLayout(self.Layout)
        self.central = QWidget()
        self.central.setLayout(self.Layout)
        self.setCentralWidget(self.central)

    def OpenFile(self):   # 实现文件选择功能，并对选择的文件进行筛查，查看是否符合规定
        self.Files, FileType = QFileDialog.getOpenFileNames(self, "Mand Mapping: Open File", "./", "All Files(*);;TXT File(*.txt);;Image Files(*.JPG, *.JPEG, *PNG, *GIF)")
        self.exts = []
        for i in range(len(self.Files)):
            file, ext = os.path.splitext(self.Files[i])
            self.exts.append(ext[1:])
        print(self.Files)
        print(self.exts)
        if ("txt" in self.exts):
            if len(self.Files) > 1:
                QMessageBox.question(self, "File information.",
                                     "You can select one txt file or several images",
                                     QMessageBox.Yes)
            else:
                self.FilePath.setText(self.Files[0])
        else:
            ok = True
            for ext in range(len(self.exts)):
                if self.exts[ext] not in ['jpg', 'jpeg', 'png', 'gif', 'JPG', 'JPEG', 'PNG', 'GIF']:
                    QMessageBox.question(self, "File information.",
                                         "You can select one txt file or several images",
                                         QMessageBox.Yes)
                    ok = False
            if ok == True:
                if len(self.Files) == 1:
                    self.FilePath.setText(self.Files[0])
                else:
                    sum_path = ''
                    for i in range(len(self.Files)):
                        sum_path += self.Files[i]
                        if i != len(self.Files)-1:
                            sum_path += "&"
                    self.FilePath.setText(sum_path)

    def TypeFace_Mutex(self):   # 实现字体的单选按钮与下拉框的兼容
        if self.TypeFace_Com.currentText() == "更多":
            self.TypeFace[self.TypeFace_List[0]].setChecked(True)
        else:
            self.TypeFace_ex.setChecked(True)

    def TypeBbox_Mutex(self):   # 实现边界框的单选按钮与下拉框的兼容
        if self.TypeBbox_Com.currentText() == "更多":
            self.TypeBbox[self.TypeBbox_List[0]].setChecked(True)
        else:
            self.TypeBbox_ex.setChecked(True)

    def CharColor_Mutex(self):   # 实现字体颜色的单选按钮与下拉框的兼容
        if self.CharColor_Com.currentText() == "更多":
            self.CharColor[self.CharColor_List[0]].setChecked(True)
        else:
            self.CharColor_ex.setChecked(True)

    def BboxColor_Mutex(self):   # 实现边界框的单选按钮与下拉框的兼容
        if self.BboxColor_Com.currentText() == "更多":
            self.BboxColor[self.BboxColor_List[0]].setChecked(True)
        else:
            self.BboxColor_ex.setChecked(True)

    def EdgeColor_Mutex(self):   # 实现边颜色的单选按钮与下拉框的兼容
        if self.EdgeColor_Com.currentText() == "更多":
            self.EdgeColor[self.EdgeColor_List[0]].setChecked(True)
        else:
            self.EdgeColor_ex.setChecked(True)

    def NoteColor_Mutex(self):   # 实现内容颜色的单选按钮与下拉框的兼容
        if self.NoteColor_Com.currentText() == "更多":
            self.NoteColor[self.NoteColor_List[0]].setChecked(True)
        else:
            self.NoteColor_ex.setChecked(True)

    def Exit(self):   # 实现退出程序功能
        Reply = QMessageBox.question(self, 'EXIT ?',
                                     "Do you really want to EXIT ?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if Reply == QMessageBox.Yes:
            self.close()

    def TypeTree_Decision(self):   # 返回选定的思维导图方向
        return self.TypeTree_List[self.TypeTree_ListChange.index(self.TypeTree_Group.checkedButton().text())]

    def TypeFace_Decision(self):   # 返回选定的字体
        if self.TypeFace_Group.checkedButton().text() != "extra":
            return self.TypeFace_List[self.TypeFace_ListChange.index(self.TypeFace_Group.checkedButton().text())]
        else:
            return self.TypeFace_List[self.TypeFace_ListChange.index(self.TypeFace_Com.currentText())]

    def TypeBbox_Decision(self):   # 返回选定的边界框格式
        if self.TypeBbox_Group.checkedButton().text() != "extra":
            return self.TypeBbox_List[self.TypeBbox_ListChange.index(self.TypeBbox_Group.checkedButton().text())]
        else:
            return self.TypeBbox_List[self.TypeBbox_ListChange.index(self.TypeBbox_Com.currentText())]

    def CharColor_Decision(self):   # 返回选定的文字颜色
        if self.CharColor_Group.checkedButton().text() != "extra":
            return self.CharColor_List[self.CharColor_ListChange.index(self.CharColor_Group.checkedButton().text())]
        else:
            return self.CharColor_List[self.CharColor_ListChange.index(self.CharColor_Com.currentText())]

    def BboxColor_Decision(self):   # 返回选定的边界框颜色
        if self.BboxColor_Group.checkedButton().text() != "extra":
            return self.BboxColor_List[self.BboxColor_ListChange.index(self.BboxColor_Group.checkedButton().text())]
        else:
            return self.BboxColor_List[self.BboxColor_ListChange.index(self.BboxColor_Com.currentText())]

    def EdgeColor_Decision(self):   # 返回选定的边颜色
        if self.EdgeColor_Group.checkedButton().text() != "extra":
            return self.EdgeColor_List[self.EdgeColor_ListChange.index(self.EdgeColor_Group.checkedButton().text())]
        else:
            return self.EdgeColor_List[self.EdgeColor_ListChange.index(self.EdgeColor_Com.currentText())]

    def TypeNote_Decision(self):   # 返回选定的内容格式
        return self.TypeNote_List[self.TypeNote_ListChange.index(self.TypeNote_Group.checkedButton().text())]

    def NoteColor_Decision(self):   # 返回选定的内容颜色
        if self.NoteColor_Group.checkedButton().text() != "extra":
            return self.NoteColor_List[self.NoteColor_ListChange.index(self.NoteColor_Group.checkedButton().text())]
        else:
            return self.NoteColor_List[self.NoteColor_ListChange.index(self.NoteColor_Com.currentText())]

    def Generate_PDF(self):   # 生成PDF型思维导图
        print(self.TypeTree_Decision())
        print(self.TypeFace_Decision())
        print(self.TypeBbox_Decision())
        print(self.CharColor_Decision())
        print(self.BboxColor_Decision())
        print(self.EdgeColor_Decision())
        print(self.NoteColor_Decision())
        print(self.TypeNote_Decision())
        self.Generate("pdf")

    def Generate_Image(self):   # 生成图片型思维导图
        print(self.TypeTree_Decision())
        print(self.TypeFace_Decision())
        print(self.TypeBbox_Decision())
        print(self.CharColor_Decision())
        print(self.BboxColor_Decision())
        print(self.EdgeColor_Decision())
        print(self.NoteColor_Decision())
        print(self.TypeNote_Decision())
        self.Generate("jpg")

    def depth(self, content):   # 返回一行文本的标号以及内容
        label = "0123456789."
        while (content[0] == ' '):
            content = content[1:]
        for i in range(len(content)):
            if content[i] not in label:
                break
        num = content[:i].split('.')
        if num[-1] == '':
            num = num[:-1]
        num = list(map(int, num))
        temp_content = content[i:-1]
        if len(temp_content) > 0:
            while (temp_content[0] == ' '):
                temp_content = temp_content[1:]
        return num, temp_content

    def Generate(self, file_format):   #生成file_format类型的思维导图并展示
        sum_list = [[], [], [], [], []]
        branch_dict = {}
        last_content = ['', '', '', '', '']
        content_dict = {}

        # 再次进行文件格式筛查，实际上没必要，选择文件步骤已经做过
        try:
            print(self.exts)
            print(self.Files)
            if self.exts[0] == 'txt' or self.exts[0] == 'TXT':
                f = open(self.Files[0], 'r', encoding='utf-8')
                context = f.readlines()
            else:
                context = []
                for i in range(len(self.Files)):
                    print(self.Files[i])
                    temp_list = BaiduOCR.detect_image(self.Files[i])
                    for j in range(len(temp_list)):
                        context.append(temp_list[j])
                print(context)
        except:
            QMessageBox.question(self, "File information.",
                                 "You can select one txt file or several images",
                                 QMessageBox.Yes)
            return None
        # 分析笔记结构
        for i in range(len(context)):
            depth_num, content = self.depth(context[i])
            if depth_num == []:
                if i == 0:
                    sum_list[0].append(content)
                    last_depth = []
                    last_content[0] = content
                else:
                    if content == "":
                        pass
                    else:
                        if last_content[len(last_depth)] not in content_dict.keys():
                            content_dict[last_content[len(last_depth)]] = content
                        else:
                            content_dict[last_content[len(last_depth)]] += ("\n" + content)
            else:
                sum_list[len(depth_num)].append(content)
                last_depth = depth_num
                if last_content[len(depth_num) - 1] not in branch_dict.keys():
                    branch_dict[last_content[len(depth_num) - 1]] = []
                branch_dict[last_content[len(depth_num) - 1]].append(content)
                last_content[len(depth_num)] = content

        print(sum_list)
        print("aaaaaaaaaa")
        print(branch_dict)
        print("bbbbbbbbbb")
        print(content_dict)
        # 生成思维导图实例，并设置导图属性
        if self.typegraph == self.TypeGraph_List[0]:
            g = Graph('G', format=file_format, engine=self.engine)
        else:
            g = Digraph('G', format=file_format, engine=self.engine)
        print(self.TypeTree_Decision())
        g.graph_attr['rankdir'] = self.TypeTree_Decision()
        g.attr(rank='same')
        g.node_attr['shape'] = self.TypeBbox_Decision()
        g.node_attr['fontname'] = self.TypeFace_Decision()
        g.node_attr['color'] = self.BboxColor_Decision()
        g.node_attr['fontcolor'] = self.CharColor_Decision()
        g.node_attr['fontsize'] = str(self.fontsize)
        g.edge_attr['color'] = self.EdgeColor_Decision()
        g.edge_attr['style'] = self.typeedge

        # 创建标题节点，并连接有归属关系的标题节点
        for i in range(5):
            if len(sum_list[i]) == 0:
                pass
            else:
                for j in range(len(sum_list[i])):
                    g.node(sum_list[i][j], sum_list[i][j])
                    if sum_list[i][j] in branch_dict.keys():
                        for k in range(len(branch_dict[sum_list[i][j]])):
                            g.edge(sum_list[i][j], branch_dict[sum_list[i][j]][k])
        # 创建内容节点，并连接有归属关系的标题节点与内容节点
        for i in content_dict.keys():
            if i not in branch_dict.keys():
                if self.TypeNote_Decision() == "None":
                    pass
                else:
                    if self.TypeNote_Decision() == "All":
                        temp = content_dict[i]
                        print(self.fontsize)
                        g.node(name=temp, label=temp, fontcolor=self.NoteColor_Decision(),
                               shape = 'none')
                    else:
                        temp = content_dict[i][:10] + "……"
                        g.node(name=temp, label=temp, fontcolor=self.NoteColor_Decision(),
                               shape='none')
                    g.edge(i, temp, color = self.NoteColor_Decision())

        print("yoyoyoyoyoyoyyoyoyo")
        g.view("G")

    def DefineTypeGraph(self, i):   # 生成菜单栏高级属性中的有向图/无向图选项
        self.action_TypeGraph_List.append(QAction(self.TypeGraph_List[i], self, checkable=True))
        self.action_TypeGraph_List[i].triggered.connect(lambda: self.TypeGraph_Decision(i))

    def DefineEngine(self, i):   # 生成菜单栏高级属性中的布局方式选项
        self.action_Engine_List.append(QAction(self.TypeEngine_List[i], self, checkable=True))
        self.action_Engine_List[i].triggered.connect(lambda: self.Engine_Decision(i))

    def DefineFontSize(self, i):   # 生成菜单栏高级属性中的字体大小选项
        self.action_FontSize_List.append(QAction(str(self.FontSize_List[i]), self, checkable=True))
        self.action_FontSize_List[i].triggered.connect(lambda: self.FontSize_Decision(i))

    def DefineTypeEdge(self, i):   # 生成菜单栏高级属性中的边格式选项
        self.action_TypeEdge_List.append(QAction(str(self.TypeEdge_List[i]), self, checkable=True))
        self.action_TypeEdge_List[i].triggered.connect(lambda: self.TypeEdge_Decision(i))

    def TypeGraph_Decision(self, i):   # 高级属性之有向图或无向图
        for j in range(len(self.action_TypeGraph_List)):
            self.action_TypeGraph_List[j].setChecked(False)
        self.action_TypeGraph_List[i].setChecked(True)
        self.typegraph = self.TypeGraph_List[i]

    def Engine_Decision(self, i):   # 高级属性之布局方式
        for j in range(len(self.action_Engine_List)):
            self.action_Engine_List[j].setChecked(False)
        self.action_Engine_List[i].setChecked(True)
        self.engine = self.TypeEngine_List[i]

    def FontSize_Decision(self, i):   # 高级属性之字体大小
        for j in range(len(self.action_FontSize_List)):
            self.action_FontSize_List[j].setChecked(False)
        self.action_FontSize_List[i].setChecked(True)
        self.fontsize = self.FontSize_List[i]

    def TypeEdge_Decision(self, i):   # 高级属性之边格式
        for j in range(len(self.action_TypeEdge_List)):
            self.action_TypeEdge_List[j].setChecked(False)
        self.action_TypeEdge_List[i].setChecked(True)
        self.typeedge = self.TypeEdge_List[i]

    def Help(self):   # 帮助
        QMessageBox.question(self, "Help",
                             "If you have problems using this software, please visit http://graphviz.org/ for some information. Or you can contact me.",
                             QMessageBox.Yes)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    GUI_Window = MainWindow()
    GUI_Window.show()
    sys.exit(app.exec_())
