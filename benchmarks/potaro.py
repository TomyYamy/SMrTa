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
    for agent_id, _ in enumerate(solution['agt']):
        #assigned_task_ids = [task_id for task_id, assigned_agent_id in enumerate(solution['t2a'][0]) if assigned_agent_id == agent_id]
        assigned_task_ids = [task_id for task_id, assigned_agent_id in enumerate(solution['t2a']) if assigned_agent_id[0] == agent_id]
        print('agent', agent_id, '=', assigned_task_ids)
        for assigned_task_id in assigned_task_ids:
            #task = tasks[0][0][assigned_task_id]
            task = tasks[assigned_task_id][0][0]
            original_cost = graph[task.start][task.end]
            #start_time = solution['ts'][0][assigned_task_id]
            start_time = solution['ts'][assigned_task_id][0]
            #end_time = solution['td'][0][assigned_task_id]
            end_time = solution['td'][assigned_task_id][0]
            print('task', assigned_task_id, 'start_time =', start_time, 'end_time =', end_time,'original_cost =', original_cost)
            cost = end_time - start_time

            label = assigned_task_id
            cmap = plt.get_cmap('tab10')
            ec = cmap.colors[assigned_task_id%len(cmap.colors)]
            p = ax.barh(y=f'agent {agent_id}', width=cost, left=start_time, label=f'{label}:{task.start}->{task.end}', color=(0,0,0,0), ec=ec, linewidth=3)
            ax.bar_label(p, labels=[label], label_type='center')

            scores.append(task.deadline-end_time)

    total_score = sum(scores)
    print('score =', total_score)

    ax.legend(loc='upper left', bbox_to_anchor=(1.05, 1))
    fig.tight_layout()
    plt.show()
    plt.clf()
    #plt.close()

if __name__ == r"__main__":
    main()
