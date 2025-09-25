import json
import matplotlib.pyplot as plt

import smrta.create_randomized_inputs as cri
import smrta.run_realistic_setting as rrs

from pathlib import Path
from smrta.solver import MultiRobotTaskAllocation
from smrta.solver import Options
from smrta.solver import SolverKind, TheoryKind


def main():
    """The main entrypoint.
    """

    path = Path(__file__).resolve().parent

    # We load the room graph, first.
    #
    # This is a specific format that may be viewed by printing the data structure
    # after it has been un-pickled, accordingly.
    #filename = path.joinpath("potaro/potaro_weighted_graph.pickle")
    filename = path.joinpath("potaro/potaro_weighted_graph4log.pickle")
    count, graph = rrs.dictionary_to_matrix(rrs.load_weighted_graph(file_name=str(filename)))

    # We load the agents and tasks, next.
    #
    # This will load the configuration file needed to set up the agents and theory
    # tasks for the solver to solve.
    #filename = path.joinpath("potaro/test_case.json")
    filename = path.joinpath("potaro/test_case4log_30mins.json")
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
        incremental=True,
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
    plt.rcParams['pdf.fonttype'] = 42
    fig, ax = plt.subplots()
    ax.invert_yaxis()

    scores = []
    task_id_count = 0
    for increment_index, _ in enumerate(solution['t2a']):
        for local_index, assigned_agent in enumerate(solution['t2a'][increment_index]):
            task = tasks[increment_index][0][local_index] # task = ([index: start_node_id -> target_node_id[deadline]], issued_time)
            original_cost = graph[task.start][task.end]
            start_time = solution['ts'][increment_index][local_index]
            end_time = solution['td'][increment_index][local_index]
            print(f'agent:{assigned_agent} task:{task_id_count} start_time:{start_time} end_time ={end_time} original_cost ={original_cost}')
            cost = end_time - start_time

            label = task_id_count
            cmap = plt.get_cmap('tab10')
            ec = cmap.colors[task_id_count%len(cmap.colors)]
            p = ax.barh(y=f'agent {assigned_agent}', width=cost, left=start_time, label=f'{label}:{task.start}->{task.end}', color=(0,0,0,0), ec=ec, linewidth=3)
            ax.bar_label(p, labels=[label], label_type='center')

            task_id_count = task_id_count + 1

            scores.append(task.deadline-end_time) #TODO: score is just travel time. Make it execution time.

    total_score = sum(scores)
    print('score =', total_score)

    ax.legend(loc='upper left', bbox_to_anchor=(1.05, 1))
    fig.tight_layout()
    plt.show()
    plt.clf()
    #plt.close()

    # Print number of assigned tasks for each agent
    accumulate_dic = {}
    for increment_agent_assignments in solution['t2a']:
        for assigned_agent in increment_agent_assignments:
            if accumulate_dic.get(assigned_agent) == None:
                accumulate_dic.update({assigned_agent: 1})
            else:
                accumulate_dic[assigned_agent] = accumulate_dic[assigned_agent] + 1
    print(f'assigned tasks for each agent: {accumulate_dic}')


if __name__ == r"__main__":
    main()
