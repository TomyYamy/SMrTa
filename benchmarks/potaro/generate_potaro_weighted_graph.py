import pickle

# Generate
potaro_weighted_graph = {}
potaro_weighted_graph[0] = {2: 5, 3: 5}


# Print
print('potaro_weighted_graph=', potaro_weighted_graph)

# Save
with open("benchmarks/potaro/potaro_weighted_graph.pickle", mode="wb") as fo:
  pickle.dump(potaro_weighted_graph, fo)
