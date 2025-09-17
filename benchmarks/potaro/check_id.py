import pickle


if __name__ == '__main__':
  file_name = 'benchmarks/potaro/potaro_weighted_graph_NetworkX.pickle'

  # Load DiG
  with open(file_name, mode='br') as fi:
    DiG = pickle.load(fi)
    fi.close
