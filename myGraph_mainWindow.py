#!/usr/bin/python
import os
import sys
# import importlib
import imp
import inspect
import traceback

from NodeGraphQt import BaseNode, BackdropNode, setup_context_menu, PropertiesBinWidget, NodeTreeWidget
from graph import NodeGraph
from PySide2.QtWidgets import *
from PySide2.QtCore import *

import qdarkstyle

# from widget import OptionBox
import command
import widgets

nodesDir = os.path.dirname(__file__).replace('\\','/') + '/myGraph/custom_nodes'

class EmittingStream(QObject):
    textWritten = Signal(str)
    def write(self, text):
        self.textWritten.emit(str(text))

class MyGraphWindow(QMainWindow):

    def __init__(self, parent = None):
        super(MyGraphWindow, self).__init__(parent)
        mainwidget = QWidget(self)
        self.setWindowTitle("MyGraph 1.0Alpha")

        # Build menu
        self.menubar = QMenuBar(self)
        file_menu = QMenu("&File")
        open_action = QAction("&Open", self,  shortcut="Ctrl+O", triggered=self.open_session)
        file_menu.addAction(open_action)
        self.menubar.addMenu(file_menu)
        self.menubar.addAction('&Edit')
        self.view_menu = QMenu('&View')
        self.menubar.addMenu(self.view_menu)
        self.panel_submenu = QMenu("&Panels")
        self.view_menu.addMenu(self.panel_submenu)
        self.run_menu = self.menubar.addAction('&Run')
        mainLayout = QHBoxLayout()

        # main UI
        self.graph =  NodeGraph()
        self.viewer = self.graph.viewer()

        mainwidget.setLayout(mainLayout)
        mainLayout.addWidget(self.viewer)
        self.setCentralWidget(mainwidget)
        self.setMenuBar(self.menubar)

        # set up default menu and commands.
        setup_context_menu(self.graph)

        # Add properties bin widget
        self.properties_bin = PropertiesBinWidget(node_graph=self.graph)
        self.properties_bin.setWindowFlags(Qt.Tool)
        side_widget = self.build_right_sidebar()
        self.add_dockWidget(name="Properties",widget=side_widget, addArea=Qt.RightDockWidgetArea)

        # Node tree widget
        self.node_tree = NodeTreeWidget(node_graph=self.graph)
        self.add_dockWidget(name="Node tree", widget=self.node_tree, addArea=Qt.LeftDockWidgetArea)

        # Connect to console
        sys.stdout = EmittingStream()
        sys.stderr = EmittingStream()
        sys.stdout.textWritten.connect(lambda text: self.console.append(text, isError=False))
        sys.stderr.textWritten.connect(lambda text: self.console.append(text, isError=True))
        self.console = widgets.Console()
        self.add_dockWidget(name="Console", widget=self.console, addArea=Qt.RightDockWidgetArea)

        self.registryNodes()
        self.do_connection()

        self.node_tree.update()

    def do_connection(self):
        # Connection
        def show_prop_bin(node):
            if not self.properties_bin.isVisible():
                self.properties_bin.show()

        def show_nodes_list(node):
            if not self.node_tree.isVisible():
                self.node_tree.update()
                self.node_tree.show()

        self.graph.node_double_clicked.connect(show_prop_bin)
        self.graph.node_double_clicked.connect(show_nodes_list)

        self.run_menu.triggered.connect(self.executeNode)
        self.run_button.clicked.connect(self.executeNode)

    def add_dockWidget(self, name, widget, allowedAreas = None, addArea = None):

        if not allowedAreas:
            allowedAreas = Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea
        if not addArea:
            addArea = Qt.LeftDockWidgetArea

        dockWidget = QDockWidget(name, self)
        dockWidget.setAllowedAreas(allowedAreas)
        dockWidget.setWidget(widget)
        self.addDockWidget(addArea, dockWidget)
        self.panel_submenu.addAction(dockWidget.toggleViewAction())

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

    def open_session(self):
        """
        Prompts a file open dialog to load a session.

        Args:
            graph (NodeGraphQt.NodeGraph): node graph.
        """
        graph = self.graph
        current = graph.current_session()
        viewer = graph.viewer()
        file_path = viewer.load_dialog(current)
        if file_path:
            graph.load_session(file_path)

    def executeNode(self):
        '''
        Execute selected node

        Returns:
        '''

        _selectedNode = self.graph.selected_nodes() # type: list
        if not _selectedNode :
            QMessageBox.warning(self, 'Warning', "No selected node.")
            return
        elif len(_selectedNode) > 1 :
            QMessageBox.warning(self, 'Warning', "Cannot execute multiple node.")
            return
        else:
            selected_node = _selectedNode[0]

        msgBox = QMessageBox.information(self, self.tr("Run"),
                               "You want to run selected node?.\n>> %s"%selected_node.NODE_NAME,
                               QMessageBox.Yes | QMessageBox.Cancel,
                               QMessageBox.Yes)

        if msgBox == QMessageBox.Yes:
            command.executeNode(selected_node)

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
                        if issubclass(obj, BaseNode) and obj != BaseNode:
                            self.graph.register_node(obj)

        except Exception as e:
            print traceback.format_exc(e)
            print(e)

        self.graph.register_node(BackdropNode)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MyGraphWindow()
    app.setStyleSheet(qdarkstyle.load_stylesheet())
    with open(qdarkstyle.QSS_FILEPATH, 'r') as reader:
        app.setStyleSheet(reader.read())
    win.show()
    app.exec_()