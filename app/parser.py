from file_tool import create_file,clear_file,write_array,read_to_array
import settings
from entities.Chromosome import Chromosome
from algorithms.graph import caculate_sum_of_edges

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


def parse_generations(edges):
    arr = read_to_array(settings.generations_path)
    preprocessed_arr = []
    for a in arr:
        if a[0:3] == "At ":
            preprocessed_arr.append(a)
    initial_fitness = caculate_sum_of_edges(edges)
    res = [Chromosome(len(edges),initial_fitness)]
    for a in preprocessed_arr:
        res.append(Chromosome(a.split(" ")[3],int(a.split(" ")[4][:-1])))
    for r in res:
        print(r.__str__())
    return res