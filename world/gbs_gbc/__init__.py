import settings
import typing

from Options import OptionError
from Utils import visualize_regions
from .Options import GBSOptions, option_groups_listss  # the options we defined earlier
from .Items import GBSItem, item_table  # data used below to add items to the World
from .Locations import GBSLocation, location_table  # same as above
from worlds.AutoWorld import World, WebWorld
from BaseClasses import Region, Location, Entrance, Item, ItemClassification, MultiWorld, CollectionState, \
    LocationProgressType
from .Regions import create_regions, connect_entrances
from .client import GBSClient
from ..generic.Rules import add_rule, set_rule


class MyGameSettings(settings.Group):
    class RomFile(settings.UserFilePath):
        """Insert help text for host.yaml here."""
        #rom_file: RomFile = RomFile("SSAP.gb")
        description =  "GB Studios GameBoy Color Template AP ROM"
        copy_to = "GBC AP ROM which is totally legit and fully functioning.gb"
        md5s = ["E9773D4BE958C4C00C8E7A740554C563"]

    rom_file: RomFile = RomFile(RomFile.copy_to)
    rom_start: bool = True



class GBSWeb(WebWorld):
    theme = "stone"
    option_groups = option_groups_listss
    options_presets = {
        "GB Studio - GameBoy Color Template Game": {
            "stupid_people": True,
            "route": False,
            "oob_coins": False,
            "hidden_secret_stuff": False,
            "progress_per_lvl": False,
        }
    }


class GBSWorld(World):
    """GB Studio's GameBoy Color Template Game now for Archipelago!"""
    game = "GB Studio - GameBoy Color Template Game"  # name of the game/world
    options_dataclass = GBSOptions  # options the player can set
    options: GBSOptions  # typing hints for option results
    settings: typing.ClassVar[MyGameSettings]  # will be automatically assigned from type hint
    topology_present = False  # show path to required location checks in spoiler
    web = GBSWeb()





    # ID of first item and location, could be hard-coded but code may be easier
    # to read with this as a property.
    base_id = 1
    # instead of dynamic numbering, IDs could be part of data

    # The following two dicts are required for the generation to know which
    # items exist. They could be generated from json or something else. They can
    # include events, but don't have to since events will be placed manually.
    item_name_to_id = {name: id for
                       name, id in item_table.items()}
    location_name_to_id = {name: id for
                           name, id in location_table.items()}

    # Items can be grouped using their names to allow easy checking if any item
    # from that group has been collected. Group names can also be used for !hint

    def add_event_to_region(self, event_name: str, event_item_name: str, region: Region, access_rules=None):
        created_event = GBSLocation(self.player, event_name, None, region)
        if access_rules is not None:
            created_event.access_rule = access_rules
        created_event.show_in_spoiler = False
        created_event.place_locked_item(GBSItem(event_item_name, ItemClassification.progression, None, self.player))
        created_event.progress_type = LocationProgressType.PRIORITY
        region.locations.append(created_event)


    def __init__(self, multiworld, player):
        super().__init__(multiworld, player)



    def create_regions(self):
        create_regions(self)
        print(str(round(11 * (self.options.perc_to_goal / 100))) + " is how many quests are needed to complete this AP")
        if self.options.perc_to_goal == 100:
            self.multiworld.completion_condition[self.player] = lambda state: state.can_reach("End", "Region",
                                                                                              self.player) and state.has(
                "Quest Completion", self.player, round(11 * (self.options.perc_to_goal / 100))) and state.has(
                "Cat", self.player) and state.has("Ice Block", self.player) and state.has("Radio", self.player) and state.has(
                "Sage", self.player) and state.has("Duck", self.player) and state.has("Space Dog", self.player) and state.has(
                "Flower Lady", self.player) and state.has("Turnips", self.player) and state.has("Rocket Ship", self.player) and state.has("Hider", self.player)

        else:
            self.multiworld.completion_condition[self.player] = lambda state: state.can_reach("End", "Region", self.player) and state.has("Quest Completion", self.player, round(11 * (self.options.perc_to_goal / 100)))

    def generate_basic(self) -> None:
        # state: CollectionState = self.multiworld.get_all_state()
        # state.update_reachable_regions(self.player)
        # reachable_regions: set[Region] = set(state.reachable_regions[self.player])
        # unreachable_regions: set[Region] = set()  # type: ignore
        # for region in self.multiworld.regions:
        #     if region not in reachable_regions:
        #         unreachable_regions.add(region)
        # visualize_regions(root_region=self.get_region(region_name="Menu"), file_name=f"{self.player_name}_world.puml",
        #                   show_entrance_names=True, regions_to_highlight=unreachable_regions)

        return super().generate_basic()


    def create_item(self, name: str) -> "Item":
        return Item(name, ItemClassification.progression, self.item_name_to_id[name], self.player)

    def create_items(self):

        totalItems = len(self.multiworld.get_unfilled_locations(self.player))
        itemvariable = 1
        item_to_give = self.random.randint(1, 10)
        print(str(self.item_id_to_name[item_to_give]))
        while itemvariable != 11:
            if not self.options.roomsanity:
                if item_to_give != itemvariable:
                    self.multiworld.itempool.append(Item(str(self.item_id_to_name[itemvariable]), ItemClassification.progression, itemvariable, self.player))
                    print("Added " + str(self.item_id_to_name[itemvariable]))
                else:
                    self.multiworld.push_precollected(self.create_item(str(self.item_id_to_name[itemvariable])))
                    print("Gave " + str(self.item_id_to_name[item_to_give]))
                    totalItems += 1
            else:
                self.multiworld.itempool.append(Item(str(self.item_id_to_name[itemvariable]), ItemClassification.progression, itemvariable, self.player))
            itemvariable += 1
            totalItems -= 1
        totalItems = len(self.multiworld.get_unfilled_locations(self.player))
        if totalItems >= 1:
            while totalItems != 0:
                self.multiworld.itempool.append(Item(str(self.item_id_to_name[12]), ItemClassification.filler, 12, self.player))
                totalItems -= 1

        set_rule(self.get_location("Missing Cat"), lambda state: state.has("Cat", self.player))
        set_rule(self.get_location("Block Puzzle"), lambda state: state.has("Ice Block", self.player))
        set_rule(self.get_location("Ill Fitting Radio"), lambda state: state.has("Radio", self.player))
        set_rule(self.get_location("Sage Advice"), lambda state: state.has("Sage", self.player))
        set_rule(self.get_location("A Duck Mix-Up"), lambda state: state.has("Duck", self.player))
        set_rule(self.get_location("Space Dog"), lambda state: state.has("Space Dog", self.player))
        set_rule(self.get_location("Keep On The Grass"), lambda state: state.has("Flower Lady", self.player))
        set_rule(self.get_location("Turnip Trouble"), lambda state: state.has("Turnips", self.player))
        set_rule(self.get_location("Sneak Onboard"), lambda state: state.has("Rocket Ship", self.player))
        set_rule(self.get_location("Hide N Seek"), lambda state: state.has("Hider", self.player))






    def connect_entrances(self) -> None:
        connect_entrances(self)


        # from Utils import visualize_regions
        # visualize_regions(self.multiworld.get_region("Menu", self.player), f"{self.player_name}_SeveredSoul_world.puml", show_entrance_names=True, regions_to_highlight=self.multiworld.get_all_state(self.player).reachable_regions[self.player])

    def fill_slot_data(self) -> dict[str, any]:
        # In order for our game client to handle the generated seed correctly we need to know what the user selected
        # for their difficulty and final boss HP.
        # A dictionary returned from this method gets set as the slot_data and will be sent to the client after connecting.
        # The options dataclass has a method to return a `Dict[str, Any]` of each option name provided and the relevant
        # option's value.
        names = ["death_link", "perc_to_goal", "roomsanity"]
        return self.options.as_dict(*names)