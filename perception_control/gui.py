import sys
from PyQt5.QtWidgets import QLabel, QPushButton, QSpinBox, QMessageBox, QCheckBox, QApplication, QTextBrowser, QSlider, \
    QDesktopWidget, QLineEdit
from PyQt5.QtCore import Qt, QDateTime, QTimer
from PyQt5.QtGui import QPainter, QPen
import serialcomm
import threading
import time
from PyQt5.Qt import QMainWindow, QWidget
from PyQt5.QtChart import QDateTimeAxis, QValueAxis, QSplineSeries, QChart, QChartView, QLineSeries


class MainWindow(QMainWindow):
    # Serial_thread = None
    # 启停控制 按钮被点击次数
    engine_isclicked_count = 0

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 主窗口
        self.mainWindow()
        # 头标题
        self.title()
        # 状态显示
        self.stateShow()
        # 抽屉开关状态
        self.drawerState()
        # 温度变化曲线
        self.tem_curve()
        # 命令按钮控制
        self.button_command()
        # 创建一个实例，并且打开串口
        self.Serial_thread = serialcomm.SerialAssistant()
        # 绑定信号
        self.Serial_thread.mysingal.connect(self.mysingal_event)
        # 线程启动
        self.Serial_thread.start()
        time.sleep(0.1)
        # self.Serial_thread.set_up_prestart_interval(1)
        # 接收数据
        self.t = threading.Thread(target=self.Serial_thread.recv_data)
        # 设置线程为守护线程，防止退出主线程时，子线程仍在运行
        self.t.setDaemon(True)
        self.t.start()

    def mysingal_event(self, mysignal_event):
        l = mysignal_event
        self.c_tem = l[0]
        self.s_tem = l[1]
        e_state = l[2]
        self.lock1_state = l[3]
        self.lock2_state = l[4]
        self.lock3_state = l[5]
        self.lock4_state = l[6]
        self.lock5_state = l[7]
        self.lock6_state = l[8]
        self.lock7_state = l[9]
        self.lock8_state = l[10]
        self.lock9_state = l[11]
        self.lock10_state = l[12]

        self.current_tem_textBrowser.setText(str(self.c_tem))
        self.current_tem_textBrowser.setStyleSheet(
            "QTextBrowser{color:gray}"
            "QTextBrowser{text-align:center}"
            "QTextBrowser{font-weight:bold}"
            "QTextBrowser{font-size:25px}")
        self.set_tem_textBrowser.setText(str(self.s_tem))
        self.set_tem_textBrowser.setStyleSheet(
            "QTextBrowser{color:gray}"
            "QTextBrowser{text-align:center}"
            "QTextBrowser{font-weight:bold}"
            "QTextBrowser{font-size:25px}")
        self.compress_textBrowser.setText(str(e_state))
        self.compress_textBrowser.setStyleSheet(
            "QTextBrowser{color:gray}"
            "QTextBrowser{text-align:center}"
            "QTextBrowser{font-weight:bold}"
            "QTextBrowser{font-size:25px}")

        if self.lock1_state == '1':
            self.drawer1_switch_label.setStyleSheet("background-color:green")
        else:
            self.drawer1_switch_label.setStyleSheet("background-color:gray")

        if self.lock2_state == '1':
            self.drawer2_switch_label.setStyleSheet("background-color:green")
        else:
            self.drawer2_switch_label.setStyleSheet("background-color:gray")

        if self.lock3_state == '1':
            self.drawer3_switch_label.setStyleSheet("background-color:green")
        else:
            self.drawer3_switch_label.setStyleSheet("background-color:gray")

        if self.lock4_state == '1':
            self.drawer4_switch_label.setStyleSheet("background-color:green")
        else:
            self.drawer4_switch_label.setStyleSheet("background-color:gray")

        if self.lock5_state == '1':
            self.drawer5_switch_label.setStyleSheet("background-color:green")
        else:
            self.drawer5_switch_label.setStyleSheet("background-color:gray")

        if self.lock6_state == '1':
            self.drawer6_switch_label.setStyleSheet("background-color:green")
        else:
            self.drawer6_switch_label.setStyleSheet("background-color:gray")

        if self.lock7_state == '1':
            self.drawer7_switch_label.setStyleSheet("background-color:green")
        else:
            self.drawer7_switch_label.setStyleSheet("background-color:gray")

        if self.lock8_state == '1':
            self.drawer8_switch_label.setStyleSheet("background-color:green")
        else:
            self.drawer8_switch_label.setStyleSheet("background-color:gray")

        if self.lock9_state == '1':
            self.drawer9_switch_label.setStyleSheet("background-color:green")
        else:
            self.drawer9_switch_label.setStyleSheet("background-color:gray")

        if self.lock10_state == '1':
            self.drawer10_switch_label.setStyleSheet("background-color:green")
        else:
            self.drawer10_switch_label.setStyleSheet("background-color:gray")

    def mainWindow(self):
        # 主窗口设置
        self.setWindowTitle('串口通信')  # 标题
        self.resize(700, 800)
        # 窗口居中
        self.center()
        # 最大窗口
        self.setMaximumSize(700, 800)
        # 设置窗口透明度
        self.setWindowOpacity(0.8)

    def center(self):
        # 获取屏幕坐标系
        screen = QDesktopWidget().screenGeometry()
        # 获取窗口坐标系
        size = self.geometry()
        newLeft = (screen.width() - size.width()) / 2
        newTop = (screen.height() - size.height()) / 2

    def title(self):
        self.headlabel = QLabel("现场快递柜状态采集与控制系统", self)
        # 标签在界面上的位置
        self.headlabel.setGeometry(85, 10, 530, 30)
        # 标签风格
        self.headlabel.setStyleSheet(
            "color:rgb(10,10,10,255);"
            "font-size:35px;"
            "font-weight:bold;"
            "font-family:楷体;"
        )

    def stateShow(self):
        # 当前温度的状态显示
        self.current_tem_label = QLabel('当前温度', self)
        self.current_tem_label.setGeometry(102, 80, 80, 20)
        self.current_tem_label.setStyleSheet(
            "color:rgb(100,10,255,255);"
            "font-size:18px;"
            "font-family:黑体"
        )
        self.current_tem_textBrowser = QTextBrowser(self)
        self.current_tem_textBrowser.setGeometry(70, 110, 140, 40)
        self.current_tem_textBrowser.setAlignment(Qt.AlignCenter)

        # 设定温度
        self.set_tem_label = QLabel('设定温度', self)
        self.set_tem_label.setGeometry(302, 80, 80, 20)
        self.set_tem_label.setStyleSheet(
            "color:rgb(100,10,255,255);"
            "font-size:18px;"
            "font-family:黑体"
        )
        self.set_tem_textBrowser = QTextBrowser(self)
        self.set_tem_textBrowser.setGeometry(270, 110, 140, 40)

        # 压缩机
        self.compress_label = QLabel('工作状态', self)
        self.compress_label.setGeometry(512, 80, 80, 20)
        self.compress_label.setStyleSheet(
            "color:rgb(100,10,255,255);"
            "font-size:18px;"
            "font-family:黑体"
        )
        self.compress_textBrowser = QTextBrowser(self)
        self.compress_textBrowser.setGeometry(480, 110, 140, 40)

        # 分区名————状态显示
        self.state_label = QLabel('状态显示', self)
        self.state_label.setGeometry(550, 165, 100, 30)
        self.state_label.setStyleSheet(
            "font-weight:bold;"
            "font-size:20px;"
        )

    def drawerState(self):
        # 抽屉1
        self.drawer1_label = QLabel('抽屉1', self)
        self.drawer1_label.setGeometry(60, 215, 50, 20)
        self.drawer1_label.setStyleSheet(
            "color:rgb(255,0,0,255);"
            "font-size:18px;"
            "font-family:黑体"
        )
        self.drawer1_switch_label = QLabel(self)
        self.drawer1_switch_label.setGeometry(45, 242, 80, 35)
        self.drawer1_switch_label.setStyleSheet("background-color:gray")

        # 抽屉2
        self.drawer2_label = QLabel('抽屉2', self)
        self.drawer2_label.setGeometry(195, 215, 50, 20)
        self.drawer2_label.setStyleSheet(
            "color:rgb(255,0,0,255);"
            "font-size:18px;"
            "font-family:黑体"
        )
        self.drawer2_switch_label = QLabel(self)
        self.drawer2_switch_label.setGeometry(180, 242, 80, 35)
        self.drawer2_switch_label.setStyleSheet("background-color:gray")

        # 抽屉3
        self.drawer3_label = QLabel('抽屉3', self)
        self.drawer3_label.setGeometry(325, 215, 50, 20)
        self.drawer3_label.setStyleSheet(
            "color:rgb(255,0,0,255);"
            "font-size:18px;"
            "font-family:黑体"
        )
        self.drawer3_switch_label = QLabel(self)
        self.drawer3_switch_label.setGeometry(305, 242, 80, 35)
        self.drawer3_switch_label.setStyleSheet("background-color:gray")

        # 抽屉4
        self.drawer4_label = QLabel('抽屉4', self)
        self.drawer4_label.setGeometry(450, 215, 50, 20)
        self.drawer4_label.setStyleSheet(
            "color:rgb(255,0,0,255);"
            "font-size:18px;"
            "font-family:黑体"
        )

        self.drawer4_switch_label = QLabel(self)
        self.drawer4_switch_label.setGeometry(435, 242, 80, 35)
        self.drawer4_switch_label.setStyleSheet("background-color:gray")

        # 抽屉5
        self.drawer5_label = QLabel('抽屉5', self)
        self.drawer5_label.setGeometry(580, 215, 50, 20)
        self.drawer5_label.setStyleSheet(
            "color:rgb(255,0,0,255);"
            "font-size:18px;"
            "font-family:黑体"
        )
        self.drawer5_switch_label = QLabel(self)
        self.drawer5_switch_label.setGeometry(565, 242, 80, 35)
        self.drawer5_switch_label.setStyleSheet("background-color:gray")

        # 抽屉6
        self.drawer6_label = QLabel('抽屉6', self)
        self.drawer6_label.setGeometry(60, 285, 50, 20)
        self.drawer6_label.setStyleSheet(
            "color:rgb(255,0,0,255);"
            "font-size:18px;"
            "font-family:黑体"
        )
        self.drawer6_switch_label = QLabel(self)
        self.drawer6_switch_label.setGeometry(45, 310, 80, 35)
        self.drawer6_switch_label.setStyleSheet("background-color:gray")

        # 抽屉7
        self.drawer7_label = QLabel('抽屉7', self)
        self.drawer7_label.setGeometry(195, 285, 50, 20)
        self.drawer7_label.setStyleSheet(
            "color:rgb(255,0,0,255);"
            "font-size:18px;"
            "font-family:黑体"
        )
        self.drawer7_switch_label = QLabel(self)
        self.drawer7_switch_label.setGeometry(180, 310, 80, 35)
        self.drawer7_switch_label.setStyleSheet("background-color:gray")

        # 抽屉8
        self.drawer8_label = QLabel('抽屉8', self)
        self.drawer8_label.setGeometry(325, 285, 50, 20)
        self.drawer8_label.setStyleSheet(
            "color:rgb(255,0,0,255);"
            "font-size:18px;"
            "font-family:黑体"
        )
        self.drawer8_switch_label = QLabel(self)
        self.drawer8_switch_label.setGeometry(305, 310, 80, 35)
        self.drawer8_switch_label.setStyleSheet("background-color:gray")

        # 抽屉9
        self.drawer9_label = QLabel('抽屉9', self)
        self.drawer9_label.setGeometry(450, 285, 50, 20)
        self.drawer9_label.setStyleSheet(
            "color:rgb(255,0,0,255);"
            "font-size:18px;"
            "font-family:黑体"
        )

        self.drawer9_switch_label = QLabel(self)
        self.drawer9_switch_label.setGeometry(435, 310, 80, 35)
        self.drawer9_switch_label.setStyleSheet("background-color:gray")

        # 抽屉10
        self.drawer10_label = QLabel('抽屉10', self)
        self.drawer10_label.setGeometry(580, 285, 55, 20)
        self.drawer10_label.setStyleSheet(
            "color:rgb(255,0,0,255);"
            "font-size:18px;"
            "font-family:黑体"
        )
        self.drawer10_switch_label = QLabel(self)
        self.drawer10_switch_label.setGeometry(565, 310, 80, 35)
        self.drawer10_switch_label.setStyleSheet("background-color:gray")

        # 分区名————状态显示
        self.state_label = QLabel('抽屉状态', self)
        self.state_label.setGeometry(550, 345, 100, 30)
        self.state_label.setStyleSheet(
            "font-weight:bold;"
            "font-size:20px;"
        )

    def tem_curve(self):
        self.tem_curve_label = QLabel('温度曲线', self)
        self.tem_curve_label.setGeometry(550, 685, 120, 30)
        self.tem_curve_label.setStyleSheet(
            "font-weight:bold;"
            "font-size:20px;"
        )
        self.chart_init()
        self.timer_init()

    def timer_init(self):
        # 使用QTimer，1秒触发一次，更新数据
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.drawLine)
        self.timer.start(1000)

    def chart_init(self):
        self.chart = QChart()

        self.chartview = QChartView(self)
        self.chartview.setGeometry(25, 385, 640, 300)
        # 抗锯齿
        self.chartview.setRenderHint(QPainter.Antialiasing)
        self.chartview.setChart(self.chart)

        # 绘制曲线
        # self.series = QSplineSeries()
        # 绘制折线图
        self.series_collect_tem = QLineSeries()
        self.series_set_tem = QSplineSeries()
        # 设置曲线名称
        self.series_collect_tem.setName("采集温度")
        self.series_set_tem.setName("设定温度")
        # 把曲线添加到QChart的实例中
        self.chart.addSeries(self.series_collect_tem)
        self.chart.addSeries(self.series_set_tem)
        # 声明并初始化X轴，Y轴

        self.dtaxisX = QDateTimeAxis()
        self.vlaxisY = QValueAxis()
        # 设置坐标轴显示范围
        self.dtaxisX.setMin(QDateTime.currentDateTime().addSecs(-60 * 1))
        self.dtaxisX.setMax(QDateTime.currentDateTime().addSecs(0))
        self.vlaxisY.setMin(-10)
        self.vlaxisY.setMax(35)
        # 设置X轴时间样式
        self.dtaxisX.setFormat("hh:mm:ss")
        # 设置坐标轴上的格点
        self.dtaxisX.setTickCount(6)
        self.vlaxisY.setTickCount(5)
        # 设置坐标轴名称
        self.dtaxisX.setTitleText("时间")
        self.vlaxisY.setTitleText("温度/℃")
        # 设置网格不显示
        self.vlaxisY.setGridLineVisible(False)
        # 把坐标轴添加到chart中
        self.chart.addAxis(self.dtaxisX, Qt.AlignBottom)
        self.chart.addAxis(self.vlaxisY, Qt.AlignLeft)
        # 把曲线关联到坐标轴
        self.series_collect_tem.attachAxis(self.dtaxisX)
        self.series_collect_tem.attachAxis(self.vlaxisY)
        self.series_set_tem.attachAxis(self.dtaxisX)
        self.series_set_tem.attachAxis(self.vlaxisY)

    def drawLine(self):
        # 获取当前时间
        bjtime = QDateTime.currentDateTime()
        # 更新X轴坐标
        self.dtaxisX.setMin(QDateTime.currentDateTime().addSecs(-60 * 1))
        self.dtaxisX.setMax(QDateTime.currentDateTime().addSecs(0))
        # 当曲线上的点超出X轴的范围时，移除最早的点
        if (self.series_collect_tem.count() > 60):
            self.series_collect_tem.removePoints(0, self.series_collect_tem.count() - 60)
        # 产生随即数
        # yint = random.randint(-20, 40)
        # 添加数据到曲线末端
        self.series_collect_tem.append(bjtime.toMSecsSinceEpoch(), self.c_tem)

        if (self.series_set_tem.count() > 60):
            self.series_set_tem.removePoints(0, self.series_set_tem.count() - 60)
        # 产生随即数
        # yint = random.randint(-20, 40)
        # 添加数据到曲线末端
        self.series_set_tem.append(bjtime.toMSecsSinceEpoch(), self.s_tem)

    def button_command(self):
        # 打开抽屉
        self.btn_open_drawer = QPushButton('打开抽屉', self)
        self.btn_open_drawer.setGeometry(10, 730, 150, 50)
        self.btn_open_drawer.setStyleSheet(
            "QPushButton{color:rgb(255,255,255,255)}"
            "QPushButton:hover{color:black}"
            "QPushButton{background-color:rgb(255,100,125,255)}"
            "QPushButton{border:10px}"
            "QPushButton{border-radius:20px}"
            "QPushButton{padding:2px 4px}"
            "QPushButton{font-weight:bold}"
            "QPushButton{font-size:20px}")
        self.btn_open_drawer.setToolTip("这是用来打开指定抽屉的")

        # 启停温度控制
        self.btn_OpenClose_tem = QPushButton('启停温度控制', self)
        self.btn_OpenClose_tem.setGeometry(188, 730, 150, 50)
        self.btn_OpenClose_tem.setStyleSheet(
            "QPushButton{color:rgb(255,255,255,255)}"
            "QPushButton:hover{color:blue}"
            "QPushButton{background-color:rgb(255,100,125,255)}"
            "QPushButton{border:10px}"
            "QPushButton{border-radius:20px}"
            "QPushButton{padding:2px 4px}"
            "QPushButton{font-weight:bold}"
            "QPushButton{font-size:20px}")
        self.btn_OpenClose_tem.setToolTip('这是用来启停压缩机的')
        self.btn_OpenClose_tem.clicked.connect(self.openCloseCommpress_event)

        # 设置控制温度
        self.btn_control_tem = QPushButton('设置控制温度', self)
        self.btn_control_tem.setGeometry(363, 730, 150, 50)
        self.btn_control_tem.setStyleSheet(
            "QPushButton{color:rgb(255,255,255,255)}"
            "QPushButton:hover{color:green}"
            "QPushButton{background-color:rgb(255,100,125,255)}"
            "QPushButton{border:10px}"
            "QPushButton{border-radius:20px}"
            "QPushButton{padding:2px 4px}"
            "QPushButton{font-weight:bold}"
            "QPushButton{font-size:20px}")
        self.btn_control_tem.setToolTip('这是用来设置控制温度的')

        # 设置系统参数
        self.btn_set_system = QPushButton('设置系统参数', self)
        self.btn_set_system.setGeometry(540, 730, 150, 50)
        self.btn_set_system.setStyleSheet(
            "QPushButton{color:rgb(255,255,255,255)}"
            "QPushButton:hover{color:orange}"
            "QPushButton{background-color:rgb(255,100,125,255)}"
            "QPushButton{border:10px}"
            "QPushButton{border-radius:20px}"
            "QPushButton{padding:2px 4px}"
            "QPushButton{font-weight:bold}"
            "QPushButton{font-size:20px}")
        self.btn_set_system.setToolTip('这是用来设置系统参数的')

    def openCloseCommpress_event(self):
        # 启动
        # self.engine_isclicked_count += 1
        # count = self.engine_isclicked_count % 2
        # print(count)
        if self.Serial_thread.data == ['00'] * 44 or self.Serial_thread.data == b'':
            QMessageBox.warning(None, '警告', '未连接至控制板，不能进行此操作!')

        else:
            self.engine_isclicked_count += 1
            count = self.engine_isclicked_count % 2

           # self.Serial_thread.set_up_prestart_interval(1)
            self.Serial_thread.success_flag=1
            self.Serial_thread.control_engine()
            if self.Serial_thread.success_flag == 1 and count == 1:
                time.sleep(1)
                QMessageBox().information(None, "提示", "开启成功！", QMessageBox.Yes)
                self.Serial_thread.success_flag = 0
            elif self.Serial_thread.success_flag == 1 and count == 0:
                time.sleep(1)
                QMessageBox().information(None, "提示", "关闭成功！", QMessageBox.Yes)
                self.Serial_thread.success_flag = 0

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.drawLines(qp)
        qp.end()

    def drawLines(self, qp):
        pen = QPen(Qt.black, 2, Qt.SolidLine)
        qp.setPen(pen)
        # 状态显示   的布局
        qp.drawLine(20, 60, 670, 60)
        qp.drawLine(20, 60, 20, 180)
        qp.drawLine(20, 180, 530, 180)
        qp.drawLine(670, 60, 670, 180)
        qp.drawLine(640, 180, 670, 180)

        #  开关状态    的布局
        qp.drawLine(20, 200, 670, 200)
        qp.drawLine(20, 200, 20, 360)
        qp.drawLine(670, 200, 670, 360)
        qp.drawLine(20, 360, 530, 360)
        qp.drawLine(640, 360, 670, 360)

        #  温度变化   的布局
        qp.drawLine(20, 380, 670, 380)
        qp.drawLine(20, 380, 20, 700)
        qp.drawLine(20, 700, 530, 700)
        qp.drawLine(670, 380, 670, 700)
        qp.drawLine(670, 700, 640, 700)

    def closeEvent(self, event):
        reply = QMessageBox.question(None, 'Message',
                                     "Are you sure to quit?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


class ChooseDrawer(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 主窗口设置
        self.main_window()
        # 提示标签
        self.tiptxt()
        # 单选框按钮
        self.radio_drawer()
        # 按钮
        self.button()

    def main_window(self):
        self.setWindowTitle('抽屉选择')
        self.resize(450, 200)
        self.setMaximumSize(450, 200)
        # 阻塞主窗口
        self.setWindowModality(Qt.ApplicationModal)

    def tiptxt(self):
        self.tip_label = QLabel('请选择要打开的抽屉', self)
        self.tip_label.setGeometry(30, 5, 280, 40)
        self.tip_label.setStyleSheet(
            "color:rgb(255,0,255,255);"
            "font-size:25px;"
            "font-family:楷体;"
            "font-weight:bold;"
        )

    def radio_drawer(self):
        # 抽屉1
        self.radio_drawer1 = QCheckBox('抽屉1', self)
        self.radio_drawer1.setGeometry(20, 70, 90, 20)

        # 抽屉2
        self.radio_drawer2 = QCheckBox('抽屉2', self)
        self.radio_drawer2.setGeometry(105, 70, 90, 20)

        # 抽屉3
        self.radio_drawer3 = QCheckBox('抽屉3', self)
        self.radio_drawer3.setGeometry(190, 70, 90, 20)

        # 抽屉4
        self.radio_drawer4 = QCheckBox('抽屉4', self)
        self.radio_drawer4.setGeometry(285, 70, 90, 20)

        # 抽屉5
        self.radio_drawer5 = QCheckBox('抽屉5', self)
        self.radio_drawer5.setGeometry(370, 70, 90, 20)

        # 抽屉6
        self.radio_drawer6 = QCheckBox('抽屉6', self)
        self.radio_drawer6.setGeometry(20, 100, 90, 20)

        # 抽屉7
        self.radio_drawer7 = QCheckBox('抽屉7', self)
        self.radio_drawer7.setGeometry(105, 100, 90, 20)

        # 抽屉8
        self.radio_drawer8 = QCheckBox('抽屉8', self)
        self.radio_drawer8.setGeometry(190, 100, 90, 20)

        # 抽屉9
        self.radio_drawer9 = QCheckBox('抽屉9', self)
        self.radio_drawer9.setGeometry(285, 100, 90, 20)

        # 抽屉10
        self.radio_drawer10 = QCheckBox('抽屉10', self)
        self.radio_drawer10.setGeometry(370, 100, 90, 20)

    def button(self):
        # 打开按钮
        self.btn_open = QPushButton('打开', self)
        self.btn_open.setGeometry(80, 145, 100, 40)
        self.btn_open.setStyleSheet(
            "QPushButton{color:rgb(255,255,255,255)}"
            "QPushButton:hover{color:black}"
            "QPushButton{background-color:rgb(255,125,100,255)}"
            "QPushButton{border:10px}"
            "QPushButton{border-radius:20px}"
            "QPushButton{padding:2px 4px}"
            "QPushButton{font-weight:bold}"
            "QPushButton{font-size:20px}")
        self.btn_open.setToolTip('这是用来打开抽屉的')
        self.btn_open.clicked.connect(self.btn_open_event)

        # 返回按钮
        self.btn_return = QPushButton('返回', self)
        self.btn_return.setGeometry(260, 145, 100, 40)
        self.btn_return.setStyleSheet(
            "QPushButton{color:rgb(255,255,255,255)}"
            "QPushButton:hover{color:black}"
            "QPushButton{background-color:rgb(255,125,100,255)}"
            "QPushButton{border:10px}"
            "QPushButton{border-radius:20px}"
            "QPushButton{padding:2px 4px}"
            "QPushButton{font-weight:bold}"
            "QPushButton{font-size:20px}")
        self.btn_return.clicked.connect(self.btn_return_event)
        self.btn_return.setToolTip('这是用来返回界面的')

    def btn_open_event(self):
        lock_list = []
        if self.radio_drawer1.isChecked():
            lock_list.append(1)
        if self.radio_drawer2.isChecked():
            lock_list.append(2)
        if self.radio_drawer3.isChecked():
            lock_list.append(3)
        if self.radio_drawer4.isChecked():
            lock_list.append(4)
        if self.radio_drawer5.isChecked():
            lock_list.append(5)
        if self.radio_drawer6.isChecked():
            lock_list.append(6)
        if self.radio_drawer7.isChecked():
            lock_list.append(7)
        if self.radio_drawer8.isChecked():
            lock_list.append(8)
        if self.radio_drawer9.isChecked():
            lock_list.append(9)
        if self.radio_drawer10.isChecked():
            lock_list.append(10)

        def close_drawser_set_checked():
            time.sleep(30)
            main_window.Serial_thread.open_clock([])
            time.sleep(1)
            self.radio_drawer1.setChecked(False)
            self.radio_drawer2.setChecked(False)
            self.radio_drawer3.setChecked(False)
            self.radio_drawer4.setChecked(False)
            self.radio_drawer5.setChecked(False)
            self.radio_drawer6.setChecked(False)
            self.radio_drawer7.setChecked(False)
            self.radio_drawer8.setChecked(False)
            self.radio_drawer9.setChecked(False)
            self.radio_drawer10.setChecked(False)

        if lock_list == []:
            QMessageBox.information(self, '提示', '未选择抽屉', QMessageBox.Yes)

        else:
            main_window.Serial_thread.open_clock(lock_list)
            t = threading.Thread(target=close_drawser_set_checked)
            t.setDaemon(True)
            t.start()
            if main_window.Serial_thread.success_flag == 1:
                time.sleep(0.5)
                QMessageBox.information(self, '提示', '抽屉打开成功')
                main_window.Serial_thread.success_flag = 0
            self.close()

    def btn_return_event(self):
        self.close()


class SetTem(QWidget):
    tem = 4

    def __init__(self, parent=None):
        super(SetTem, self).__init__(parent)
        self.setWindowTitle('设定指定温度')
        self.resize(500, 200)
        self.setWindowModality(Qt.ApplicationModal)

        self.label_tip = QLabel('请设定温度', self)
        self.label_tip.setAlignment(Qt.AlignCenter)
        self.label_tip.setGeometry(10, 20, 160, 40)
        self.label_tip.setStyleSheet(
            "background-color:rgb(100,200,255,255);"
            "font-size:25px;"
            "font-family:楷体;"
            "font-weight:bold;"
        )

        self.tem_show = QTextBrowser(self)
        self.tem_show.setGeometry(400, 20, 80, 50)
        self.tem_show.setText(str(4))
        self.tem_show.setStyleSheet(
            "QTextBrowser{color:rgb(255,100,20)}"
            "QTextBrowser{text-align:center}"
            "QTextBrowser{font-weight:bold}"
            "QTextBrowser{font-size:25px}")

        self.slider = QSlider(Qt.Horizontal, self)
        self.slider.setStyleSheet(

            "padding-top:15px;"
            "padding-bottom:15px;"
            "padding-radius:5px;"
        )
        self.slider.setGeometry(10, 80, 480, 50)
        self.slider.setMinimum(-20)
        self.slider.setMaximum(70)
        self.slider.setSingleStep(1)
        self.slider.setValue(8)
        self.slider.setTickPosition(QSlider.TicksBelow)
        self.slider.setTickInterval(1)

        self.slider.valueChanged.connect(self.valuechange)

        self.btn_set = QPushButton('设定', self)
        self.btn_set.setGeometry(50, 150, 100, 40)
        self.btn_set.setStyleSheet(
            "QPushButton{color:rgb(255,255,255,255)}"
            "QPushButton:hover{color:black}"
            "QPushButton{background-color:rgb(200,100,100,255)}"
            "QPushButton{border:100px}"
            "QPushButton{border-radius:15px}"
            "QPushButton{padding:2px 4px}"
            "QPushButton{font-weight:bold}"
            "QPushButton{font-size:20px}")
        self.btn_set.setToolTip('这是用来设定温度的')
        self.btn_set.clicked.connect(self.btn_set_event)

        self.btn_return = QPushButton('返回', self)
        self.btn_return.setGeometry(350, 150, 100, 40)
        self.btn_return.setStyleSheet(
            "QPushButton{color:rgb(255,255,255,255)}"
            "QPushButton:hover{color:black}"
            "QPushButton{background-color:rgb(200,100,100,255)}"
            "QPushButton{border:100px}"
            "QPushButton{border-radius:15px}"
            "QPushButton{padding:2px 4px}"
            "QPushButton{font-weight:bold}"
            "QPushButton{font-size:20px}")
        self.btn_return.setToolTip('这是用来返回的')
        self.btn_return.clicked.connect(self.btn_return_event)

    def btn_set_event(self):
        self.tem = self.slider.value() / 2

        main_window.Serial_thread.set_up_temp(self.tem)
        if main_window.Serial_thread.success_flag == 1:
            time.sleep(1)
            QMessageBox.information(self, '提示', '已成功设置控制温度')
            main_window.Serial_thread.success_flag = 0

        self.close()

    def btn_return_event(self):
        self.close()

    def valuechange(self):
        self.tem_show.setText(str(self.slider.value() / 2))


class SETsystem(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 主窗口
        self.mainWindow()
        self.spin()
        self.tips()
        self.button()
        self.txt()

    def mainWindow(self):
        # 主窗口设置
        self.setWindowTitle('系统参数设置')  # 标题
        # 阻塞主窗口
        self.setWindowModality(Qt.ApplicationModal)
        self.resize(40000, 300)
        # 窗口居中
        self.center()
        # 最大窗口
        self.setMaximumSize(400, 300)
        # 设置窗口透明度

    # self.setWindowOpacity(0.8)

    def center(self):
        # 获取屏幕坐标系
        screen = QDesktopWidget().screenGeometry()
        # 获取窗口坐标系
        size = self.geometry()
        newLeft = (screen.width() - size.width()) / 2
        newTop = (screen.height() - size.height()) / 2

    def tips(self):
        self.time_out_label = QLabel('压缩机启动延时(/s)', self)
        self.time_out_label.setGeometry(10, 25, 200, 20)
        self.time_out_label.setStyleSheet(
            'font-family:楷体;'
            'font-size:20px;'
            'font-weight:bold;'
        )

        self.tem_deviation_label = QLabel('温度控制偏差(/℃)', self)
        self.tem_deviation_label.setGeometry(10, 80, 200, 20)
        self.tem_deviation_label.setStyleSheet(
            'font-family:楷体;'
            'font-size:20px;'
            'font-weight:bold;'
        )

        self.device_id_label = QLabel('设备ID', self)
        self.device_id_label.setGeometry(10, 135, 200, 20)
        self.device_id_label.setStyleSheet(
            'font-family:楷体;'
            'font-size:20px;'
            'font-weight:bold;'
        )

        self.device_address_label = QLabel('设备地址', self)
        self.device_address_label.setGeometry(10, 190, 200, 20)
        self.device_address_label.setStyleSheet(
            'font-family:楷体;'
            'font-size:20px;'
            'font-weight:bold;'
        )

    def spin(self):
        self.timeout_spin = QSpinBox(self)
        self.timeout_spin.setGeometry(250, 20, 125, 30)
        self.timeout_spin.setMaximum(30)
        self.timeout_spin.setValue(1)

        self.tem_deviation_spin = QSpinBox(self)
        self.tem_deviation_spin.setGeometry(250, 77, 125, 30)
        self.tem_deviation_spin.setMaximum(10)
        self.tem_deviation_spin.setMinimum(2)
        self.tem_deviation_spin.setValue(2)

        self.device_address_spin = QSpinBox(self)
        self.device_address_spin.setGeometry(250, 180, 125, 30)
        self.device_address_spin.setMinimum(1)
        self.device_address_spin.setMaximum(120)

    def txt(self):
        self.device_id_txt = QLineEdit(self)
        self.device_id_txt.setGeometry(250, 128, 125, 30)
        self.device_id_txt.setText('10 01 25 F0 02')

    def button(self):
        self.btn_set = QPushButton('设定', self)
        self.btn_set.setGeometry(50, 240, 100, 50)
        self.btn_set.clicked.connect(self.btn_set_event)
        self.btn_set.setStyleSheet(
            "QPushButton{color:rgb(125,255,255,255)}"
            "QPushButton:hover{color:black}"
            "QPushButton{background-color:rgb(200,50,100,255)}"
            "QPushButton{border:100px}"
            "QPushButton{border-radius:15px}"
            "QPushButton{padding:2px 4px}"
            "QPushButton{font-weight:bold}"
            "QPushButton{font-size:20px}"
        )

        self.btn_return = QPushButton('返回', self)
        self.btn_return.setGeometry(240, 240, 100, 50)
        self.btn_return.clicked.connect(self.btn_return_event)
        self.btn_return.setStyleSheet(
            "QPushButton{color:rgb(125,255,255,255)}"
            "QPushButton:hover{color:black}"
            "QPushButton{background-color:rgb(200,50,100,255)}"
            "QPushButton{border:100px}"
            "QPushButton{border-radius:15px}"
            "QPushButton{padding:2px 4px}"
            "QPushButton{font-weight:bold}"
            "QPushButton{font-size:20px}"
        )

    def btn_set_event(self):
        # l=[]
        # l.append(self.timeout_spin.value())
        # l.append(self.tem_deviation_spin.value())
        # l.append(self.device_address_spin.value())
        # l.append(self.device_id_txt.text())

        # print(l)

        # 设置时间间隔,温度偏差
        def set_interval_tem_offset():
            main_window.Serial_thread.set_up_prestart_interval(self.timeout_spin.value())
            main_window.Serial_thread.set_up_temp_offset(self.tem_deviation_spin.value())
            # set_tem_window.tem = set_tem_window.slider.value() / 2

        # main_window.Serial_thread.set_up_temp(set_tem_window.tem)

        # 设置设备地址和id
        def set_device_address_id():
            main_window.Serial_thread.set_up_device_address(self.device_address_spin.value())
            main_window.Serial_thread.set_up_device_code(self.device_id_txt.text())
            # set_tem_window.tem=set_tem_window.slider.value()/2

        # main_window.Serial_thread.set_up_temp(set_tem_window.tem)

        t1 = threading.Thread(target=set_interval_tem_offset)

        t3 = threading.Thread(target=set_device_address_id)
        # t4=threading.Thread(target=set_id)
        t1.setDaemon(True)
        # t2.setDaemon(True)
        t3.setDaemon(True)
        # t4.setDaemon(True)
        t1.start()
        # t2.start()
        t3.start()
        # t4.start()

        time.sleep(2)
        # set_tem_window.tem = set_tem_window.slider.value() / 2
        # main_window.Serial_thread.set_up_temp(set_tem_window.tem)
        QMessageBox.information(self, '提示', '设置成功', QMessageBox.Yes)
        self.close()

    def btn_return_event(self):
        self.close()


def btn_open_drawer_event():
    if main_window.Serial_thread.data == ['00'] * 44 or main_window.Serial_thread.data == b'':
        QMessageBox.warning(None, '警告', '未连接至控制板，不能进行此操作!')
    else:
        drawer_window.show()


def btn_set_tem_event():
    if main_window.Serial_thread.data == ['00'] * 44 or main_window.Serial_thread.data == b'':
        QMessageBox.warning(None, '警告', '未连接至控制板，不能进行此操作!')
    elif main_window.engine_isclicked_count % 2 == 0:
        QMessageBox.warning(None, '警告', '未开启压缩机，无法设置控制温度')
    else:
        set_tem_window.show()


def btn_set_system():
    if main_window.Serial_thread.data == ['00'] * 44 or main_window.Serial_thread.data == b'':
        QMessageBox.warning(None, '警告', '未连接至控制板，不能进行此操作!')
    # elif main_window.engine_isclicked_count%2==1:
    # QMessageBox.warning(None,'警告','未关闭压缩机，无法设置系统参数')
    else:
        system_window.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    drawer_window = ChooseDrawer()
    main_window.btn_open_drawer.clicked.connect(btn_open_drawer_event)
    set_tem_window = SetTem()
    main_window.btn_control_tem.clicked.connect(btn_set_tem_event)
    system_window = SETsystem()
    main_window.btn_set_system.clicked.connect(btn_set_system)
    sys.exit(app.exec_())
