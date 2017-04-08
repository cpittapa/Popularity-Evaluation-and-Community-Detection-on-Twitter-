import json
import networkx as nx
import matplotlib.pyplot as plt
import os



'''
SETTINGS
'''
id_str=23375688  #user id for celebrity . If changing the celebrity, please change this id also
friends_cnt=10  #Please change the count to lowers number to run faster


final=[]


'''
Description : create_graph will open friend.xt also and store each friend collected as a node.
Also an edge is created between the node and celerity node.After this, it will traverse through the
primary friends of the celebrity and using the friends collected for each of these prime friends in friends folder,
we will establish edges if there is a friendship between the prime friends.

'''
def create_graph():
    f=0
    nodes = []
    prime=[]
    G=nx.Graph()
    f1 = open('data/friends.txt', 'r')
    file = f1.read()
    data = json.loads(file)
    G.add_node(id_str)
    prime=data
    for i in range(len(data)):
        G.add_node(data[i])
        G.add_edge(id_str,data[i])
        nodes.append(data[i])
    f2=open("data/graph.txt",'w')
    for node in prime:
        filename='data/friends/%s.txt'%node
        f1 = open(filename, 'r')
        file = f1.read()
        data1 = json.loads(file)
        nprime=prime.copy()
        nprime.remove(node)
        nprime.append(id_str)
        for i in nprime:
            if(i in data1):
                G.add_edge(i,node)
                f2.write(str(i) + " " + str(node)+"\n")
                f+=1
        f1.close()
    nx.draw(G,with_labels = True)
    plt.show()
    return G


'''
Description : girvan_newman method will take the graph previouly created, along with minsize and maxsize parameter, to create clusters.
minsize attributes to minimum number allowed in a cluster and maxsize the maximum number allowed in a cluster.

'''
def girvan_newman(G, minsize, maxsize):
    if G.order() == 1:
        return [G.nodes()]

    def find_best_edge(G0):
        eb = nx.edge_betweenness_centrality(G0)
        return sorted(eb.items(), key=lambda x: x[1], reverse=True)

    components = [c for c in nx.connected_component_subgraphs(G)]
    edge_to_remove = find_best_edge(G)
    i = 0
    while len(components) == 1:
        j = 0
        e = edge_to_remove[i][j]
        G.remove_edge(*e)
        i +=1
        components = [c for c in nx.connected_component_subgraphs(G)]
    result = []
    for c in components:
        if c.number_of_nodes() < minsize:
            continue
        elif c.number_of_nodes() >= minsize and c.number_of_nodes() <= maxsize:
            result.extend([c.nodes()])
        elif c.number_of_nodes() > maxsize:
            result.extend(girvan_newman(c, minsize, maxsize))
    return result

'''
Description : write_summary will take the result of girvan newman and write the results into a summary_cluster.txt

'''
def write_summary(result):
    file1 = "data/summary_cluster.txt"

    try:
        os.remove(file1)
    except OSError:
        pass
    for line in open("data/friends.txt"):
        data=json.loads(line)

    f1 = open(file1, "a")
    f1.write("\n COMMUNITY DETECTION  ")
    f1.write("\n Number of users collected:  "+str(len(data)+1))
    cluster_length = [len(x) for x in result]
    f1.write("\n Number of communities discovered:  " + str(len(cluster_length)))
    cluster_length = [len(x) for x in result]
    sum=0
    for a in cluster_length:
        sum+=a
    f1.write("\n Average number of users per community:  " + str(sum/(len(cluster_length))))



'''
Main Method
'''
if __name__ == '__main__':
    G=create_graph()
    print("Number of nodes in graph ",G.number_of_nodes())
    print("Number of edges in graph ", G.number_of_edges())
    result=girvan_newman(G,3,15)
    cluster_length=[len(x) for x in result]
    print('Final cluster sizes:',cluster_length)
    sum=0
    for a in cluster_length:
        sum+=a
    print("Average of clusters sizes",sum/(len(cluster_length)))
    i=0
    for cluster in result:
        print("Cluster %d :"%i)
        print(cluster)
        i+=1

    write_summary(result)

