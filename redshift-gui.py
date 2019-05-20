#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import subprocess
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class RedshiftGUI(QWidget):
  def __init__(self, parent = None):
    super(RedshiftGUI, self).__init__(parent)

    self.folder =  os.getenv('HOME') + '/redshift-gui/'
    self.temperaturePath = self.folder + 'colortemp'
    if os.path.exists(self.temperaturePath):
      with open(self.temperaturePath, 'r') as f:
        self.temperature = f.readline()
        if len(self.temperature) == 0:
          self.temperature = 6500
        else:
          self.temperature = int(self.temperature)
    else:
      self.temperature = 6500
      with open(self.temperaturePath, 'w') as f:
        f.write(str(self.temperature))

    self.setTemperature()

    layout = QVBoxLayout()
    self.l1 = QLabel("Temperature: " + str(self.temperature) + "K")
    self.l1.setAlignment(Qt.AlignCenter)
    layout.addWidget(self.l1)

    self.s1 = QSlider(Qt.Horizontal)
    self.s1.setMinimum(10)
    self.s1.setMaximum(70)
    self.s1.setValue(self.temperature/100)
    self.s1.setTickPosition(QSlider.TicksBelow)
    self.s1.setTickInterval(1)
    self.s1.setSingleStep(1)

    layout.addWidget(self.s1)
    self.s1.valueChanged.connect(self.valuechange)
    self.setLayout(layout)
    self.setWindowTitle("Redshift temperature changer")

  def setTemperature(self):
    subprocess.call('redshift -P -O ' + str(self.temperature) + ' >> /dev/null', shell=True)

  def valuechange(self):
    self.temperature = self.s1.value() * 100
    self.l1.setText("Temperature: " + str(self.temperature) + " K")
    self.setTemperature()

  def closeEvent(self, event):
    temperature = self.s1.value() * 100
    f = open(self.temperaturePath, 'w')
    f.write(str(self.temperature))
    f.close()


def main():
  app = QApplication(sys.argv)
  ex = RedshiftGUI()
  ex.resize(640, 75)
  ex.show()
  sys.exit(app.exec_())

if __name__ == '__main__':
  main()
