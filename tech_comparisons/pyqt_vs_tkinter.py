# tech_comparisons/pyqt_vs_tkinter.py

# Tkinter Approach
# Very basic and built-in, but the UI looks outdated and layout management is hard to scale for the WorkClaim app
import tkinter as tk
root = tk.Tk()
root.title("WorkClaim - Tkinter Test")
tk.Label(root, text="Facility Selection").pack()
root.mainloop()

# PyQt5 Approach (Our Choice) 
# We chose PyQt because it's object oriented, 
# has much better layout management handles complex UIs better for our facility reservation system
from PyQt5.QtWidgets 
import QApplication, QWidget, QLabel, QVBoxLayout
import sys
app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle('WorkClaim - PyQt')
layout = QVBoxLayout()
layout.addWidget(QLabel('Facility Selection'))
window.setLayout(layout)
window.show()
sys.exit(app.exec_())
