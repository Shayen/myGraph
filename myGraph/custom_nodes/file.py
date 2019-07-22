import Node

from PySide2.QtGui import QFont

class Read(Node.NodeBase):
    """
    An example of a node with a embedded QLineEdit.
    """

    # unique node identifier.
    __identifier__ = 'com.file'

    # initial default node name.
    NODE_NAME = 'read file'
    __MODE = 'r'

    def __init__(self):
        super(Read, self).__init__()

        # create input & output ports
        self.input_filename = self.addInputPin('file_name')
        self.result = self.addOutputPin('data', default_value=None)


    def execute(self):

        with open(self.input_filename.getData(),  self.__MODE) as f:
            self.result.setData(f.read())
        f.close()

class Write(Node.NodeBase):
    """
    An example of a node with a embedded QLineEdit.
    """

    # unique node identifier.
    __identifier__ = 'com.file'

    # initial default node name.
    NODE_NAME = 'write file'
    __MODE = 'w'

    def __init__(self):
        super(Write, self).__init__()

        # create input & output ports
        self.input_filename = self.addInputPin('file_name')
        self.input_data = self.addInputPin('data')

    def execute(self):

        with open(self.input_filename.getData(),  self.__MODE) as f:
            f.write(self.input_data.getData())
        f.close()


class Append(Write):
    # unique node identifier.
    __identifier__ = 'com.file'

    # initial default node name.
    NODE_NAME = 'write file (append)'
    __MODE = 'a'