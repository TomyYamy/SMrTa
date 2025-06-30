import math
import smrta.create_randomized_inputs as cri
import smrta.run_realistic_setting as rrs

from importlib.resources import files, as_file
from smrta.MRTASolver import MRTASolver
from smrta.bin.smrta.cli import cli

# The main function.
#
# This is the main entrypoint for running the application from the command-line,
# accordingly.
def main():
    arguments = cli().parse_args()

    # Load the configuration file and room graph.
    #
    # This will load the agent configurations from the file and pre-process data
    # to correctly call the solver.
    agents, ts = cri.load_config(arguments.file)

    with as_file(files("smrta.data").joinpath("weighted_graph_p3.pkl")) as path:
        count, graph = rrs.dictionary_to_matrix(rrs.load_weighted_graph(
            file_name=str(path)
        ))

    # Compute the number of APS.
    #
    # This will compute the number of APS based on the number of total tasks
    # divided by the number of agents.
    aps = math.ceil(sum([len(tasks) for tasks, _ in ts]) / len(agents)) * 2 + 1

    # Call the solver.
    #
    # This will supply the correct arguments to the solver and run it,
    # accordingly.
    MRTASolver(
        solver_name=arguments.solver,
        theory=arguments.theory,
        agents=agents,
        tasks_stream=ts,
        room_graph=graph,
        capacity=arguments.capacity,
        num_aps=aps if not arguments.num_aps else arguments.num_aps,
        fidelity=arguments.fidelity,
        free_action_points=(not arguments.keep_aps),
        timeout=arguments.timeout,
        basename=arguments.export,
        default_deadline=arguments.deadline,
        aps_list=list(range(3, aps + 1, 2)),
        incremental=arguments.incremental,
        debug=arguments.verbose,
    )
