import json

import networkx as nx
import itertools as iter
import matplotlib.pyplot as plt
import pickle as pickle


if __name__ == '__main__':
  file_name = 'benchmarks/potaro/yakugzai.json'
  # for demo
  # start_and_goal_candidate_list = [
  #   ('020100310', 0), #dummy ME_room #TODO: Why we need the dummy?
  #   ('020100310', 1), #薬局前充電器9[10]
  #   ('020100414', 2), #4E[14]
  #   ('020100412', 3), #4G[12]
  #   ('020100608', 4), #6A 東側[08]
  #   ('020100603', 5), #6B 西側[03]
  #   ('020100627', 6), #6C 東側[27]
  #   ('020100707', 7), #7A 東側[07]
  #   ('020100703', 8), #7B 西側[03]
  #   ('020100726', 9), #7C 東側[26]
  #   ('020100722',10), #7D 西側[22]
  #   ('020100803',11), #8B 東側[03]
  #   ('020100826',12), #8C 東側[26]
  #   ('020100822',13), #8D 西側[22]
  #   ('020100907',14), #9A 東側[07]
  #   ('020100903',15), #9B 西側[03]
  #   ('020100923',16)  #9C[23]
  # ]
  # For log data
  start_and_goal_candidate_list = [('020100316', 0), ('020100412', 1), ('020100414', 2), ('020100603', 3), ('020100608', 4), ('020100622', 5), ('020100627', 6), ('020100703', 7), ('020100708', 8), ('020100722', 9), ('020100727', 10), ('020100803', 11), ('020100808', 12), ('020100822', 13), ('020100827', 14), ('020100903', 15), ('020100908', 16), ('020100923', 17)]

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
  #print(DiG)
  ## Save
  with open("benchmarks/potaro/potaro_weighted_graph_NetworkX.pickle", mode="wb") as fo:
    pickle.dump(DiG, fo)

  # Run Dijkstra and Generate potaro_weighted_graph
  ## Permutations
  potaro_weighted_graph = {}
  perm_start_and_goal = list(iter.permutations(start_and_goal_candidate_list, 2))
  for start_enum, goal_enum in perm_start_and_goal:
    path_nodes = nx.dijkstra_path(DiG, start_enum[0], goal_enum[0], weight='weight')
    edges_path_list = [(path_nodes[i], path_nodes[i+1]) for i in range(len(path_nodes)-1)]
    print(f'shortest path of ({start_enum[0]},{goal_enum[0]}) = {edges_path_list}')
    edge_weights = nx.get_edge_attributes(DiG, 'weight')
    #print(edge_weights)
    dist = sum([edge_weights[edge] for edge in edges_path_list])
    print('dist =', dist)

    # add potaro_weighted_graph
    if potaro_weighted_graph.get(start_enum[1]) != None:
      potaro_weighted_graph[start_enum[1]].update({goal_enum[1]: dist})
    else:
      potaro_weighted_graph.update({start_enum[1]: {goal_enum[1]: dist}})

  ## Save
  print('potaro_weighted_graph=', potaro_weighted_graph)
  with open("benchmarks/potaro/potaro_weighted_graph4log.pickle", mode="wb") as fo:
    pickle.dump(potaro_weighted_graph, fo)

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

