from typing import Optional, List, Union, Text

from launch import Condition, LaunchContext, LaunchDescriptionEntity
from launch.action import Action
from launch.substitution import Substitution
from launch.frontend import Entity, Parser
import psutil


# TODO(jeduardo): Implement a launch action that checks if the gzserver (or
#  gzclient) process is running and kills it.

def get_process_pid(process: str) -> Optional[int]:
    """
    Verify if the provided process is running, and if it is return its PID.

    :param process: Name of the process to determine the PID.
    :return: PID of the running process, or None if a process with the
    specified name is not running.

    """
    low_proc = process.lower()
    for proc in psutil.process_iter():
        if proc.name().strip().lower() == low_proc:
            return proc.pid
    else:
        return None


def kill_process(pid: int) -> None:
    """Kill the process with the specified PID."""
    proc = psutil.Process(pid)
    proc.kill()


class KillProcess(Action):
    def __init__(
        self,
        pname: Union[Substitution, Text],
        condition: Optional[Condition] = None,
    ) -> None:
        super().__init__(condition=condition)

        from launch.utilities import normalize_to_list_of_substitutions
        self.__pname = normalize_to_list_of_substitutions(pname)[0]

    @property
    def pname(self) -> Substitution:
        """Return the name of the process that will be killed."""
        return self.__pname

    @classmethod
    def parse(cls, entity: Entity, parser: Parser):
        _, kwargs = super().parse(entity, parser)
        kwargs['pname'] = parser.parse_substitution(entity.get_attr("pname"))
        return cls, kwargs

    def execute(
        self, context: LaunchContext
    ) -> Optional[List[LaunchDescriptionEntity]]:
        # Resolve the process name
        process_name = self.pname.perform(context)
        # Get the process PID
        pid = get_process_pid(process_name)
        if pid is not None:
            # If the specified process is running. Kill it.
            kill_process(pid)

        # No other actions are needed, so we return None
        return None
