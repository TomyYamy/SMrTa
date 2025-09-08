import json

import networkx as nx


if __name__ == '__main__':
  file_name = 'benchmarks/potaro/yakugzai.json'

  # json load
  with open(file_name) as f:
    weighted_graph_list = json.load(f)
  #print(weighted_graph_list)

  # Convert to NetworkX graph
  ## weighted_elist
  G = nx.Graph()
  for element_dict in weighted_graph_list:
    G.add_edge(element_dict['start_global_id'], element_dict['goal_global_id'] , weight = element_dict['average_elapsed_time'],
               start_global_id = element_dict['start_global_id'],
               goal_waypoint_name = element_dict['goal_waypoint_name'],
               elapsed_times = element_dict['elapsed_times'])
  #print(G)
