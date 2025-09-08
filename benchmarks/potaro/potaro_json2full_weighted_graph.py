import json

import networkx as nx
import matplotlib.pyplot as plt


if __name__ == '__main__':
  file_name = 'benchmarks/potaro/yakugzai.json'

  # Load json
  with open(file_name) as f:
    weighted_graph_list = json.load(f)
  #print(weighted_graph_list)

  # Convert to NetworkX graph
  ## weighted_elist
  DiG = nx.DiGraph()
  for element_dict in weighted_graph_list:
    DiG.add_edge(element_dict['start_global_id'], element_dict['goal_global_id'] , weight = element_dict['average_elapsed_time'],
               start_global_id = element_dict['start_global_id'],
               goal_waypoint_name = element_dict['goal_waypoint_name'],
               elapsed_times = element_dict['elapsed_times'])
  #print(G)

  # Run Dijkstra
  path_nodes = nx.dijkstra_path(DiG, '020100310', '020100603', weight='weight')
  edges_path_list = [(path_nodes[i], path_nodes[i+1]) for i in range(len(path_nodes)-1)]
  print('shortest path =', edges_path_list)
  edge_weights = nx.get_edge_attributes(DiG, 'weight')
  #print(edge_weights)
  dist = sum([edge_weights[edge] for edge in edges_path_list])
  print('dist =', dist)

  # Draw
  fig, ax = plt.subplots(figsize=(20,10))
  node_positions = nx.spring_layout(DiG, scale=50)# auto layout
  nx.draw_networkx(DiG, pos=node_positions, node_color='lightgrey', node_size=100, width=1) # base
  nx.draw_networkx_edge_labels(DiG, pos=node_positions, edge_labels=edge_weights) # weights
  nx.draw_networkx_edges(DiG, pos=node_positions, edgelist=edges_path_list, width=5, edge_color=plt.get_cmap('tab10').colors[0]) # path
  plt.axis('off')
  ax.set(aspect=1)
  #plt.savefig(prefix_file_name+'.pdf')
  plt.tight_layout()
  plt.show()
  plt.clf()
  plt.close()

