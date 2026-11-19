import typing
from dataclasses import dataclass
from Options import Option, Range, Toggle, PerGameCommonOptions, DefaultOnToggle, DeathLink, Choice, OptionGroup


class NotBeingStupid(DefaultOnToggle):
    """This changes nothing. You can toggle it on or off. Up to your preference"""
    display_name = "Not Being Stupid"

class PercentToGoal(Range):
    """What percentage of quests do you want to complete to goal your game?"""
    display_name = "Percent to Goal"
    range_start = 50
    range_end = 100
    default = 50

class RoomSanity(Toggle):
    """Every room that has dialogue or you can move around in is now a check"""
    display_name = "Room Sanity"
    default = False

@dataclass
class GBSOptions(PerGameCommonOptions):
    perc_to_goal: PercentToGoal
    death_link: DeathLink
    roomsanity: RoomSanity




option_definitions = {
    "stupid_people": NotBeingStupid,
}


option_groups_listss = [
    OptionGroup("Traps", [DeathLink]),
]