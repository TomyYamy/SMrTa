import json
import matplotlib as plt

import smrta.create_randomized_inputs as cri
import smrta.run_realistic_setting as rrs

from pathlib import Path
from smrta.solver import MultiRobotTaskAllocation
from smrta.solver import Options
from smrta.solver import SolverKind, TheoryKind


def gannt_chart(ax, nodes, node_start_times, path, agent_name='0', color_pallet_dict={}):

    color_count = 0
    for edge in path:
        consume_time = edge[1][2]['weight']
        node_start, node_end = get_nodes_of_edge(nodes, edge)
        agent_start_time = node_start_times[node_start[0]]
    if(color_pallet_dict):
        edge_key = (edge[1][0], edge[1][1])
        ce = color_pallet_dict[edge_key]
    else:
        cmap = plt.get_cmap('tab10')
        ce = cmap.colors[color_count%len(cmap.colors)]
    label = str(node_start[1][0])+'-'+str(node_end[1][0])
    p = ax.barh(y=agent_name, width=consume_time, left=agent_start_time, label=label, color=(0,0,0,0), ec=ce, linewidth=3)
    ax.bar_label(p, labels=[label], label_type='center', rotation=90)
    color_count = color_count+1



def main():
    """The main entrypoint.
    """

    path = Path(__file__).resolve().parent

    # We load the room graph, first.
    #
    # This is a specific format that may be viewed by printing the data structure
    # after it has been un-pickled, accordingly.
    filename = path.joinpath("potaro/potaro_weighted_graph.pickle")
    count, graph = rrs.dictionary_to_matrix(rrs.load_weighted_graph(file_name=str(filename)))

    # We load the agents and tasks, next.
    #
    # This will load the configuration file needed to set up the agents and theory
    # tasks for the solver to solve.
    filename = path.joinpath("potaro/test_case.json")
    agents, tasks = cri.load_config(filename)

    # Set the options.
    #
    # This will set the S-MrTa options such as the backend to use, the type of
    # theory to leverage and any additional configurations needed when running
    # the allocation problem, accordingly.
    #
    # NOTE: The combination of `solver` and `theory` options matter as not all
    # combinations are currently supported (e.g., `SolverKind.Bitwuzla` and
    # `TheoryKind.Integer`) are not implemented, accordingly.
    options = Options(
        solver=SolverKind.Bitwuzla,
        theory=TheoryKind.BitVector,
        capacity=2,
        npoints=None,
        fidelity=1,
        reclaim=False,
        timeout=3600,
        basename=None,
        deadline=100,
        incremental=False,
        debug=False,
    )

    solver = MultiRobotTaskAllocation(options)

    # Run the solver.
    #
    # This will run the allocator with the selected backend solver an return a
    # plan based on the provided options, accordingly.
    solution = solver.solve(
        agents=agents,
        tasks=tasks,
        environment=graph
    )

    # Post-process the solution.
    #
    # The resulting solution from the given problem is now retrieved and stored,
    # accordingly. This allows for post-processing.
    print(json.dumps(solution, indent=2))


    # Plot Gannt chart
    agent_id = 0
    for agent_task in solution['agt']:
        print('agent', agent_id, '=', agent_task)
        agent_id = agent_id+1


if __name__ == r"__main__":
    main()
