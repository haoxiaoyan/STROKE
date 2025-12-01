import sys

import joblib

from GUI import Ui_MainWindow
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
import numpy as np

metrics = {}
# 读取模型
# with open('./lightGBM_model.pkl', 'rb') as file:
#     loaded_model = pickle.load(file)

class MyGUIDemo(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MyGUIDemo, self).__init__()
        self.setupUi(self)
        self.signal(self)
        self.WidgetsUi(self)

    def WidgetsUi(self, MainWindow):
        # lineEdit
        self.lineEdit_1.setPlaceholderText('Please enter!(%)')
        self.lineEdit_2.setPlaceholderText('Please enter!(×10^9/L)')
        self.lineEdit_3.setPlaceholderText('Please enter!(g/L)')
        self.lineEdit_4.setPlaceholderText('Please enter!(mg/L)')
        self.lineEdit_5.setPlaceholderText('Please enter!(mmol/L)')
        self.lineEdit_6.setPlaceholderText('Please enter!(mmol/L)')
        self.lineEdit_7.setPlaceholderText('Please enter!(mmol/L)')
        self.lineEdit_8.setPlaceholderText('Please enter!(μmol/L)')
        self.lineEdit_9.setPlaceholderText('Please enter!(μg/mL)')
        self.lineEdit_10.setPlaceholderText('Please enter!(mg/L FEU)')

    def signal(self, MainWindow):
        # Button
        self.pushButton.setEnabled(False)
        self.pushButton.clicked.connect(self.generate_result)
        # lineedit
        self.lineEdit_1.textChanged.connect(self.check_input_func)
        self.lineEdit_2.textChanged.connect(self.check_input_func)
        self.lineEdit_3.textChanged.connect(self.check_input_func)
        self.lineEdit_4.textChanged.connect(self.check_input_func)
        self.lineEdit_5.textChanged.connect(self.check_input_func)
        self.lineEdit_6.textChanged.connect(self.check_input_func)
        self.lineEdit_7.textChanged.connect(self.check_input_func)
        self.lineEdit_8.textChanged.connect(self.check_input_func)
        self.lineEdit_9.textChanged.connect(self.check_input_func)
        self.lineEdit_10.textChanged.connect(self.check_input_func)

    def generate_result(self):
        mt = []  # 用于存各项指标
        metrics['NEUT%'] = float(self.lineEdit_1.text())
        metrics['WBC'] = float(self.lineEdit_2.text())
        metrics['TP'] = float(self.lineEdit_3.text())
        metrics['CysC'] = float(self.lineEdit_4.text())
        metrics['K⁺'] = float(self.lineEdit_5.text())
        metrics['Na⁺'] = float(self.lineEdit_6.text())
        metrics['Cl⁻'] = float(self.lineEdit_7.text())
        metrics['UA'] = float(self.lineEdit_8.text())
        metrics['FDP'] = float(self.lineEdit_9.text())
        metrics['D-Dimer'] = float(self.lineEdit_10.text())

        print(metrics)
        # 将字典中的值装入tensor, 同时进行预测
        for value in metrics.values():
            mt.append(value)
        mt_str = str(mt)
        c = np.array([mt])
        print(c)
        #加载模型
        model = joblib.load("lightGBM_model.pkl")
        predicted = model.predict_proba(c)
        print(predicted)
        #将概率变成4位小数
        number = predicted[0][1]
        number_lst = str(number).split(".")
        if "." in str(number):
            new_number = number_lst[0] + "." + number_lst[1][:4]
        else:
            new_number = number_lst[0] + "." + "0" * 4

        new_number = float(new_number)*100
        isDisease_str = str('%.2f' % new_number) + "%"
        QMessageBox.warning(self,
                                'Your preliminary prediction results',
                                "The indicators you entered are：\n" + mt_str + '\n' + "Your probability of IS is：" + isDisease_str)
        self.lineEdit_1.clear()
        self.lineEdit_2.clear()
        self.lineEdit_3.clear()
        self.lineEdit_4.clear()
        self.lineEdit_5.clear()
        self.lineEdit_6.clear()
        self.lineEdit_7.clear()
        self.lineEdit_8.clear()
        self.lineEdit_9.clear()
        self.lineEdit_10.clear()

    def check_input_func(self):
        if self.lineEdit_1.text() and self.lineEdit_2.text() and \
                self.lineEdit_3.text() and self.lineEdit_4.text() and \
                self.lineEdit_5.text() and self.lineEdit_6.text() and \
                self.lineEdit_7.text() and self.lineEdit_8.text() and \
                self.lineEdit_9.text() and self.lineEdit_10.text():
                self.pushButton.setEnabled(True)
        else:
            self.pushButton.setEnabled(False)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyGUIDemo()
    window.setWindowIcon(QtGui.QIcon("E:\Github代码管理\Keras_tf2\心脏病预测\Heart.ico"))
    window.setWindowTitle("LightGBM-based Early Prediction System for Stroke Types")
    window.show()
    sys.exit(app.exec_())
