# createKG.py
# Create Knowledge Graphs from text files for Simple-Ton
# New: 7/25/25
#
import pandas as pd
import os
import networkx as nx
import matplotlib.pyplot as plt

lt_inputFile = "inputData/lt_head_relation_tail.txt"
lt_inputFileAdd = "inputData/lt_head_relation_tail_add.txt"
lt_AttribFile = "inputData/lt_node_attributes.txt"
nlt_inputFile = "inputData/nlt_head_relation_tail.txt"

inputLTG = "processedData/kg-LTG.gml"
inputnLTG = "processedData/kg-nLTG.gml"

def getInput(inputFile):

    head = []
    relation = []
    tail = []
    
    try:
        with open(inputFile, 'r') as file:
            for line in file:
                s_line = line.strip()
                if s_line[0] != '#':
                    line_lst = s_line.split(',')
                    head.append(line_lst[0])
                    relation.append(line_lst[1])
                    tail.append(line_lst[2])
                    
    except FileNotFoundError:
        print(f"File {inputFile} not found error.")
    except Exception as e:
        print(f"Exception {e} caught.")

    return head, relation, tail


def printG(G):
    print('# of nodes:')
    print(G.number_of_nodes())
    print(f'{G.graph["name"]} nodes:')
    print(G.nodes)
    print('# of edges:')
    print(G.number_of_edges())
    print(f'{G.graph["name"]} edges:')
    print(G.edges)
    #print(G.graph["name"]
    print(f"---All new {G.graph["name"]} node attributes:")
    for node, attributes in G.nodes(data=True):
        print(attributes)
        print(f"node: {node}, attributes: {attributes}")

    print(f"---All new {G.graph["name"]} edge attributes:")
    for u, v, data in G.edges(data=True):
        print(data)
        print(f"Edge ({u}, {v}) attributes: {data}")

    print('-----')

    return


def plotG(G):
    # Visualize the knowledge graph
    node_labels = nx.get_node_attributes(G, 'Age')
    pos = nx.spring_layout(G, seed=42, k=0.9)
    labels = nx.get_edge_attributes(G, 'label')
    plt.figure(figsize=(12, 10))
    nx.draw(G, pos, with_labels=True, font_size=10, node_size=700, node_color='lightblue', edge_color='gray', alpha=0.6)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, font_size=8, label_pos=0.3, verticalalignment='baseline')
    nx.draw_networkx_labels(G, pos, labels=node_labels)
    plt.title('Knowledge Graph')
    plt.show()

    return


def loadGraph():

    LTG = None
    nLTG = None
    
    if os.path.exists(inputLTG):
        print(f"File {inputLTG} exits, loading data...")
        LTG = nx.read_gml(inputLTG)

    if os.path.exists(inputnLTG):
        print(f"File {inputnLTG} exits, loading data...")
        nLTG = nx.read_gml(inputnLTG)

    return LTG, nLTG


def addNode(G):

    h = input("Enter Head: ")
    if h == '':
        return G
    t = input("Enter Tail: ")
    if t == '':
        return G
    r = input("Enter Relation: ")
    if r == '':
        return G

    G.add_edge(h, t, label=r)

    return G


def delNode(G):
    n = input("Enter node name to remove: ")
    if n == '':
        return G
    try:
        G.remove_node(n)
    except nx.NetworkXError as e:
        print(f"NetworkX Exception caught: {e} ")
    else:
        print(f"Node: {n} removed.") 
    return G


def getRoot(G):
    for node, indegree in G.in_degree():
        if indegree == 0:
            # if you'r graph is a tree you only have one root so you don't need to check every node, once you find it it's done
            return node
    return None


def loadKG():

    # Check for existing graph file(s)
    LTG, nLTG = loadGraph()

    if LTG == None:
        # Construct living things graph
        #
        h, r, t = getInput(lt_inputFile)
        df = pd.DataFrame({'head': h, 'relation': r, 'tail': t})
        LTG = nx.DiGraph(name="LivingThings")
        for _, row in df.iterrows():
            LTG.add_edge(row['head'], row['tail'], label=row['relation'])

        # Add attributes
        node, attribName, attribValue = getInput(lt_AttribFile)
        for n, name, value in zip(node, attribName, attribValue):
            LTG.nodes[n][name] = value

    if nLTG == None:
        # Construct non-living things graph
        #
        h, r, t = getInput(nlt_inputFile)
        df = pd.DataFrame({'head': h, 'relation': r, 'tail': t})
        nLTG = nx.DiGraph(name="nonLivingThings")
        for _, row in df.iterrows():
            nLTG.add_edge(row['head'], row['tail'], label=row['relation'])
    
    return LTG, nLTG


def addFile(G):
    if G == None:
        print("No Graph to add to...Exiting.")
        return None
    h, r, t = getInput(lt_inputFileAdd)
    df = pd.DataFrame({'head': h, 'relation': r, 'tail': t})
    for _, row in df.iterrows():
        G.add_edge(row['head'], row['tail'], label=row['relation'])
    return G 

if __name__ == "__main__":

    LTG, nLTG = loadKG()

    plotG(LTG)

    plotG(nLTG)

    """
    # Check for existing graph file(s)
    LTG, nLTG = loadGraph()

    if LTG == None:
        # Construct living things graph
        #
        h, r, t = getInput(lt_inputFile)
        df = pd.DataFrame({'head': h, 'relation': r, 'tail': t})
        LTG = nx.DiGraph(name="LivingThings")
        for _, row in df.iterrows():
            LTG.add_edge(row['head'], row['tail'], label=row['relation'])

        # Add attributes
        node, attribName, attribValue = getInput(lt_AttribFile)
        for n, name, value in zip(node, attribName, attribValue):
            LTG.nodes[n][name] = value

    plotG(LTG)

    if nLTG == None:
        # Construct non-living things graph
        #
        h, r, t = getInput(nlt_inputFile)
        df = pd.DataFrame({'head': h, 'relation': r, 'tail': t})
        nLTG = nx.DiGraph(name="nonLivingThings")
        for _, row in df.iterrows():
            nLTG.add_edge(row['head'], row['tail'], label=row['relation'])

    plotG(nLTG)

    # Get root node
    print(f"Root node: {getRoot(LTG)}")

    # Node ancestor and child search
    searchNode = input(f"Enter {LTG.name} node name for ancestor search: ")

    if searchNode != '':
        try:
            ancestorsFound = nx.ancestors(LTG, searchNode)
        except nx.NetworkXError as e:
            print(f"NetworkX Exception caught: {e} ")
        else:
            print("Ancestors: ")
            print(ancestorsFound)
            # Sorted
            print(nx.shortest_path(LTG, source=getRoot(LTG), target=searchNode))
            print("Childern:")
            c = nx.descendants(LTG, searchNode)
            if len(c) > 0:
                print(c)
            

    # Add node
    LTG = addNode(LTG)
    # Remove node
    LTG = delNode(LTG)

    # Add another text input file
    LTG = addFile(LTG)
    
    # Resulting graph
    plotG(LTG)

    # Save to file(s)
    ans = input("Save graph(s) to file(s) <Y/n>: ")
    if ans in ['Y', 'y']:
        nx.write_gml(LTG, "kg7-LTG.gml")
        nx.write_gml(nLTG, "kg7-nLTG.gml")
        print("Files saved.")    
    """
