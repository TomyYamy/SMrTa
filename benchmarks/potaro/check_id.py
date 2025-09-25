import pickle

start_and_goal_candidate_list = [('020100903', 0), ('020100703', 1), ('020100808', 2), ('020100610', 3), ('020100408', 4), ('020100412', 5), ('020100822', 6), ('020100729', 7), ('020100414', 8), ('020100923', 9), ('020100827', 10), ('020100724', 11), ('020100605', 12), ('020100908', 13), ('020100829', 14), ('020100910', 15), ('020100318', 16), ('020100419', 17), ('020100805', 18), ('020100803', 19), ('020100206', 20), ('020100622', 21), ('020100727', 22), ('020100202', 23), ('020100627', 24), ('020100603', 25), ('020100722', 26), ('020100905', 27), ('020100608', 28), ('020100708', 29), ('020100209', 30), ('020100629', 31), ('020100705', 32), ('020100824', 33)]

if __name__ == '__main__':
  file_name = 'benchmarks/potaro/potaro_weighted_graph_NetworkX.pickle'

  # Load DiG
  with open(file_name, mode='br') as fi:
    DiG = pickle.load(fi)
    fi.close

  # Nodes list
  no_exist_in_weighted_graph = []
  for start_and_goal_candidate in start_and_goal_candidate_list:
    if start_and_goal_candidate[0] not in DiG.nodes:
      no_exist_in_weighted_graph.append(start_and_goal_candidate[0])

  print(f'no_exist_in_weighted_graph={no_exist_in_weighted_graph}')
