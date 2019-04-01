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

nodesDir = os.path.dirname(__file__).replace('\\','/') + '/custom_nodes'

class MyGraphWindow(QMainWindow):

    def __init__(self, parent = None):
        super(MyGraphWindow, self).__init__(parent)
        mainwidget = QWidget(self)
        self.menubar = QMenuBar(self)
        self.menubar.addAction('&Files')
        self.menubar.addAction('&Edit')
        self.run_menu = self.menubar.addAction('&Run')
        mainLayout = QVBoxLayout()
        self.graph =  NodeGraph()
        # setup_context_menu(self.graph)
        self.viewer = self.graph.viewer()

        mainwidget.setLayout(mainLayout)
        mainLayout.addWidget(self.viewer)
        self.setCentralWidget(mainwidget)
        self.setMenuBar(self.menubar)

        # set up default menu and commands.
        setup_context_menu(self.graph)

        # show the properties bin when a node is "double clicked" in the graph.
        properties_bin = self.graph.properties_bin()
        properties_bin.setWindowFlags(QtCore.Qt.Tool)

        # Connection
        self.run_menu.triggered.connect(self.executeNode)

        def show_prop_bin(node):
            if not properties_bin.isVisible():
                properties_bin.show()

        self.graph.node_double_clicked.connect(show_prop_bin)

        self.registryNodes()

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