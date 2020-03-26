import xml.etree.ElementTree as etree
from graphviz import Digraph
import sys

def print_usage():
    pass

def main(graph_file, is_view=True):
    tree = etree.parse(graph_file)
    root = tree.getroot()

    # Sanity check

    # Get layers
    layers = root.findall('layers/layer')

    # Get edges
    edges = root.findall('edges/edge')

    # Create Dot
    dot = Digraph(comment=root.attrib['name'], format='svg', directory='/tmp')

    # Add nodes to Dot
    for layer in layers:
        shape = "rectangle"
        #if layer.attrib['type'] == 'Input':
            #style = "rounded"
        out_ports = layer.findall('output/port')
        dim = '\n'.join(map(lambda port: '[%s]'%(','.join(map(lambda dim: dim.text, port.findall('dim')))), out_ports))
        #dim = ','.join(map(lambda x: x.text, layer.findall('output/port/dim')))
        text = '%s [%s]'%(layer.attrib['type'], layer.attrib['id']) + '\n%s'%dim
        dot.node(layer.attrib['id'], text, shape=shape, style="rounded")

    # Add edges to Dot
    for edge in edges:
        dot.edge(edge.attrib['from-layer'], edge.attrib['to-layer'])

    # Render Dot
    output_file = root.attrib['name']
    dot.render(output_file, view=is_view)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        graph_file = sys.argv[1]
    else:
        print_usage()
    main(graph_file, False)
