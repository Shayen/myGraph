#!/usr/bin/python
import os
import sys
# import importlib
import imp
import inspect
import traceback

from NodeGraphQt import NodeGraph, Node, Backdrop, setup_context_menu
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2 import QtWidgets, QtCore

# from widget import OptionBox
import command

nodesDir = os.path.dirname(__file__).replace('\\','/') + '/myGraph/custom_nodes'

class MyGraphWindow(QMainWindow):

    def __init__(self, parent = None):
        super(MyGraphWindow, self).__init__(parent)
        mainwidget = QWidget(self)
        self.menubar = QMenuBar(self)
        self.menubar.addAction('&Files')
        self.menubar.addAction('&Edit')
        self.run_menu = self.menubar.addAction('&Run')
        mainLayout = QHBoxLayout()

        # main UI
        splitter1 = QSplitter(Qt.Horizontal)
        self.graph =  NodeGraph()
        # setup_context_menu(self.graph)
        self.viewer = self.graph.viewer()

        mainwidget.setLayout(mainLayout)
        splitter1.addWidget(self.viewer)
        self.setCentralWidget(mainwidget)
        self.setMenuBar(self.menubar)

        # set up default menu and commands.
        setup_context_menu(self.graph)

        # show the properties bin when a node is "double clicked" in the graph.
        # properties_bin = self.graph.properties_bin()
        # properties_bin.setWindowFlags(QtCore.Qt.Tool)

        # Add properties bin widget
        self.properties_bin = self.graph.properties_bin()
        splitter1.addWidget(self.build_right_sidebar())

        mainLayout.addWidget(splitter1)

        self.registryNodes()

        self.do_connection()

    def do_connection(self):
        # Connection
        def show_prop_bin(node):
            if not self.properties_bin.isVisible():
                self.properties_bin.show()

        self.graph.node_double_clicked.connect(show_prop_bin)

        self.run_menu.triggered.connect(self.executeNode)
        self.run_button.clicked.connect(self.executeNode)

    def build_right_sidebar(self):
        widget = QWidget()
        layout = QVBoxLayout()

        button_layout = QHBoxLayout()
        self.save_button = QPushButton(text = 'Save')
        self.run_button = QPushButton(text = 'run')
        # self.run_button.setMinimumHeight(40)

        button_layout.addWidget(self.run_button)
        button_layout.addWidget(self.save_button)
        button_layout.setStretchFactor(self.run_button, 1)

        layout.addLayout(button_layout)
        layout.addWidget(self.properties_bin)
        layout.setStretchFactor(self.properties_bin, 1)

        widget.setLayout(layout)
        return widget

    def executeNode(self):
        '''
        Execute selected node

        Returns:
        '''

        _selectedNode = self.graph.selected_nodes()
        if not _selectedNode :
            QMessageBox.warning(self, 'Warning', "No selected node.")
        elif len(_selectedNode) > 1 :
            QMessageBox.warning(self, 'Warning', "Cannot execute multiple node.")

        command.executeNode(_selectedNode[0])

    def registryNodes(self):

        # Find all node class in given node directory, then registry to graph
        try:
            for node in os.listdir(nodesDir):
                if not node.endswith('.py') or node.startswith('.'):
                    continue

                __modulepath = nodesDir + '/' + node
                __modulename = os.path.splitext(node)[0]
                try:
                    # importlib.import_module(__modulename, __modulepath)
                    imp.load_source(__modulename, __modulepath)
                except ImportError as e:
                    print(traceback.format_exc(e))
                    raise(e)


                for name, obj in inspect.getmembers(sys.modules[__modulename]):
                    if inspect.isclass(obj):
                        if issubclass(obj, Node) and obj != Node:
                            self.graph.register_node(obj)

        except Exception as e:
            print traceback.format_exc(e)
            print(e)

        self.graph.register_node(Backdrop)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MyGraphWindow()
    win.show()
    app.exec_()