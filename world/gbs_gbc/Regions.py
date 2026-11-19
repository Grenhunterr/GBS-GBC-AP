from BaseClasses import Location, LocationProgressType, ItemClassification
from typing import Optional
from BaseClasses import Region, Entrance
from . import GBSItem
from .Locations import GBSLocation, location_table
from ..generic.Rules import add_rule




def create_regions(world):
    player = world.player
    multiworld = world.multiworld
    regmen = Region("Menu", player, multiworld, "Menu")
    multiworld.regions.append(regmen)

    reggui = Region("GUI", player, multiworld, "GUI")
    locgui_names = []
    reggui.locations += [GBSLocation(player, loc_name, location_table[loc_name], reggui) for loc_name in locgui_names]
    multiworld.regions.append(reggui)

    regparallax = Region("Parallax Example", player, multiworld, "Parallax Example")
    locparallax_names = []
    if world.options.roomsanity:
        locparallax_names.append("Room - path/Parallax Example")
    regparallax.locations += [GBSLocation(player, loc_name, location_table[loc_name], regparallax) for loc_name in locparallax_names]
    multiworld.regions.append(regparallax)

    regpathsamptown = Region("Path to Sample Town", player, multiworld, "Path to Sample Town")
    locpathsamptown_names = (["Turnip Trouble"])
    if world.options.roomsanity:
        locpathsamptown_names.append("Room - path/Path to Sample Town")
    world.add_event_to_region("Quest8", "Quest Completion", regpathsamptown, lambda state: state.has("Turnips", world.player))
    regpathsamptown.locations += [GBSLocation(player, loc_name, location_table[loc_name], regpathsamptown) for loc_name in locpathsamptown_names]
    multiworld.regions.append(regpathsamptown)

    regsamptown = Region("Sample Town", player, multiworld, "Sample Town")
    locsamptown_names = ["Missing Cat", "A Duck Mix-Up", "Hide N Seek", "Keep On The Grass"]
    world.add_event_to_region("Quest1", "Quest Completion", regsamptown, lambda state: state.has("Cat", world.player))
    world.add_event_to_region("Quest5", "Quest Completion", regsamptown, lambda state: state.has("Duck", world.player))
    world.add_event_to_region("Quest11", "Quest Completion", regsamptown, lambda state: state.has("Hider", world.player))
    world.add_event_to_region("Quest7", "Quest Completion", regsamptown, lambda state: state.has("Flower Lady", world.player))
    if world.options.roomsanity:
        locsamptown_names.append("Room - town/Sample Town")
    regsamptown.locations += [GBSLocation(player, loc_name, location_table[loc_name], regsamptown) for loc_name in locsamptown_names]
    multiworld.regions.append(regsamptown)

    regtophouse = Region("Top House", player, multiworld, "Top House")
    loctophouse_names = ["Ill Fitting Radio"]
    if world.options.roomsanity:
        loctophouse_names.append("Room - town/Top House")
    world.add_event_to_region("Quest3", "Quest Completion", regtophouse, lambda state: state.has("Radio", world.player))
    regtophouse.locations += [GBSLocation(player, loc_name, location_table[loc_name], regtophouse) for loc_name in loctophouse_names]
    multiworld.regions.append(regtophouse)

    regcave = Region("Cave", player, multiworld, "Cave")
    loccave_names = ["Sage Advice"]
    if world.options.roomsanity:
        loccave_names.append("Room - caves/Cave")
    world.add_event_to_region("Quest4", "Quest Completion", regcave, lambda state: state.has("Sage", world.player))
    regcave.locations += [GBSLocation(player, loc_name, location_table[loc_name], regcave) for loc_name in loccave_names]
    multiworld.regions.append(regcave)

    regsite = Region("Launch Site", player, multiworld, "Launch Site")
    locsite_names = []
    if world.options.roomsanity:
        locsite_names.append("Room - town/Launch Site")
    regsite.locations += [GBSLocation(player, loc_name, location_table[loc_name], regsite) for loc_name in locsite_names]
    multiworld.regions.append(regsite)

    regspace = Region("Space Battle", player, multiworld, "Space Battle")
    locspace_names = ["Sneak Onboard"]
    if world.options.roomsanity:
        locspace_names.append("Room - space/Space Battle")
    world.add_event_to_region("Quest9", "Quest Completion", regspace, lambda state: state.has("Rocket Ship", world.player))
    regspace.locations += [GBSLocation(player, loc_name, location_table[loc_name], regspace) for loc_name in locspace_names]
    multiworld.regions.append(regspace)

    regdeepspace = Region("Deep Space", player, multiworld, "Deep Space")
    locdeepspace_names = ["Space Dog"]
    if world.options.roomsanity:
        locdeepspace_names.append("Room - space/Deep Space")
    world.add_event_to_region("Quest6", "Quest Completion", regdeepspace, lambda state: state.has("Space Dog", world.player))
    regdeepspace.locations += [GBSLocation(player, loc_name, location_table[loc_name], regdeepspace) for loc_name in locdeepspace_names]
    multiworld.regions.append(regdeepspace)

    regunder = Region("Underground", player, multiworld, "Underground")
    locunder_names = ["Block Puzzle"]
    if world.options.roomsanity:
        locunder_names.append("Room - caves/Underground")
    world.add_event_to_region("Quest2", "Quest Completion", regunder, lambda state: state.has("Ice Block", world.player))
    regunder.locations += [GBSLocation(player, loc_name, location_table[loc_name], regunder) for loc_name in locunder_names]
    multiworld.regions.append(regunder)

    regdeepunder = Region("Deep Underground", player, multiworld, "Deep Underground")
    locdeepunder_names = ["Hidden Treasure"]
    if world.options.roomsanity:
        locdeepunder_names.append("Room - caves/Deeper Underground")
    world.add_event_to_region("Quest10", "Quest Completion", regdeepunder)
    regdeepunder.locations += [GBSLocation(player, loc_name, location_table[loc_name], regdeepunder) for loc_name in locdeepunder_names]
    multiworld.regions.append(regdeepunder)

    regmus = Region("Music House", player, multiworld, "Music House")
    locmus_names = []
    if world.options.roomsanity:
        locmus_names.append("Room - town/Music House")
    regmus.locations += [GBSLocation(player, loc_name, location_table[loc_name], regmus) for loc_name in locmus_names]
    multiworld.regions.append(regmus)

    regdream = Region("Dream", player, multiworld, "Dream")
    locdream_names = []
    if world.options.roomsanity:
        locdream_names.append("Room - Dream")
    regdream.locations += [GBSLocation(player, loc_name, location_table[loc_name], regdream) for loc_name in locdream_names]
    multiworld.regions.append(regdream)

    regplayhouse = Region("Player's House", player, multiworld, "Player's House")
    locplayhouse_names = []
    if world.options.roomsanity:
        locplayhouse_names.append("Room - Player's House")
    regplayhouse.locations += [GBSLocation(player, loc_name, location_table[loc_name], regplayhouse) for loc_name in
                           locplayhouse_names]
    multiworld.regions.append(regplayhouse)

    regend = Region("End", player, multiworld, "End")
#    location_end = GBSLocation(player, "Beaten Game", location_table["Beaten Game"], regend)
#    location_end.progress_type = LocationProgressType.EXCLUDED
#    regend.locations.append(location_end)
    multiworld.regions.append(regend)

def connect(world, name: str, source: str, target: str, rule=None, reach: Optional[bool] = False,
            rule_to_str: Optional[str] = None, ) -> Optional[Entrance]:
    source_region = world.multiworld.get_region(source, world.player)
    target_region = world.multiworld.get_region(target, world.player)

    connection = Entrance(world.player, name, source_region)

    if rule:
        connection.access_rule = rule

    source_region.exits.append(connection)
    connection.connect(target_region)


    #print(f"\nConnecting Region {source} to Region {target} with rule: {rule_to_str}\n")

    return connection if reach else None




def connect_entrances(world) -> None:
    connect(world, "Menu -> GUI", "Menu", "GUI")
    connect(world, "Start Game", "GUI", "Parallax Example")
    connect(world, "Parallax Example -> Path to Sample Town", "Parallax Example", "Path to Sample Town")
    connect(world, "Path to Sample Town -> Sample Town", "Path to Sample Town", "Sample Town")
    connect(world, "Path to Sample Town -> Player's House", "Path to Sample Town", "Player's House")
    connect(world, "Top House in Sample Town", "Sample Town", "Top House")
    connect(world, "Music House in Sample Town", "Sample Town", "Music House")
    connect(world, "Cave in Sample Town", "Sample Town", "Cave")
    connect(world, "Tunnel to Underground", "Sample Town", "Underground")
    connect(world, "Underground to Deep Underground", "Underground", "Deep Underground", lambda state: state.has("Ice Block", world.player))
    connect(world, "Sample Town to Launch Site", "Sample Town", "Launch Site")
    connect(world, "Launch Site to Space Battle", "Launch Site", "Space Battle", lambda state: state.has("Rocket Ship", world.player))
    connect(world, "Space Battle to Deep Space", "Space Battle", "Deep Space")
    connect(world, "All A Dream", "Deep Space", "Dream")
    connect(world, "Do Req Quests", "Sample Town", "End")


