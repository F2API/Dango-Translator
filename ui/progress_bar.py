from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import os
import base64

import ui.static.icon
import utils.thread
import utils.message

LOADING_PATH = "./config/icon/loading.gif"


# 进度条
class ProgressBar(QWidget) :

    def __init__(self, rate, use_type) :

        super(ProgressBar, self).__init__()
        self.rate = rate
        self.use_type = use_type
        self.getInitConfig()
        self.ui()


    def ui(self) :

        # 窗口置顶
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        # 窗口尺寸及不可拉伸
        self.resize(self.window_width, self.window_height)
        self.setMinimumSize(QSize(self.window_width, self.window_height))
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.WindowCloseButtonHint)
        # 窗口图标
        self.setWindowIcon(ui.static.icon.APP_LOGO_ICON)
        # 设置字体
        self.setStyleSheet("font: %spt '%s'; background-color: rgb(255, 255, 255);}"%(self.font_size, self.font_type))

        self.progress_bar = QProgressBar(self)
        self.customSetGeometry(self.progress_bar, 20, 10, 260, 10)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setStyleSheet("QProgressBar { background-color: rgba(62, 62, 62, 0.2); "
                                        "border-radius: 6px;}"
                                        "QProgressBar::chunk { background-color: %s; border-radius: 5px;}"
                                        %(self.color_2))
        self.progress_bar.setValue(0)

        self.progress_label = QLabel(self)
        self.customSetGeometry(self.progress_label, 240, 25, 150, 20)
        self.progress_label.setStyleSheet("color: %s"%self.color_2)

        self.file_size_label = QLabel(self)
        self.customSetGeometry(self.file_size_label, 20, 25, 150, 20)
        self.file_size_label.setStyleSheet("color: %s" % self.color_2)

        self.paintProgressBar(0, 0, "0/0")


    # 根据分辨率定义控件位置尺寸
    def customSetGeometry(self, object, x, y, w, h) :

        object.setGeometry(QRect(int(x * self.rate),
                                 int(y * self.rate),
                                 int(w * self.rate),
                                 int(h * self.rate)))


    # 初始化配置
    def getInitConfig(self):

        # 界面字体
        self.font_type = "华康方圆体W7"
        # 界面字体大小
        self.font_size = 10
        # 灰色
        self.color_1 = "#595959"
        # 蓝色
        self.color_2 = "#5B8FF9"
        # 界面尺寸
        self.window_width = int(300 * self.rate)
        self.window_height = int(50 * self.rate)
        # 结束信号
        self.finish_sign = False
        # 中止信号
        self.stop_sign = False


    # 绘制进度信息
    def paintProgressBar(self, float_val, int_val, str_val) :

        self.progress_label.setText("{:.2f}%".format(float_val))
        self.progress_bar.setValue(int_val)
        self.file_size_label.setText(str_val)


    # 修改窗口标题
    def modifyTitle(self, title) :

        self.setWindowTitle(title)


    # 停止任务
    def stopProcess(self) :

        self.stop_sign = True


    # 窗口关闭处理
    def closeEvent(self, event) :

        if self.finish_sign :
            return
        if self.use_type == "offline_ocr" :
            utils.message.closeProcessBarMessageBox("停止安装",
                                                    "本地OCR安装进行中\n确定要中止操作吗     ",
                                                    self)
        elif self.use_type == "input_images" :
            utils.message.closeProcessBarMessageBox("停止导入",
                                                    "图片导入进行中\n确定要中止操作吗     ",
                                                     self)
        if not self.stop_sign :
            event.ignore()


# 图片翻译进度条
class MangaProgressBar(QWidget) :

    def __init__(self, rate) :

        super(MangaProgressBar, self).__init__()
        self.rate = rate
        self.getInitConfig()
        self.ui()


    def ui(self) :

        # 窗口置顶
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        # 窗口尺寸及不可拉伸
        self.resize(self.window_width, self.window_height)
        self.setMaximumSize(QSize(self.window_width, self.window_height))
        self.setMinimumSize(QSize(self.window_width, self.window_height))
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint)
        # 窗口图标
        self.setWindowIcon(ui.static.icon.APP_LOGO_ICON)
        # 设置字体
        self.setStyleSheet("font: %spt '%s'; background-color: rgb(255, 255, 255);}"%(self.font_size, self.font_type))

        self.progress_bar = QProgressBar(self)
        self.customSetGeometry(self.progress_bar, 20, 10, 260, 10)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setStyleSheet("QProgressBar { background-color: rgba(62, 62, 62, 0.2); "
                                        "border-radius: 6px;}"
                                        "QProgressBar::chunk { background-color: %s; border-radius: 5px;}"
                                        %(self.color_2))
        self.progress_bar.setValue(0)

        self.progress_label = QLabel(self)
        self.customSetGeometry(self.progress_label, 240, 25, 150, 20)
        self.progress_label.setStyleSheet("color: %s"%self.color_2)

        self.file_size_label = QLabel(self)
        self.customSetGeometry(self.file_size_label, 30, 25, 150, 20)
        self.file_size_label.setStyleSheet("color: %s"%self.color_2)

        widget = QWidget(self)
        self.customSetGeometry(widget, 15, 40, 300, 200)
        layout = QGridLayout(self)
        widget.setLayout(layout)

        label = QLabel(self)
        label.setStyleSheet("color: %s"%self.color_2)
        label.resize(QSize(100*self.rate, 20*self.rate))
        label.setText("文字识别")
        layout.addWidget(label, 0, 0)

        label = QLabel(self)
        label.setStyleSheet("color: %s"%self.color_2)
        label.resize(QSize(100*self.rate, 20*self.rate))
        label.setText("文字翻译")
        layout.addWidget(label, 1, 0)

        label = QLabel(self)
        label.setStyleSheet("color: %s"%self.color_2)
        label.resize(QSize(100*self.rate, 20*self.rate))
        label.setText("文字消除")
        layout.addWidget(label, 2, 0)

        label = QLabel(self)
        label.setStyleSheet("color: %s"%self.color_2)
        label.resize(QSize(100*self.rate, 20*self.rate))
        label.setText("文字渲染")
        layout.addWidget(label, 3, 0)

        if not os.path.exists(LOADING_PATH) :
            with open(LOADING_PATH, "wb") as file :
                file.write(base64.b64decode(ui.static.icon.LOADING_GIF))
        self.loading_movie = QMovie(LOADING_PATH)
        self.loading_movie.setScaledSize(QSize(50*self.rate, 50*self.rate))
        self.loading_movie.start()

        self.ocr_icon_label = QLabel(self)
        self.ocr_icon_label.resize(QSize(100*self.rate, 20*self.rate))
        self.ocr_icon_label.setAlignment(Qt.AlignCenter)
        self.ocr_icon_label.setMovie(self.loading_movie)
        layout.addWidget(self.ocr_icon_label, 0, 1)

        self.trans_icon_label = QLabel(self)
        self.trans_icon_label.resize(QSize(100*self.rate, 20*self.rate))
        self.trans_icon_label.setAlignment(Qt.AlignCenter)
        self.trans_icon_label.setMovie(self.loading_movie)
        layout.addWidget(self.trans_icon_label, 1, 1)

        self.ipt_icon_label = QLabel(self)
        self.ipt_icon_label.resize(QSize(100*self.rate, 20*self.rate))
        self.ipt_icon_label.setAlignment(Qt.AlignCenter)
        self.ipt_icon_label.setMovie(self.loading_movie)
        layout.addWidget(self.ipt_icon_label, 2, 1)

        self.rdr_icon_label = QLabel(self)
        self.rdr_icon_label.resize(QSize(100*self.rate, 20*self.rate))
        self.rdr_icon_label.setAlignment(Qt.AlignCenter)
        self.rdr_icon_label.setMovie(self.loading_movie)
        layout.addWidget(self.rdr_icon_label, 3, 1)

        self.ocr_time_label = QLabel(self)
        self.ocr_time_label.resize(QSize(100*self.rate, 20*self.rate))
        self.ocr_time_label.setStyleSheet("color: %s"%self.color_2)
        self.ocr_time_label.setText("耗时 - s")
        layout.addWidget(self.ocr_time_label, 0, 2, 1, 2)

        self.trans_time_label = QLabel(self)
        self.trans_time_label.resize(QSize(100*self.rate, 20*self.rate))
        self.trans_time_label.setStyleSheet("color: %s"%self.color_2)
        self.trans_time_label.setText("耗时 - s")
        layout.addWidget(self.trans_time_label, 1, 2, 1, 2)

        self.ipt_time_label = QLabel(self)
        self.ipt_time_label.resize(QSize(100*self.rate, 20*self.rate))
        self.ipt_time_label.setStyleSheet("color: %s"%self.color_2)
        self.ipt_time_label.setText("耗时 - s")
        layout.addWidget(self.ipt_time_label, 2, 2, 1, 2)

        self.rdr_time_label = QLabel(self)
        self.rdr_time_label.resize(QSize(100*self.rate, 20*self.rate))
        self.rdr_time_label.setStyleSheet("color: %s"%self.color_2)
        self.rdr_time_label.setText("耗时 - s")
        layout.addWidget(self.rdr_time_label, 3, 2, 1, 2)

        # 翻译进度消息窗口
        self.message_text = QTextEdit(self)
        self.customSetGeometry(self.message_text, 10, 240, 280, 150)
        self.message_text.setWordWrapMode(QTextOption.WrapAnywhere)
        self.message_text.setLineWrapMode(QTextEdit.NoWrap)
        self.message_text.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.message_text.setReadOnly(True)
        self.message_text.setStyleSheet("background-color: rgb(224, 224, 224);"
                                        "font: 9pt '华康方圆体W7';"
                                        "border: 1px solid black;")
        self.message_text.setCursor(ui.static.icon.SELECT_CURSOR)

        self.paintProgressBar(0, "0/0")


    # 根据分辨率定义控件位置尺寸
    def customSetGeometry(self, object, x, y, w, h) :

        object.setGeometry(QRect(int(x * self.rate),
                                 int(y * self.rate),
                                 int(w * self.rate),
                                 int(h * self.rate)))


    # 初始化配置
    def getInitConfig(self):

        # 界面字体
        self.font_type = "华康方圆体W7"
        # 界面字体大小
        self.font_size = 10
        # 灰色
        self.color_1 = "#595959"
        # 蓝色
        self.color_2 = "#5B8FF9"
        # 界面尺寸
        self.window_width = int(300 * self.rate)
        self.window_height = int(400 * self.rate)
        # 结束信号
        self.finish_sign = False
        # 中止信号
        self.stop_sign = False


    # 绘制进度信息
    def paintProgressBar(self, int_val, str_val) :

        self.progress_label.setText("{}%".format(int_val))
        self.progress_bar.setValue(int_val)
        self.file_size_label.setText(str_val)

        if int_val < 100 :
            self.ocr_icon_label.setMovie(self.loading_movie)
            self.trans_icon_label.setMovie(self.loading_movie)
            self.ipt_icon_label.setMovie(self.loading_movie)
            self.rdr_icon_label.setMovie(self.loading_movie)

            self.ocr_time_label.setText("耗时 - s")
            self.trans_time_label.setText("耗时 - s")
            self.ipt_time_label.setText("耗时 - s")
            self.rdr_time_label.setText("耗时 - s")


    # 修改窗口标题
    def modifyTitle(self, title) :

        self.setWindowTitle(title)


    # 停止任务
    def stopProcess(self) :

        self.stop_sign = True


    # 绘制当前翻译状态
    def paintStatus(self, status_type, status_time, success_status) :

        if status_type == "ocr" :
            if success_status:
                self.ocr_icon_label.setPixmap(ui.static.icon.FINISH_PIXMAP)
            else:
                self.ocr_icon_label.setPixmap(ui.static.icon.FAIL_PIXMAP)
            self.ocr_time_label.setText("耗时 {} s".format(status_time))

        elif status_type == "trans" :
            if success_status:
                self.trans_icon_label.setPixmap(ui.static.icon.FINISH_PIXMAP)
            else:
                self.trans_icon_label.setPixmap(ui.static.icon.FAIL_PIXMAP)
            self.trans_time_label.setText("耗时 {} s".format(status_time))

        elif status_type == "ipt" :
            if success_status:
                self.ipt_icon_label.setPixmap(ui.static.icon.FINISH_PIXMAP)
            else:
                self.ipt_icon_label.setPixmap(ui.static.icon.FAIL_PIXMAP)
            self.ipt_time_label.setText("耗时 {} s".format(status_time))

        elif status_type == "rdr" :
            if success_status:
                self.rdr_icon_label.setPixmap(ui.static.icon.FINISH_PIXMAP)
            else :
                self.rdr_icon_label.setPixmap(ui.static.icon.FAIL_PIXMAP)
            self.rdr_time_label.setText("耗时 {} s".format(status_time))


    # 设置消息窗文本
    def setMessageText(self, text, color) :

        if not text :
            self.message_text.clear()
        else :
            self.message_text.insertHtml("<span style='color:{};'>{}</span>".format(color, text))
            self.message_text.insertHtml("<br>")
            cursor = self.message_text.textCursor()
            cursor.movePosition(QTextCursor.End)
            self.message_text.setTextCursor(cursor)


    # 窗口关闭处理
    def closeEvent(self, event) :

        if self.finish_sign :
            return
        utils.message.closeProcessBarMessageBox("停止翻译",
                                                "图片翻译进行中\n确定要中止操作吗     ",
                                                self)
        if not self.stop_sign :
            event.ignore()