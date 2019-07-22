import Node

is_maya = True
try:
    import maya.cmds as cmds
except ImportError:
    is_maya = False

if is_maya :
    class Cube(Node.NodeBase):
        """
        An example of a node with a embedded QLineEdit.
        """

        # unique node identifier.
        __identifier__ = 'maya.poly'

        # initial default node name.
        NODE_NAME = 'plus'

        def __init__(self):
            super(Cube, self).__init__()

            # create input & output ports
            self.input1 = self.addInputPin('in1')
            self.input2 = self.addInputPin('in2')
            self.result = self.addOutputPin('result', default_value=0)
            # self.add_output('result')
            # self.create_property('result', 0)
        def execute(self):
            cmds.cube()