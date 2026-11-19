from platform import system
from typing import TYPE_CHECKING
import asyncio
import logging
from NetUtils import ClientStatus

import random
import worlds._bizhawk as bizhawk
from worlds._bizhawk.client import BizHawkClient
from worlds.AutoWorld import World

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext, BizHawkClientCommandProcessor

logger = logging.getLogger("Client")
rudeness = 0
funnydeath = 0



# def cmd_rude(self: "BizHawkClientCommandProcessor") -> None:
#     """Toggles the Rude Messages"""
#     if self.ctx.game != "GB Studio - GameBoy Color Template Game":
#         logger.warning("This command can only be used when playing GB Studio - GameBoy Color Template Game.")
#         return
#     if not self.ctx.server or not self.ctx.slot:
#         logger.warning("You must be connected to a server to use this command.")
#         return
#
#     global rudeness
#     rudeness ^= 1
#     logger.warning("Rude messages enabled." if rudeness else "Rude messages disabled.")
#
# def cmd_death(self: "BizHawkClientCommandProcessor") -> None:
#     """When toggled, this command will turn on the funny death messages instead of having actually useful ones."""
#     if self.ctx.game != "GB Studio - GameBoy Color Template Game":
#         logger.warning("This command can only be used when playing GB Studio - GameBoy Color Template Game.")
#         return
#     if not self.ctx.server or not self.ctx.slot:
#         logger.warning("You must be connected to a server to use this command.")
#         return
#
#     global funnydeath
#     funnydeath ^= 1
#     logger.warning("Funny death messages enabled." if funnydeath else "Funny death messages disabled.")

class GBSClient(BizHawkClient):
    game = "GB Studio - GameBoy Color Template Game"           # Match this with your World name
    system = "GBC"                  # SNES, GBA, etc.
    patch_suffix = ".apgbs"    # Optional: show these files in "Open Patch"
    death_link_ready = False
    previous_death_link = 0
    tagged = -1
    hinted_claw = False
    hinted_store = False

    def __init__(self):
        super().__init__()
        self.checked_locations = set()

    async def send_check(self, ctx, location_id):
        if location_id not in self.checked_locations:
            self.checked_locations.add(location_id)
            await ctx.send_msgs([{
                "cmd": "LocationChecks",
                "locations": [location_id]
            }])


    async def validate_rom(self, ctx: "BizHawkClientContext") -> bool:
        try:
            # Read some identifying bytes from ROM
            print("attempting read from 0x0134 for the name")
            logger.warning("attempting read from 0x0134 for the name")
            rom_name_bytes = await bizhawk.read(ctx.bizhawk_ctx, [(0x0134, 8, "ROM")])
            print("rom name is being decoded")
            logger.warning("rom name is being decoded")
            rom_name = rom_name_bytes[0].decode("ascii")

            logger.warning("rom name is " + str(rom_name))
            print("rom name is " + str(rom_name))
            if rom_name != "GBSGBCAP":  # Replace with actual expected header or identifier
                logger.warning("rom name is not GBSGBCAP")
                print("rom name is not GBSGBCAP")
                return False
            ctx.game = self.game
            ctx.items_handling = 0b011  # Server sends items
            ctx.want_slot_data = True

            # if "rudeness" in ctx.command_processor.commands:
            #     ctx.command_processor.commands.pop("rudeness")
            #
            # if "funny_death" in ctx.command_processor.commands:
            #     ctx.command_processor.commands.pop("funny_death")
            #
            # if "rudeness" not in ctx.command_processor.commands:
            #     ctx.command_processor.commands["rudeness"] = cmd_rude
            #
            # if "funny_death" not in ctx.command_processor.commands:
            #     ctx.command_processor.commands["funny_death"] = cmd_death

            return True
        except bizhawk.RequestFailedError:
            logger.warning("connector didn't respond or couldn't verify rom name")
            return False  # Can't confirm ROM, deny

        # ROM is valid


    async def game_watcher(self, ctx: "BizHawkClientContext") -> None:

        if ctx.server is None or ctx.server.socket.closed or ctx.slot_data is None:
            return

        try:

            # Read necessary WRAM bytes from memory
            ram_data = (await bizhawk.read(ctx.bizhawk_ctx, [
                (0x0441, 1, "WRAM"),  # Goal
                # Quest 1-11
                (0x0419, 1, "WRAM"),
                (0x041B, 1, "WRAM"),
                (0x041D, 1, "WRAM"),
                (0x041F, 1, "WRAM"),
                (0x0421, 1, "WRAM"),
                (0x0423, 1, "WRAM"),
                (0x0425, 1, "WRAM"),
                (0x0427, 1, "WRAM"),
                (0x0429, 1, "WRAM"),
                (0x042B, 1, "WRAM"),
                (0x042D, 1, "WRAM"),

                (0x0447, 1, "WRAM"), # deathlink and death reason. 1 = pit, 2 = Turnip I think
                (0x043B, 1, "WRAM"), # health value

                (0x0CFF, 1, "WRAM"), # supposedly empty spot in memory

                (0x045F, 1, "WRAM"), # current room
            ]))


            await self.handle_death_link(ctx, ram_data[13][0])
            if self.tagged < 0:
                if ctx.slot_info is not None:
                    if ctx.slot_data.get("death_link") == 0:
                        self.tagged = 0
                        await ctx.update_death_link(False)
                    else:
                        self.tagged = 1
                        self.previous_death_link = ctx.bizhawk_ctx
                        await ctx.update_death_link(True)


            # EXAMPLE: Trigger a location check if bit 3 of byte 0x02000004 is set
            if ram_data[1][0] == 1:
                await self.send_check(ctx, 1)

            if ram_data[2][0] == 1:
                await self.send_check(ctx, 2)

            if ram_data[3][0] == 1:
                await self.send_check(ctx, 3)

            if ram_data[4][0] == 1:
                await self.send_check(ctx, 4)

            if ram_data[5][0] == 1:
                await self.send_check(ctx, 5)

            if ram_data[6][0] == 1:
                await self.send_check(ctx, 6)

            if ram_data[7][0] == 1:
                await self.send_check(ctx, 7)

            if ram_data[8][0] == 1:
                await self.send_check(ctx, 8)

            if ram_data[9][0] == 1:
                await self.send_check(ctx, 9)

            if ram_data[10][0] == 1:
                await self.send_check(ctx, 10)

            if ram_data[11][0] == 1:
                await self.send_check(ctx, 11)

            if ctx.slot_data.get("perc_to_goal") != 0:
                if ram_data[15][0] == 1:
                    await self.send_check(ctx, 12)
                elif ram_data[15][0] == 2:
                    await self.send_check(ctx, 13)
                elif ram_data[15][0] == 3:
                    await self.send_check(ctx, 14)
                elif ram_data[15][0] == 4:
                    await self.send_check(ctx, 15)
                elif ram_data[15][0] == 5:
                    await self.send_check(ctx, 16)
                elif ram_data[15][0] == 6:
                    await self.send_check(ctx, 17)
                elif ram_data[15][0] == 7:
                    await self.send_check(ctx, 18)
                elif ram_data[15][0] == 8:
                    await self.send_check(ctx, 19)
                elif ram_data[15][0] == 9:
                    await self.send_check(ctx, 20)
                elif ram_data[15][0] == 10:
                    await self.send_check(ctx, 21)
                elif ram_data[15][0] == 11:
                    await self.send_check(ctx, 22)
                elif ram_data[15][0] == 12:
                    await self.send_check(ctx, 23)
                elif ram_data[15][0] == 13:
                    await self.send_check(ctx, 24)



            #enemy hits this is going to be great
            received_index = ram_data[14][0]



            for i in range(len(ctx.items_received) - received_index):
                if ctx.items_received[received_index + i].item == 1: # Cat
                    await bizhawk.write(ctx.bizhawk_ctx, [(0x0449, [1], "WRAM")])
                    await bizhawk.write(ctx.bizhawk_ctx, [(0x0CFF, [received_index + i + 1], "WRAM")])

                elif ctx.items_received[received_index + i].item == 2: # Ice Block
                    await bizhawk.write(ctx.bizhawk_ctx, [(0x044B, [1], "WRAM")])
                    await bizhawk.write(ctx.bizhawk_ctx, [(0x0CFF, [received_index + i + 1], "WRAM")])

                elif ctx.items_received[received_index + i].item == 3: # Radio
                    await bizhawk.write(ctx.bizhawk_ctx, [(0x044D, [1], "WRAM")])
                    await bizhawk.write(ctx.bizhawk_ctx, [(0x0CFF, [received_index + i + 1], "WRAM")])

                elif ctx.items_received[received_index + i].item == 4: # Sage
                    await bizhawk.write(ctx.bizhawk_ctx, [(0x044F, [1], "WRAM")])
                    await bizhawk.write(ctx.bizhawk_ctx, [(0x0CFF, [received_index + i + 1], "WRAM")])

                elif ctx.items_received[received_index + i].item == 5: # Duck
                    await bizhawk.write(ctx.bizhawk_ctx, [(0x0451, [1], "WRAM")])
                    await bizhawk.write(ctx.bizhawk_ctx, [(0x0CFF, [received_index + i + 1], "WRAM")])

                elif ctx.items_received[received_index + i].item == 6: # Dog
                    await bizhawk.write(ctx.bizhawk_ctx, [(0x0453, [1], "WRAM")])
                    await bizhawk.write(ctx.bizhawk_ctx, [(0x0CFF, [received_index + i + 1], "WRAM")])

                elif ctx.items_received[received_index + i].item == 7: # Flower Lady
                    await bizhawk.write(ctx.bizhawk_ctx, [(0x0455, [1], "WRAM")])
                    await bizhawk.write(ctx.bizhawk_ctx, [(0x0CFF, [received_index + i + 1], "WRAM")])

                elif ctx.items_received[received_index + i].item == 8: # Turnips
                    await bizhawk.write(ctx.bizhawk_ctx, [(0x0457, [1], "WRAM")])
                    await bizhawk.write(ctx.bizhawk_ctx, [(0x0CFF, [received_index + i + 1], "WRAM")])

                elif ctx.items_received[received_index + i].item == 9: # Rocket Ship
                    await bizhawk.write(ctx.bizhawk_ctx, [(0x0459, [1], "WRAM")])
                    await bizhawk.write(ctx.bizhawk_ctx, [(0x0CFF, [received_index + i + 1], "WRAM")])

                elif ctx.items_received[received_index + i].item == 10: # Hider
                    await bizhawk.write(ctx.bizhawk_ctx, [(0x045B, [1], "WRAM")])
                    await bizhawk.write(ctx.bizhawk_ctx, [(0x0CFF, [received_index + i + 1], "WRAM")])

                elif ctx.items_received[received_index + i].item == 11: # House Key
                    await bizhawk.write(ctx.bizhawk_ctx, [(0x045D, [1], "WRAM")])
                    await bizhawk.write(ctx.bizhawk_ctx, [(0x0CFF, [received_index + i + 1], "WRAM")])




            # EXAMPLE: Send goal completion when bit 0 of byte 0x02000006 is set
            if not ctx.finished_game and (ram_data[0][0] == 1):
                await ctx.send_msgs([{
                    "cmd": "StatusUpdate",
                    "status": ClientStatus.CLIENT_GOAL
                }])
                ctx.finished_game = True





        except bizhawk.RequestFailedError:
            # BizHawk might have lost connection—just skip this frame
            return

        if ctx.slot_info is not None:
            percentage_variable = ctx.slot_data.get("perc_to_goal")
            if ctx.slot_data.get("perc_to_goal") != 0:
                await bizhawk.write(ctx.bizhawk_ctx, [(0x0445, [percentage_variable], "WRAM")])
            #
            # if ctx.slot_data.get("route") == 1:
            #     await bizhawk.write(ctx.bizhawk_ctx, [(0x0B9E, [1], "WRAM")])
            #
            # if ctx.slot_data.get("hidden_secret_stuff") == 1:
            #     await bizhawk.write(ctx.bizhawk_ctx, [(0x0B9A, [1], "WRAM")])
            #
            # if ctx.slot_data.get("secret_shop") == 1:
            #     await bizhawk.write(ctx.bizhawk_ctx, [(0x0C58, [1], "WRAM")])


    async def handle_death_link(self, ctx: "BizHawkClientContext", ghost_health: int) -> None:

        if ctx.slot_data.get("death_link") == 1 or ctx.slot_data.get("death_link") == True:

            death_reason = (await bizhawk.read(ctx.bizhawk_ctx, [(0x0447, 1, "WRAM")]))[0][0]

            if not self.death_link_ready:
                if ghost_health > 0:
                    self.death_link_ready = True
                    return
                return

            if self.previous_death_link != ctx.last_death_link:
                if self.death_link_ready:
                    await bizhawk.write(ctx.bizhawk_ctx, [(0x043B, [0], "WRAM")])
                    self.death_link_ready = False
                    self.previous_death_link = ctx.last_death_link

            if ghost_health == 0:


                if death_reason == 1:
                    await ctx.send_death(f"{ctx.player_names[ctx.slot]} fell in a pit.")
                    logger.warning(f"{ctx.player_names[ctx.slot]} fell in a pit.")
                elif death_reason == 2:
                    await ctx.send_death(f"{ctx.player_names[ctx.slot]} died to a Turnip.")
                    logger.warning(f"{ctx.player_names[ctx.slot]} died to a Turnip.")



                self.previous_death_link = ctx.last_death_link
                self.death_link_ready = False