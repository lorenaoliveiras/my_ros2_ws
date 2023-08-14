from typing import Optional, List

from launch import LaunchContext, LaunchDescriptionEntity, Condition
from launch.action import Action
from launch.actions import GroupAction
from launch.frontend import Entity, Parser


# TODO(jeduardo): Implement the ExecuteInSequence action.


class ExecuteInSequence(Action):
    def __init__(self, *, condition: Optional[Condition] = None) -> None:
        super().__init__(condition=condition)

    @staticmethod
    def parse(entity: Entity, parser: Parser):
        return super().parse(entity, parser)

    def get_sub_entities(self) -> List[LaunchDescriptionEntity]:
        return super().get_sub_entities()

    def execute(self, context: LaunchContext) -> Optional[
        List[LaunchDescriptionEntity]]:
        return super().execute(context)