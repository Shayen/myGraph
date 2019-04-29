import Node

class List(Node.NodeBase):
    """
    An example of a node with a embedded QLineEdit.
    """

    # unique node identifier.
    __identifier__ = 'com.list'

    # initial default node name.
    NODE_NAME = 'list'

    def __init__(self):
        super(List, self).__init__()

        # create input & output ports
        self.input_list = self.addInputPin('list_input', multi_input=True)
        self.result = self.addOutputPin('result', default_value=None)

    def execute(self):
        # node.input(0).connected_ports()[0].node().get_property(node.input(0).connected_ports()[0].name())
        result = []
        for connected_port in self.input_list.instance.connected_ports():
            data = connected_port.node().get_property(connected_port.name())
            result.append(data)

        self.result.setData(result)

class List_selection(Node.NodeBase):
    """
    An example of a node with a embedded QLineEdit.
    """

    # unique node identifier.
    __identifier__ = 'com.list.selection'

    # initial default node name.
    NODE_NAME = 'list selection'

    def __init__(self):
        super(List_selection, self).__init__()

        # create input & output ports
        self.input_list = self.addInputPin('list_input')
        self.input_index = self.addInputPin(name = 'index')
        self.result = self.addOutputPin('result', default_value=None)

    def execute(self):
        result = self.input_list.getData()[int(self.input_index.getData())]
        self.result.setData(result)

class List_append(Node.NodeBase):

    # unique node identifier.
    __identifier__ = 'com.list.append'

    # initial default node name.
    NODE_NAME = 'append list'

    def __init__(self):
        super(List_append, self).__init__()

        # create input & output ports
        self.input_list = self.addInputPin('list_input')
        self.input_item = self.addInputPin(name = 'item')
        self.result = self.addOutputPin('result', default_value=None)

    def execute(self):
        result = self.input_list.append(self.input_item)
        self.result.setData(result)

class List_sort(Node.NodeBase):
    # unique node identifier.
    __identifier__ = 'com.list.sort'

    # initial default node name.
    NODE_NAME = 'sort list'

    def __init__(self):
        super(List_sort, self).__init__()

        # create input & output ports
        self.input_list = self.addInputPin('list_input')
        self.result = self.addOutputPin('result', default_value=None)

    def execute(self):
        result = sorted(self.input_list)
        self.result.setData(result)
