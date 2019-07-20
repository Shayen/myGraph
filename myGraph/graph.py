import NodeGraphQt

class NodeGraph(NodeGraphQt.NodeGraph):

    def _on_search_triggered(self, node_type, pos):
        super(NodeGraph, self)._on_search_triggered(node_type=node_type, pos = pos)
        print(node_type)