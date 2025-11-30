# Was: createKG.py
# Now: simpletonKG.py
# Create Knowledge Graphs from text files for Simple-Ton
# New: 7/25/25; Mod: 11/27/25
#
import pandas as pd
import os
import networkx as nx
import matplotlib.pyplot as plt

alive_inputFile = "inputData/alive_head_relation_tail.txt"
alive_inputFileAdd = "inputData/alive_head_relation_tail_add.txt"
alive_AttribFile = "inputData/alive_node_attributes.txt"
device_inputFile = "inputData/device_head_relation_tail.txt"
space_inputFile = "inputData/space_head_relation_tail.txt"

input_aliveKG = "processedData/Alive.gml"
input_deviceKG = "processedData/Device.gml"
input_spaceKG = "processedData/Space.gml"



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

    aliveKG = None
    deviceKG = None
    spaceKG = None
    
    if os.path.exists(input_aliveKG):
        print(f"File {input_aliveKG} exits, loading data...")
        aliveKG = nx.read_gml(input_aliveKG)
    else:
        aliveKG = nx.DiGraph(name="Alive")
        #aliveKG = DynamicClass('Alive', None)

    if os.path.exists(input_deviceKG):
        print(f"File {input_deviceKG} exits, loading data...")
        deviceKG = nx.read_gml(input_deviceKG)
    else:
        #deviceKG = DynamicClass('Device', None)
        deviceKG = nx.DiGraph(name="Device")
        
    if os.path.exists(input_spaceKG):
        print(f"File {input_spaceKG} exits, loading data...")
        spaceKG = nx.read_gml(input_spaceKG)
    else:
        #spaceKG = DynamicClass('Space', None)
        spaceKG = nx.DiGraph(name="Space")

    return aliveKG, deviceKG, spaceKG


def addNode(G, edge2Add):

    if len(edge2Add) == 0:
        if input("Add node manually? <y/N>: ") in ['Y', 'y']:

            h = input("Enter Head: ")
            if h == '':
                return G
            t = input("Enter Tail: ")
            if t == '':
                return G
            r = input("Enter Relation: ")
            if r == '':
                return G
    else:
        h = edge2Add.get("head", "No Head")
        t = edge2Add.get("tail", "No Tail")
        r = edge2Add.get("relation", "No Relation")

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
            # if your graph is a tree you only have one root so you
            # don't need to check every node, once you find it it's done
            return node
    return None


def loadKG():

    # Check for existing graph file(s)
    #aliveKG, deviceKG = loadGraph()

    simpKG = loadGraph()

    print("len simpKG: ", len(simpKG))

    for kg in simpKG:

        print("kg.name: ", kg.name)
        print("kg.number_of_nodes: ", kg.number_of_nodes())
        
        if kg.name == 'Alive' and kg.number_of_nodes() == 0:
            # Construct alive (living things) graph
            #
            h, r, t = getInput(alive_inputFile)
            df = pd.DataFrame({'head': h, 'relation': r, 'tail': t})
            aliveKG = nx.DiGraph(name="Alive")
            for _, row in df.iterrows():
                aliveKG.add_edge(row['head'], row['tail'], label=row['relation'])

            # Add attributes
            node, attribName, attribValue = getInput(alive_AttribFile)
            for n, name, value in zip(node, attribName, attribValue):
                aliveKG.nodes[n][name] = value
        elif kg.name == 'Alive' and kg.number_of_nodes() > 0:
            aliveKG = kg

        if kg.name == 'Device' and kg.number_of_nodes() == 0:
            # Construct device (non-living things) graph
            #
            h, r, t = getInput(device_inputFile)
            df = pd.DataFrame({'head': h, 'relation': r, 'tail': t})
            deviceKG = nx.DiGraph(name="Device")
            for _, row in df.iterrows():
                deviceKG.add_edge(row['head'], row['tail'], label=row['relation'])
        elif kg.name == 'Device' and kg.number_of_nodes() > 0:
            deviceKG = kg

        if kg.name == 'Space' and kg.number_of_nodes() == 0:
            # Construct device (non-living things) graph
            #
            h, r, t = getInput(space_inputFile)
            df = pd.DataFrame({'head': h, 'relation': r, 'tail': t})
            spaceKG = nx.DiGraph(name="Space")
            for _, row in df.iterrows():
                spaceKG.add_edge(row['head'], row['tail'], label=row['relation'])
        elif kg.name == 'Space' and kg.number_of_nodes() > 0:
            spaceKG = kg
        
    return aliveKG, deviceKG, spaceKG


def addFile(G):
    if G == None:
        print("No Graph to add to...Exiting.")
        return None
    h, r, t = getInput(lt_inputFileAdd)
    df = pd.DataFrame({'head': h, 'relation': r, 'tail': t})
    for _, row in df.iterrows():
        G.add_edge(row['head'], row['tail'], label=row['relation'])
    return G


def saveKG(kg):

    for g in kg:
        fileName = "/home/gary/src/Simple-Ton/processedData/" + str(g.name) + ".gml"
        nx.write_gml(g, fileName)

    return

if __name__ == "__main__":

    print("START simpletonKG")
    
    simpKG = loadKG()

    print('len of simpKG after loadKG: ', len(simpKG))

    for kg in simpKG:
        print(kg.name)
        print(kg.number_of_nodes())
        #plotG(kg)
        printG(kg)

    #print(simpKG)

    # List a node's children (successors)
    searchNode = "man"
    children = list(simpKG[0].successors(searchNode))
    print(f"Children of {simpKG[0].name} -> {searchNode}: {children}")

    # List the returned nodes attributes
    for n in children:
        print(f"Attributes for {n} are {simpKG[0].nodes[n]}")

        if n == "John":
            simpKG[0].nodes[n]["Age"] = 40

    for n in children:
        print(f"Attributes for {n} are {simpKG[0].nodes[n]}")
    

    if input("Save graphs to files? <y/N>: ") in ["Y", "y"]:
        saveKG(simpKG)
        print("Graphs save to files.")


    """

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
    print("END simpletonKG")
