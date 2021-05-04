import asyncio

# import r6statsAPI as r6statsAPI
import r6statsapi
# import configparser

loop = asyncio.get_event_loop()
# from AsyncioCurl import AsyncioCurl
client = r6statsapi.Client("05b6451c-f8ab-49fd-af25-2f216cfd6157")
# settings = configparser.ConfigParser()
# settings.read("settings.ini")
# username = settings["PLAYERDATA"]["username"]

# async def getGenData(un):
#     playergendata = await loop.run_until_complete(client.get_generic_stats(un, r6statsapi.Platform.uplay))
#     # await playergendata
#     # await asyncio.current_task.close()  # added this line
#     with("testgendata.txt", "a+") as f:
#         for line in playergendata:
#             await f.write(line)

if __name__ == "__main__":
    playerdata = loop.run_until_complete(client.get_generic_stats("infrared.", r6statsapi.Platform.uplay))
    playerseasondata = loop.run_until_complete(client.get_seasonal_stats("toozestyy", r6statsapi.Platform.uplay))
    # playerdata = loop.run_until_complete(client.get_generic_stats("toozestyy", r6statsapi.Platform.uplay))
    print(playerdata.lootbox_probability)
    # print(playerseasondata.seasons)
    for key in playerseasondata.seasons["crimson_heist"]:
        print(key)
    print(playerseasondata.seasons)
    # print(playerseasondata.seasons["crimson_heist"])
    # getGenData("toozestyy")
