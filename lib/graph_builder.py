from graphviz import Digraph


class GraphBuilder:
    def __init__(self, url_map: dict):
        self.args_1 = {'penwidth': '0', 'fontname': 'Helvetica'}
        self.args_2 = {'fontname': 'Helvetica', 'color': '#90caf9',}
        self.gap = '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n'
        self.url_stream = url_map["stream"]
        self.enumerated_stream = url_map["enum_stream"]
        self.graph = Digraph(
            format='png',
            graph_attr={'rankdir':'LR', 'bgcolor': '#F2F2F2', 'newrank': 'true'},
            node_attr={'width': '2', 'height': '2', 'fontsize': '32pt', 'penwidth': '2'}
        )
        self.len_cs = 1

    def build(self, clickstream, first_sel, last_sel):
        self.graph, plotted_nodes = self.plot_main(self.graph, clickstream, first_sel, nodenames=True)
        self.graph = self.plot_transitions(plotted_nodes)
        self.graph = self.plot_end_statuses(clickstream, last_sel, plotted_nodes)
        return self.graph

    def scale_line_width(self, label_count: int) -> str:
        scale = 20
        res = scale * label_count/ self.len_cs
        return res.__str__() if res > 0 else 1

    def plot_main(self, graph: Digraph, clickstream: list, first_sel: list, nodenames=False) -> (Digraph, list):
        self.len_cs = len(clickstream)
        plotted_nodes, plotted_edges, fs = [], [], []
        for stream in clickstream:
            for i, node in enumerate(stream):
                if i != len(stream) - 1:
                    trans = stream[i + 1]
                    num = self.enumerated_stream[self.url_stream[node]].__str__()
                    graph.node(
                        node, node if nodenames else '', # xlabel=num,
                        fontname='Helvetica', fontcolor='#1a237e', fontsize=f'{2*int(num)}pt',
                    )
                    graph.node(
                        trans, trans if nodenames else '', # xlabel=num,
                        fontname='Helvetica', fontcolor='#1a237e', fontsize=f'{2*int(num)}pt',
                    )
                    plotted_nodes.append((node, trans))

                    # Adding starting point node
                if node in first_sel:
                    start_node_title = '_'.join([node, '_start'])
                    graph.node(
                        start_node_title, label='Start', style='invis', fillcolor='darkorange',
                        fontname='Helvetica', fontcolor='#1a237e',
                        panwidth='0',
                        fontsize = '32pt',
                    )
                    fs.append(node)
                    if (start_node_title, node) not in plotted_edges:
                        graph.edge(
                            start_node_title, node, label=f'{first_sel.count(node):.0f}',
                            fontname='Helvetica', color='darkorange',
                            minlen='2',
                            fontsize = '32pt',
                        )
                    plotted_edges.append((start_node_title, node))
        return graph, plotted_nodes

    def plot_transitions(self, plotted_nodes: list) -> Digraph:
        for (node, trans) in set(plotted_nodes):
            if plotted_nodes.count((node, trans)) > 0:
                if plotted_nodes.count((node, trans)) > 0 and plotted_nodes.count((trans, node)) > 0:
                    if plotted_nodes.count((node, trans)) == plotted_nodes.count((trans, node)):
                        continue
                    else:
                        if plotted_nodes.count((node, trans)) > plotted_nodes.count((trans, node)):
                            self.graph.edge(node, trans, minlen='2')
                        else:
                            continue
                else:
                    self.graph.edge(node, trans, minlen='2')
        return self.graph

    def plot_end_statuses(self, clickstream: list, last_sel: list, plotted_nodes: list) -> Digraph:
        # Plotting end statuses
        plotted_end_nodes = []
        for stream in clickstream:
            for node in stream[-1:]:
                if (
                        (node in last_sel) and (node not in plotted_end_nodes)
                        and
                        (
                                (node in [plotted_node[0] for plotted_node in plotted_nodes])
                                or
                                (node in [plotted_node[1] for plotted_node in plotted_nodes]))
                ):
                    status = 'last'
                    self.graph.node(
                        str(node) + status, label='Done',
                        style='invis', fillcolor='green',
                        fontname='Helvetica', fontcolor='#1a237e'
                    )
                    self.graph.edge(
                        node, str(node) + status,
                        label=f'{last_sel.count(node):2.0f}',
                        fontname='Helvetica',
                        minlen='2'
                    )

                    plotted_end_nodes.append(node)
        return self.graph
