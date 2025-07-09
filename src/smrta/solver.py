import math

from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path
from typing import List, Optional

from smrta.MRTASolver import MRTASolver as MultiRobotTaskAllocationSolver


class SolverKind(StrEnum):
    """The supported solver backends.
    """

    Bitwuzla = "bitwuzla"
    Zapatho = "z3"
    CooperatingValidityChecker = "cvc5"


class TheoryKind(StrEnum):
    """The supported theory implementations.
    """

    Integer = "QF_UFLIA"
    BitVector = "QF_UFBV"


@dataclass
class Options:
    """A set of options for the MultiRobotTaskAllocation.
    """

    solver: SolverKind       # The kind of SMT-based solver backend to use.
    theory: TheoryKind       # The kind of theory to use.
    capacity: int            # The maximum limit of the agents.
    npoints: Optional[int]   # The number of action points to use.
    fidelity: int            # The fidelity of the travel times.
    reclaim: bool            # If yes, free previously allocated action points.
    timeout: int             # The wall-time for the solver (in seconds).
    basename: Optional[Path] # The basename of the benchmark file to export.
    deadline: int            # The default deadline for tasks.
    incremental: bool        # If yes, use incremental solving.
    debug: bool              # If yes, print additional debug-based information.


class MultiRobotTaskAllocation:
    """An interface for the Multi-Robot Task Allocation solver.
    """

    def __init__(self, options: Options) -> None:
        """Initialize the Multi-Robot Task Allocation Solver.

        This initialization step is used to set options for the solver before it
        is ran, accordingly.
        """

        self.options = options

    def solve(self, agents, tasks, environment):
        """Solve the problem.

        This will solve the problem based on the provided agents, tasks, and the
        given environment, accordingly.
        """

        # Compute the number of actions points.
        #
        # This is pre-computed based on the number of total tasks in the problem
        # and the number of agents available.
        #
        # NOTE: This calculation is directly taken from the original code.
        # Therefore, the exact expression cannot be explained, only trusted.
        apts = math.ceil(sum([len(t) for t, _ in tasks]) / len(agents)) * 2 + 1

        # Run the solver.
        #
        # This runs the solver with all the specified arguments and options based
        # on the previously provided items, accordingly.
        solver = MultiRobotTaskAllocationSolver(
            solver_name=str(self.options.solver),
            theory=str(self.options.theory),
            agents=agents,
            tasks_stream=tasks,
            room_graph=environment,
            capacity=self.options.capacity,
            num_aps=self.options.npoints if self.options.npoints else apts,
            fidelity=self.options.fidelity,
            free_action_points=self.options.reclaim,
            timeout=self.options.timeout,
            basename=self.options.basename,
            default_deadline=self.options.deadline,
            aps_list=list(range(3, apts + 1, 2)),
            incremental=self.options.incremental,
            debug=self.options.debug
        )

        return solver.sol
