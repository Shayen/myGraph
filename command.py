import os
import sys
import traceback

def executeNode(node):
    """
    TODO: Imprement https://github.com/pyqtgraph/pyqtgraph/blob/229f650adfd04053213fe6567d6308a4751a349b/pyqtgraph/flowchart/Flowchart.py#L248
    Args:
        Node (Node):
    """

    print ("Executing...")
    try :
        _root = []
        _executeSequence = [node]
        _upstream = getPreviousNodes(node)
        while _upstream:
            _n = _upstream.pop(0)
            previousNodes = getPreviousNodes(_n)
            if not previousNodes:
                if not _n in _root:
                    _root.append(_n)
            else:
                _upstream += previousNodes

                if not _n in _executeSequence:
                    _executeSequence.insert(0, _n)

        _executeSequence = _root + _executeSequence

        print ('Execute order :',[n.NODE_NAME for n in _executeSequence])

        for node in _executeSequence:
            node.execute()

        return True
    except Exception as e:
        print  (traceback.format_exc(e))

def getInputValue(node):
    try:
        return node.input(0).connected_ports()[0].node().get_property(node.input(0).connected_ports()[0].name())
        # return getattr(node.input(0).connected_ports()[0].node(), node.input(0).connected_ports()[0].name())
    except IndexError:
        print ("Index Error")
        return None

def getPreviousNodes(node):
    __allPorts = node.inputs() #return port's name

    _previousNode = []
    for portName in __allPorts.keys():
        destPort = __allPorts[portName].connected_ports()
        if not destPort:
            continue
        _previousNode.append(destPort[0].node())

    return _previousNode
