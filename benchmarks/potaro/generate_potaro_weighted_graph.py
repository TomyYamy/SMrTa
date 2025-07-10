import pickle

# Generate
potaro_weighted_graph = {}
## from ME_room: 0
potaro_weighted_graph[0] = { 2: 5,
                             3: 5,
                             4: 5,
                             5: 5,
                             6: 5,
                             7: 5,
                             8: 5,
                             9: 5,
                            10: 5,
                            11: 5,
                            12: 5,
                            13: 5,
                            14: 5,
                            15: 5,
                            16: 5}
## from medicine_room: 1
potaro_weighted_graph[1] = { 2: 5,
                             3: 5,
                             4: 5,
                             5: 5,
                             6: 5,
                             7: 5,
                             8: 5,
                             9: 5,
                            10: 5,
                            11: 5,
                            12: 5,
                            13: 5,
                            14: 5,
                            15: 5,
                            16: 5}

## Set opposites
for depot_key in [0, 1]:
  for direction_key in potaro_weighted_graph[depot_key].keys():
    if not direction_key in potaro_weighted_graph.keys():
      potaro_weighted_graph[direction_key]={}
    potaro_weighted_graph[direction_key].update({depot_key: potaro_weighted_graph[depot_key][direction_key]})

# Print
print('potaro_weighted_graph=', potaro_weighted_graph)

# Save
with open("benchmarks/potaro/potaro_weighted_graph.pickle", mode="wb") as fo:
  pickle.dump(potaro_weighted_graph, fo)
