
## Python 2

# coding: utf-8

# # Connected Components
# 
# The purpose of this assignment is to familiarize yourself with the handling of graph data structures. You will implement depth-first search for identifying the connected components of an undirected graph, implementing procedure Search as a subroutine along the way.
# 
# You will use the [NetworkX](https://networkx.github.io/) Python package to represent and manipulate graphs. You should first familiarize yourself with its functionality by going through the brief [tutorial](http://networkx.github.io/documentation/networkx-1.9.1/tutorial/index.html). For this homework, you may only use the basic undirected graph methods listed [here](http://networkx.github.io/documentation/networkx-1.9.1/reference/classes.graph.html).
# 
# As a use case, we will work with a dataset recording the interactions between characters in Homer's *Iliad*.


# In[16]:


import networkx
import urllib2
homer = urllib2.urlopen('http://people.sc.fsu.edu/~jburkardt/datasets/sgb/homer.dat')


# The format of the data is straightforward. After some comment lines (beginning with \*), the file lists a codename for each character (i.e., node of the graph), followed by a description. The file then lists the groups of characters that interact in each chapter, from which you will form the edges. For instance, the first line has the form:
# 
# ```1:CH,AG,ME,GS;AP,CH;HE,AC;AC,AG,CA;HE,AT;AT,AC;AT,OG;NE,AG,AC;CS,OD```
# 
# This means that CH,AG,ME,GS interacted, so there are edges for all pairs of these nodes. Groups of characters that interacted are separated by semicolons. The lines start with chapter information of the form `1:` or `&:`, which can be ignored for this problem.

# First implement a function to read in the nodes from the input file. You may implement any auxiliary functions as needed, and are encouraged to use small functions with specific purposes to keep your code readable. Any function you implement should be clearly commented.

# Next implement a function to read in the edges from the input file.

# In[2]:


def read_nodes(gfile):
    """Reads in the nodes of the graph from the input file.
    
    Args:
        gfile: A handle for the file containing the graph data, starting at the top.
        
    Returns:
        A generator of the nodes in the graph, yielding a list of the form:
            ['CH', 'AG, 'ME', ...]
    """
    
    nodes = []
    for line in gfile: 
        if line == '\n':
            break
        elif line.split(' ')[0] == '*':
            continue 
        nodes.append(line.split(' ')[0]) 
    return nodes


# In[3]:


def read_edges(gfile):
    """Reads in the edges of the graph from the input file.
    
    Args:
        gfile: A handle for the file containing the graph data, starting at the top 
            of the edges section.
            
    Returns:
        A generator of the edges in the graph, yielding a list of pairs of the form:
            [('CH', 'AG'), ('AG', 'ME'), ...]
    """
    
    lines2 = []
    for line in gfile:
        line = line.strip('\n')
        lines = line.split(':')[-1]
        lines2.append(lines.split(';'))
            
    nodes = [item for sublist in lines2 for item in sublist]
    item2 = []
    for item in nodes:
        item2.append(item.split(','))
    combo = []
    for item in item2:
        combinations = []
        for i in range(0,len(item)):
            for j in range(i+1,len(item)):
                combinations.append((item[i],item[j]))
        combo.append(combinations)

    edges = [item for sublist in combo for item in sublist]
    return edges


# The following code should now correctly create the graph.

# In[4]:


import networkx as nx
G = nx.Graph()
G.add_nodes_from(read_nodes(homer))
G.add_edges_from(read_edges(homer))


# Next implement procedure Search. The function takes in a graph and a root node, and returns a list of the nodes visited during the search. The nodes should appear in the order in which they were *first visited*. The neighbors of a node should be processed in *alphabetical order*, where numbers come before letters. This will ensure that the output of your function is uniquely defined, given any input node.

# In[6]:


def Search(graph, root):
    """Runs Search from vertex root in a graph. Neighboring nodes are processed in alphabetical order.
    
    Args:
        graph: the given graph, with nodes encoded as strings.
        root: the node from which to start the search.
        
    Returns:
        A list of nodes in the order in which they were first visited.
    """
    
    visited = []
    stack = []
    stack.append(root)
    while stack:
        node = stack.pop()
        if node not in visited:
            visited.append(node)
            for item in reversed(sorted(graph.neighbors(node))):
                if item not in visited:
                    stack.append(item)
    return visited


# We will check the correctness of your code by verifying that it correctly computes the DFS tree starting at Ulysses (node `OD`).

# In[7]:


ulysses = Search(G, 'OD')


# Next implement DFS to find the connected components of the character graph. When choosing roots for your components, always pick the *smallest unvisited node* according to alphabetical ordering. Combined with your Search routine, this will ensure that the output is again uniquely defined.

# In[20]:


def connected_components(graph):
    """Computes the connected components of the given graph.
    
    Args: 
        graph: the given graph, with nodes encoded as strings.
        
    Returns:
        The connected components of the graph. Components are listed in
        alphabetical order of their root nodes.
    """
 
    visited= []
    components = []
    for node in sorted(graph.nodes()): 
        print(node)
        if node not in visited:
            temp = Search(graph,node)
            components.append(temp)
            for node in temp:
                visited.append(node)
    return components      


# We will check correctness of your code by verifying that your output list is identical to our solution.

# In[ ]:


character_interactions = connected_components(G)


# As a preliminary check, you should find that the following statements are all true.

# In[22]:


component_sizes = [len(c) for c in character_interactions]
print "There are 12 connected components in the Iliad:", len(component_sizes) == 12
print "The giant component has size 542:", max(component_sizes) == 542
print "There are 5 isolated characters:", len([c for c in component_sizes if c == 1]) == 5

