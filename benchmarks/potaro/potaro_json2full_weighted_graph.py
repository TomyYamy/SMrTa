import json


if __name__ == '__main__':
  file_name = 'benchmarks/potaro/yakugzai.json'

  # json load
  with open(file_name) as f:
    weighted_graph_list = json.load(f)

  print(weighted_graph_list)

  # Convert to NetworkX graph
  for i in weighted_graph_list:
    print(i)
