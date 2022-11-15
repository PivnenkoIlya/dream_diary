import csv
import sqlite3
import sys

from PyQt5 import uic
from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5 import QtCore, QtGui, QtWidgets


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main_design.ui', self)

        self.button_add.clicked.connect(self.add)
        self.deleteAll_button.clicked.connect(self.open_dialog)
        self.button_what.clicked.connect(self.open_what)

        self.con = sqlite3.connect('dream_database.db')
        self.cur = self.con.cursor()
        try:
            self.result = self.cur.execute("""SELECT * FROM info ORDER BY id DESC""").fetchall()
            self.count_label.setText(str(len(self.result)))
            if len(self.result) == 0:
                self.text.setVisible(True)
            else:
                self.text.setVisible(False)
        except Exception:
            self.result = []
            print('такой таблицы нет!')
            self.text.setVisible(True)

        for i in range(len(self.result)):
            self.row = QtWidgets.QGroupBox(self.scrollAreaWidgetContents_3)
            self.row.setGeometry(QtCore.QRect(20, 170 * (i + 1), 601, 141))
            self.row.setStyleSheet("border: 2px solid yellow;")
            self.row.setTitle("")
            self.row.setFlat(False)
            self.row.setObjectName("row")
            self.date_dream = QtWidgets.QLabel(self.row)
            self.date_dream.setGeometry(QtCore.QRect(20, 20, 221, 41))
            font = QtGui.QFont()
            font.setPointSize(15)
            self.date_dream.setFont(font)
            self.date_dream.setStyleSheet("color:white;\n"
                                          "    border: none;\n"
                                          "\n"
                                          "            ")
            self.date_dream.setObjectName("date_dream")
            self.name_dream = QtWidgets.QLabel(self.row)
            self.name_dream.setGeometry(QtCore.QRect(200, 20, 300, 41))
            font = QtGui.QFont()
            font.setPointSize(15)
            self.name_dream.setFont(font)
            self.name_dream.setStyleSheet("color:white;\n"
                                          "            \n"
                                          "    border: none;\n"
                                          "")
            self.name_dream.setObjectName("name_dream")
            self.button_read = QtWidgets.QPushButton(self.row)
            self.button_read.setGeometry(QtCore.QRect(20, 80, 561, 41))
            font = QtGui.QFont()
            font.setPointSize(12)
            font.setBold(False)
            font.setItalic(False)
            font.setUnderline(False)
            font.setWeight(50)
            font.setStrikeOut(False)
            font.setKerning(True)
            self.button_read.setFont(font)
            self.button_read.setStyleSheet("border-color: #fff;\n"
                                           "border-radius: 20px;\n"
                                           "color: #fff")
            self.button_read.setObjectName(f"button_read_{self.result[i][-1] + 1}")
            self.deleteRow_button = QtWidgets.QPushButton(self.row)
            self.deleteRow_button.setGeometry(QtCore.QRect(530, 20, 41, 41))
            font = QtGui.QFont()
            font.setPointSize(22)
            self.deleteRow_button.setFont(font)
            self.deleteRow_button.setStyleSheet("color: rgb(255, 255, 255);\n"
                                                "border-color: rgb(255, 0, 0);")
            self.deleteRow_button.setObjectName(f"delete_button_{self.result[i][-1]}")

            #########

            self.date_dream.setText(f'{self.result[i][1]}')
            self.name_dream.setText(f'{self.result[i][0]}')
            self.button_read.setText(f"читать ->")
            self.button_read.clicked.connect(self.read_dream)
            self.deleteRow_button.setText("X")
            self.deleteRow_button.clicked.connect(self.open_dialog)

    ###############----functions----#######################

    def add(self):
        self.close()
        self.second_window = Second_window()
        self.second_window.show()

    def open_dream(self):
        self.second_window = Second_window()
        self.second_window.show()

    def _update(self):
        self.a = MainWindow()
        self.a.show()

    def read_dream(self):
        temp = self.sender().objectName().split('_')[-1]
        self.second_window = Second_window('read', temp, 'change')
        self.second_window.show()
        self.close()

    def open_dialog(self):
        self.dialog = QMessageBox(self)
        self.dialog.setIcon(QMessageBox.Warning)
        self.dialog.setStyleSheet("color:#000")
        self.dialog.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        if self.sender().objectName() != "deleteAll_button":
            self.count = int(self.sender().objectName().split('_')[-1])
            self.dialog.setText("Вы уверены, что хотите удалить сон?")
            self.dialog.buttonClicked.connect(self.delete_row)
            self.dialog.exec_()
        else:
            if len(self.cur.execute("""SELECT * FROM info""").fetchall()):
                self.dialog.setText("Вы уверены, что хотите удалить сны?")
                self.dialog.buttonClicked.connect(self.delete_all)
                self.dialog.exec_()

    def delete_all(self, dialog_button):
        if dialog_button.text() == "OK":
            self.con = sqlite3.connect('dream_database.db')
            self.cur = self.con.cursor()
            try:
                self.cur.execute(
                    """delete from info""")
                self.con.commit()
                self.close()
                self.a = MainWindow()
                self.a.show()
            except Exception:
                print('error')

    def delete_row(self, dialog_button):
        if dialog_button.text() == "OK":

            print(self.count)
            self.con = sqlite3.connect('dream_database.db')
            self.cur = self.con.cursor()
            self.cur.execute(
                f"""delete from info where id = {self.count}""")
            self.con.commit()

            self.result = self.cur.execute("""select * from info""").fetchall()
            for i in range(len(self.result)):
                old_id = self.result[i][-1]
                self.cur.execute(f"""update info set id = {i} where id = {old_id}""")
                self.con.commit()
            self.result = self.cur.execute("""select * from info""").fetchall()

            self.close()
            self.a = MainWindow()
            self.a.show()

    def open_what(self):
        self.what = What_is_this()
        self.what.show()


########################################################################
########################################################################
########################################################################

class Second_window(MainWindow):
    def __init__(self, do_read='no read', count='', do_change=''):
        super().__init__()
        uic.loadUi('design_second.ui', self)
        self.do_read = do_read
        self.do_change = do_change
        if self.do_read == 'read':
            self.count = int(count) - 1
            self.read_row()
            self.button_save.setText('изменить')
        else:
            date = QDate.currentDate()
            self.date_dream_input.setDisplayFormat("dd.MM.yyyy")
            self.date_dream_input.setDate(date)

        self.button_save.clicked.connect(self.save_dream)
        self.deleteText.clicked.connect(self.text_delete)
        self.button_goToBack.clicked.connect(self.open_dialog)
        self.tasks = MainWindow()

    ###############----functions----#######################

    def text_delete(self):
        self.story_input.clear()

    def save_dream(self):
        if self.do_change == '':
            self.con = sqlite3.connect('dream_database.db')
            self.cur = self.con.cursor()
            if self.yes.isChecked():
                temp = 'true'
            else:
                temp = 'false'
            self.cur.execute(
                """create table if not exists info(name STRING, date STRING, story STRING, keywords STRING, os STRING, id int)""")
            self.count = len(self.cur.execute("""select * from info""").fetchall())
            self.cur.execute(
                f"""INSERT INTO info('name', 'date', 'story', 'keywords', 'os', 'id')
                         VALUES(
                         '{self.name_dream_input.text()}', 
                         '{self.date_dream_input.text()}', 
                         '{self.story_input.toPlainText()}', 
                         '{self.keywords.toPlainText()}', 
                         '{temp}',
                         {self.count})""")
            self.con.commit()
            self.close()
            self.tasks._update()


        else:
            if self.yes.isChecked():
                temp = 'true'
            else:
                temp = 'false'
            self.con = sqlite3.connect('dream_database.db')
            self.cur = self.con.cursor()

            self.cur.execute(f"""update info set
            name = '{self.name_dream_input.text()}',
            date = '{self.date_dream_input.text()}',
            story = '{self.story_input.toPlainText()}',
            keywords = '{self.keywords.toPlainText()}', 
            os = '{temp}' where id = {self.count}""")
            self.con.commit()
            self.close()
            self.tasks._update()

    def read_row(self):
        self.con = sqlite3.connect('dream_database.db')
        self.cur = self.con.cursor()
        self.result = self.cur.execute("""select * from info""").fetchall()
        self.name_dream_input.setText(str(self.result[self.count][0]))

        qdate = QtCore.QDate.fromString(self.result[self.count][1], "dd.MM.yyyy")
        self.date_dream_input.setDisplayFormat("dd.MM.yyyy")
        self.date_dream_input.setDate(qdate)

        self.story_input.setText(str(self.result[self.count][2]))

        self.keywords.setText(str(self.result[self.count][3]))

        if self.result[self.count][4] == 'true':
            self.yes.setChecked(True)
        else:
            self.no.setChecked(True)

    def open_dialog(self):
        self.dialog = QMessageBox(self)
        self.dialog.setIcon(QMessageBox.Warning)
        self.dialog.setStyleSheet("color:#000")
        self.dialog.setText("Вы уверены, что хотите выйти?")
        self.dialog.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        self.dialog.buttonClicked.connect(self.go_back)
        self.dialog.exec_()

    def go_back(self, dialog_button):
        if dialog_button.text() == "OK":
            self.close()
            self.tasks._update()


class What_is_this(MainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('what_is_this.ui', self)
        self.setObjectName("Form")
        self.resize(681, 842)
        self.setMinimumSize(QtCore.QSize(681, 842))
        self.setMaximumSize(QtCore.QSize(681, 842))
        font = QtGui.QFont()
        font.setFamily("Book Antiqua")
        self.setFont(font)
        self.setStyleSheet("font-family: \"Book Antiqua\";\n"
                           "\n"
                           "background-color: transparent; ")
        self.tabs = QtWidgets.QTabWidget(self)
        self.tabs.setGeometry(QtCore.QRect(0, 0, 691, 851))
        font = QtGui.QFont()
        font.setFamily("Book Antiqua")
        font.setPointSize(15)
        self.tabs.setFont(font)
        self.tabs.setStyleSheet("\n"
                                "\n"
                                "QTabBar::tab{\n"
                                "    color: rgb(255, 255, 255);;\n"
                                "    background-color: rgb(170, 170, 170);\n"
                                "\n"
                                "}\n"
                                "\n"
                                "QTabBar::tab:SELECTED{\n"
                                "    background-color: rgb(255, 114, 116);\n"
                                "}\n"
                                "\n"
                                "QTabWidget::pane{\n"
                                "    border:none;\n"
                                "}")
        self.tabs.setIconSize(QtCore.QSize(60, 20))
        self.tabs.setUsesScrollButtons(False)
        self.tabs.setDocumentMode(False)
        self.tabs.setTabsClosable(False)
        self.tabs.setObjectName("tabs")
        self.tab1 = QtWidgets.QWidget()
        self.tab1.setStyleSheet("border:1px;")
        self.tab1.setObjectName("tab1")
        self.title = QtWidgets.QLabel(self.tab1)
        self.title.setGeometry(QtCore.QRect(100, 30, 471, 39))
        font = QtGui.QFont()
        font.setFamily("Book Antiqua")
        font.setPointSize(20)
        font.setBold(True)
        font.setItalic(True)
        font.setUnderline(False)
        font.setWeight(75)
        font.setStrikeOut(False)
        font.setKerning(True)
        self.title.setFont(font)
        self.title.setObjectName("title")
        self.text = QtWidgets.QPlainTextEdit(self.tab1)
        self.text.setGeometry(QtCore.QRect(40, 90, 581, 701))
        font = QtGui.QFont()
        font.setFamily("Book Antiqua")
        font.setPointSize(15)
        self.text.setFont(font)
        self.text.setStyleSheet("background-color:transparent;")
        self.text.setReadOnly(True)
        self.text.setObjectName("text")
        self.button_goToBack = QtWidgets.QPushButton(self.tab1)
        self.button_goToBack.setGeometry(QtCore.QRect(190, 730, 291, 41))
        font = QtGui.QFont()
        font.setFamily("Book Antiqua")
        font.setPointSize(16)
        self.button_goToBack.setFont(font)
        self.button_goToBack.setStyleSheet("border-radius: 20px;\n"
                                           "\n"
                                           "background-color: rgb(255, 114, 116);\n"
                                           "color: white;")
        self.button_goToBack.setObjectName("button_goToBack")
        self.button_readMore = QtWidgets.QPushButton(self.tab1)
        self.button_readMore.setGeometry(QtCore.QRect(290, 690, 201, 20))
        font = QtGui.QFont()
        font.setFamily("Book Antiqua")
        font.setPointSize(13)
        font.setBold(True)
        font.setWeight(75)
        self.button_readMore.setFont(font)
        self.button_readMore.setStyleSheet("\n"
                                           "color: rgb(255, 114, 116);")
        self.button_readMore.setObjectName("button_readMore")
        self.more_by_os = QtWidgets.QGroupBox(self.tab1)
        self.more_by_os.setEnabled(True)
        self.more_by_os.setGeometry(QtCore.QRect(0, 0, 681, 811))
        self.more_by_os.setStyleSheet("background-color: rgb(94, 94, 94);")
        self.more_by_os.setTitle("")
        self.more_by_os.setFlat(False)
        self.more_by_os.setCheckable(False)
        self.more_by_os.setObjectName("more_by_os")
        self.text_more_2 = QtWidgets.QPlainTextEdit(self.more_by_os)
        self.text_more_2.setGeometry(QtCore.QRect(33, 66, 631, 721))
        font = QtGui.QFont()
        font.setFamily("Book Antiqua")
        font.setPointSize(20)
        self.text_more_2.setFont(font)
        self.text_more_2.setStyleSheet("color: rgb(255, 255, 255);")
        self.text_more_2.setReadOnly(True)
        self.text_more_2.setObjectName("text_more_2")
        self.button_goToBack_3 = QtWidgets.QPushButton(self.more_by_os)
        self.button_goToBack_3.setGeometry(QtCore.QRect(180, 20, 291, 41))
        font = QtGui.QFont()
        font.setFamily("Book Antiqua")
        font.setPointSize(16)
        self.button_goToBack_3.setFont(font)
        self.button_goToBack_3.setAcceptDrops(False)
        self.button_goToBack_3.setAutoFillBackground(False)
        self.button_goToBack_3.setStyleSheet("border-radius: 20px;\n"
                                             "\n"
                                             "background-color: rgb(255, 114, 116);\n"
                                             "color: white;")
        self.button_goToBack_3.setObjectName("button_goToBack_3")
        self.tabs.addTab(self.tab1, "")
        self.tab2 = QtWidgets.QWidget()
        self.tab2.setStyleSheet("border:1px;")
        self.tab2.setObjectName("tab2")
        self.button_goToBack_2 = QtWidgets.QPushButton(self.tab2)
        self.button_goToBack_2.setGeometry(QtCore.QRect(190, 700, 291, 41))
        font = QtGui.QFont()
        font.setFamily("Book Antiqua")
        font.setPointSize(16)
        self.button_goToBack_2.setFont(font)
        self.button_goToBack_2.setStyleSheet("border-radius: 20px;\n"
                                             "\n"
                                             "background-color: rgb(255, 114, 116);\n"
                                             "color: white;")
        self.button_goToBack_2.setObjectName("button_goToBack_2")
        self.img = QtWidgets.QLabel(self.tab2)
        self.img.setGeometry(QtCore.QRect(10, 30, 281, 271))
        self.img.setStyleSheet("\n"
                               "border-radius: 25px;\n"
                               "border:none;")
        self.img.setText("")
        self.img.setPixmap(QtGui.QPixmap("img/photo_2022-10-31_19-25-30.jpg"))
        self.img.setScaledContents(True)
        self.img.setWordWrap(False)
        self.img.setOpenExternalLinks(False)
        self.img.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse)
        self.img.setObjectName("img")
        self.info = QtWidgets.QPlainTextEdit(self.tab2)
        self.info.setGeometry(QtCore.QRect(350, 36, 301, 261))
        font = QtGui.QFont()
        font.setFamily("Book Antiqua")
        font.setPointSize(20)
        self.info.setFont(font)
        self.info.setObjectName("info")
        self.subscribe_me = QtWidgets.QLabel(self.tab2)
        self.subscribe_me.setGeometry(QtCore.QRect(90, 330, 476, 41))
        font = QtGui.QFont()
        font.setFamily("Book Antiqua")
        font.setPointSize(20)
        self.subscribe_me.setFont(font)
        self.subscribe_me.setOpenExternalLinks(False)
        self.subscribe_me.setObjectName("subscribe_me")
        self.for_vk = QtWidgets.QLabel(self.tab2)
        self.for_vk.setGeometry(QtCore.QRect(30, 410, 354, 28))
        font = QtGui.QFont()
        font.setFamily("Book Antiqua")
        font.setPointSize(14)
        self.for_vk.setFont(font)
        self.for_vk.setStyleSheet("")
        self.for_vk.setOpenExternalLinks(True)
        self.for_vk.setObjectName("for_vk")
        self.for_vk_2 = QtWidgets.QLabel(self.tab2)
        self.for_vk_2.setGeometry(QtCore.QRect(30, 480, 436, 28))
        font = QtGui.QFont()
        font.setFamily("Book Antiqua")
        font.setPointSize(14)
        self.for_vk_2.setFont(font)
        self.for_vk_2.setStyleSheet("")
        self.for_vk_2.setOpenExternalLinks(True)
        self.for_vk_2.setObjectName("for_vk_2")
        self.tabs.addTab(self.tab2, "")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.create_csv = QtWidgets.QPushButton(self.tab)
        self.create_csv.setGeometry(QtCore.QRect(240, 50, 211, 51))
        font = QtGui.QFont()
        font.setFamily("Book Antiqua")
        font.setPointSize(12)
        self.create_csv.setFont(font)
        self.create_csv.setStyleSheet("background-color: rgb(255, 114, 116);\n"
                                      "color: rgb(255, 255, 255);\n"
                                      "")
        self.create_csv.setObjectName("create_csv")
        self.successful_label = QtWidgets.QLabel(self.tab)
        self.successful_label.setGeometry(QtCore.QRect(120, 140, 423, 41))
        font = QtGui.QFont()
        font.setFamily("Book Antiqua")
        font.setPointSize(20)
        self.successful_label.setFont(font)
        self.successful_label.setObjectName("successful_label")
        self.button_goToBack_4 = QtWidgets.QPushButton(self.tab)
        self.button_goToBack_4.setGeometry(QtCore.QRect(190, 650, 291, 41))
        font = QtGui.QFont()
        font.setFamily("Book Antiqua")
        font.setPointSize(16)
        self.button_goToBack_4.setFont(font)
        self.button_goToBack_4.setStyleSheet("border-radius: 20px;\n"
                                             "\n"
                                             "background-color: rgb(255, 114, 116);\n"
                                             "color: white;")
        self.button_goToBack_4.setObjectName("button_goToBack_4")
        self.tabs.addTab(self.tab, "")
        self.bg_all = QtWidgets.QLabel(self)
        self.bg_all.setGeometry(QtCore.QRect(-90, -40, 1000, 1000))
        self.bg_all.setMinimumSize(QtCore.QSize(681, 842))
        self.bg_all.setMaximumSize(QtCore.QSize(1000, 1000))
        font = QtGui.QFont()
        font.setFamily("Book Antiqua")
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.bg_all.setFont(font)
        self.bg_all.setMouseTracking(False)
        self.bg_all.setTabletTracking(False)
        self.bg_all.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.bg_all.setAcceptDrops(False)
        self.bg_all.setToolTipDuration(0)
        self.bg_all.setAutoFillBackground(False)
        self.bg_all.setText("")
        self.bg_all.setPixmap(
            QtGui.QPixmap("img/1643604187_13-phonoteka-org-p-gradientnii-fon-dlya-prezentatsii-13.jpg"))
        self.bg_all.setScaledContents(True)
        self.bg_all.setObjectName("bg_all")
        self.bg_all.raise_()
        self.tabs.raise_()

        self.tabs.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(self)

        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Form", "Form"))
        self.title.setText(_translate("Form", "Для чего нужен дневник снов?"))
        self.text.setPlainText(_translate("Form",
                                          "Мало кто из нас записывает свои сновидения, а ведь это настолько просто... Но зачем всё это нужно?\n"
                                          "\n"
                                          "1) Улучшается сновидческая память\n"
                                          "\n"
                                          "2) По мере улучшения памяти, вы начнёте запоминать сюжет все лучше и лучше. Это даёт вам возможность извлекать из снов замечательные идеи, которые способны кардинально изменить вашу жизнь\n"
                                          "\n"
                                          "3) Сны становятся ярче, реалистичнее и интереснее\n"
                                          "\n"
                                          "4) Самое главное - вы научитесь выходить в осознанный сон, то есть попадать в пространство, в котором возможно всё: от проходов сквозь стену до познания себя и окружаещего мира!"))
        self.button_goToBack.setText(_translate("Form", "назад"))
        self.button_readMore.setText(_translate("Form", "читать подробнее"))
        self.text_more_2.setPlainText(_translate("Form",
                                                 " Осознанный сон (lucid dream, ОС) — тип сна, в котором человек понимает, что находится в сновидении и может управлять происходящим: своими действиями, поведением окружающих и законами, которым подчиняется мир внутри сна. При этом у человека сохраняются воспоминания о реальной жизни и характеристики личности.\n"
                                                 "\n"
                                                 " Практически все люди видят сны, но забывают их почти полностью в течение десяти минут после пробуждения. Сновидения случаются даже у слепорожденных людей, правда, вместо привычных большинству образов, они чувствуют во сне преимущественно запахи и тактильные ощущения. Универсального понимания того, почему мы видим сны, пока нет, но есть несколько теорий.\n"
                                                 "\n"
                                                 " На сцене обычного сна человек предстает играющим зрителем, который, в отличие от актера или режиссера, не может влиять на сюжет или действия персонажа. В ОС сновидящий выступает как играющий сценарист, управляя сюжетом, декорациями и собственным поведением.\n"
                                                 "\n"
                                                 " Осознанный сон дает даже большие возможности для контроля над ситуацией, чем сама реальность, поскольку в нем можно влиять на внешние обстоятельства — как на других персонажей, так и на законы физики."))
        self.button_goToBack_3.setText(_translate("Form", "назад"))
        self.tabs.setTabText(self.tabs.indexOf(self.tab1), _translate("Form", "О проекте"))
        self.button_goToBack_2.setText(_translate("Form", "назад"))
        self.info.setPlainText(_translate("Form", "Пивненко Илья\n"
                                                  "\n"
                                                  "Дата создания:\n"
                                                  "     10.11.2022"))
        self.subscribe_me.setText(_translate("Form", "Подпишитись на мои соцсети:"))
        self.for_vk.setText(_translate("Form",
                                       "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                       "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                       "p, li { white-space: pre-wrap; }\n"
                                       "</style></head><body style=\" font-family:\'Book Antiqua\'; font-size:14pt; font-weight:400; font-style:normal;\">\n"
                                       "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-style:italic;\">ВК: </span><a href=\"https://vk.com/id458794280\"><span style=\" font-weight:600; font-style:italic; text-decoration: underline; color:#0055ff;\">https://vk.com/id458794280</span></a></p></body></html>"))
        self.for_vk_2.setText(_translate("Form",
                                         "<html><head/><body><p>Telegram: <a href=\"https://t.me/DeadRiderGames\"><span style=\" font-weight:600; text-decoration: underline; color:#0055ff;\">https://t.me/DeadRiderGames</span></a></p></body></html>"))
        self.tabs.setTabText(self.tabs.indexOf(self.tab2), _translate("Form", "Об авторе"))
        self.create_csv.setText(_translate("Form", "Создать CSV файл"))
        self.successful_label.setText(_translate("Form", "CSV файл успешно создан!"))
        self.button_goToBack_4.setText(_translate("Form", "назад"))
        self.tabs.setTabText(self.tabs.indexOf(self.tab), _translate("Form", "Дополнительно"))

        self.more_by_os.setVisible(False)
        self.successful_label.setVisible(False)

        self.button_readMore.clicked.connect(self.read_more)
        self.button_goToBack.clicked.connect(self.go_back)
        self.button_goToBack_2.clicked.connect(self.go_back)
        self.button_goToBack_4.clicked.connect(self.go_back)
        self.button_goToBack_3.clicked.connect(self.go_backToTabs)
        self.create_csv.clicked.connect(self.createCsv)

    def go_back(self):
        self.close()

    def read_more(self):
        self.more_by_os.setVisible(True)

    def go_backToTabs(self):
        self.more_by_os.setVisible(False)

    def createCsv(self):
        self.result = self.cur.execute("""select * from info""").fetchall()

        with open("info.csv", mode="w", encoding='utf-8') as w_file:
            file_writer = csv.writer(w_file, delimiter=";", lineterminator="\r")

            file_writer.writerow(["название", "дата", "сюжет", "ключевые слова", "id"])
            for i in self.result:
                file_writer.writerow([i[0], i[1], i[2], i[3], i[4]])
        self.successful_label.setVisible(True)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())
