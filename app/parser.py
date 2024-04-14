from file_tool import create_file,clear_file,write_array
import settings

def parse(edges,terminal):
    res=[]
    res.append("SECTION Graph\n")
    edges_count = len(edges)
    nodes = set()
    for edge in edges:
        nodes.add(edge[0])
        nodes.add(edge[1])
    nodes_count = len(nodes)
    res.append("Nodes "+str(nodes_count)+"\n")
    res.append("Edges "+str(edges_count)+"\n")
    res.append("\n")
    for edge in edges:
        res.append("E "+str(edge[0])+" "+str(edge[1])+" "+str(edge[2])+"\n")
    res.append("END\n\n")

    res.append("SECTION Terminals\n")
    res.append("Terminals "+str(len(terminal))+"\n")
    for t in terminal:
        res.append("T "+str(t)+"\n")
    res.append("END\n\n")

    res.append("EOF\n")
    return res

def write_to_test(arr):
    create_file(settings.test_path)
    clear_file(settings.test_path)
    write_array(arr,settings.test_path)
