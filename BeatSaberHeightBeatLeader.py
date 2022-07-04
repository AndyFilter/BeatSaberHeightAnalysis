import matplotlib.pyplot as plt
import requests
import json
from types import SimpleNamespace
import time
from multiprocessing.pool import ThreadPool
from os.path import exists
from scipy.interpolate import make_interp_spline
import numpy as np
import DecodeBeatReplay

mapId = "1dc9471"
_mapId = input("Enter Map Id: ")

if(len(_mapId) > 3 or len(_mapId) > 16):
    mapId = _mapId
else:
    print("Map Id is invalid")
    quit()

beatLeaderUrl = f'https://api.beatleader.xyz/leaderboard/{mapId}'

pages = 1
pagesLimit = 24
itemsScanned = 0


class Score:
    id: int
    playerId: str
    rank: int
    replay: str


class Scores:
    scores: list


class Metadata:
    total: int
    page: int
    itemsPerPage: int



class Player:
    id: str
    rank: int
    height: float
    def __init__(self, _id, _rank, _height):
        self.id = _id
        self.rank = _rank
        self.height = _height


class PlayerInfo:  # This class does nothing (-;
    id: str
    rank: int
    height: float
    def __init__(self, _id, _rank, _replay):
        self.id = _id
        self.rank = _rank
        self.replay = _replay


fileName = f"Players_{mapId}_BeatLeader.txt"
playersHeights = {}

def SaveData(fileName: str):
    file = open(fileName, "w")
    for player in playersHeights:
        file.write(f'{player}~,~{playersHeights[player]}\n')
    file.close()


def ReadData(filename: str):
    global playersHeights
    _playersHeights = {}
    file = open(filename, "r").readlines()
    for i, line in enumerate(file):
        values = line.split("~,~")
        _playersHeights[values[0]] = values[1].removesuffix("\n")
    #print(_playersHeights)
    playersHeights = _playersHeights

if(exists(fileName)):
    ReadData(fileName)

foundPlayers: list = []
playerHeights = {}
playerInfos = {}

pageNum: int = 1
scannedPages = 0

while (pageNum <= min(pages, pagesLimit)):
    scannedPages += 1
    print(f"page {pageNum}")
    data = requests.get(f"{beatLeaderUrl}?page={pageNum}", headers={'Accept-Encoding': 'gzip, deflate'})
    j = json.loads(data.text, object_hook=lambda d: SimpleNamespace(**d))
    pages = (j.plays // 10) + 1

    j: Scores = j

    for score in j.scores:
        score: Score = score
        #print(score.playerId)
        playerHeights[score.playerId] = score.rank
        playerInfos[score.playerId] = PlayerInfo(score.playerId, score.rank, score.replay)
        itemsScanned += 1
        if (len(score.replay) > 0):
            #print(score.replay)
            foundPlayers.append(score.playerId)

    pageNum += 1


def GetPlayerHeight(playerId: str):
    if(playersHeights.__contains__(playerId)):
        return playerId, playersHeights[playerId]

    beatLeaderUrl = playerInfos[playerId].replay
    with requests.get(beatLeaderUrl, headers={'Accept-Encoding': 'gzip, deflate', 'Range': 'bytes=0-420'}) as data:
        if(data.status_code != 206):  # This status code means success with only specified bytes range
            return

        replay = DecodeBeatReplay.DecodeReplay(data.content)
        height = replay.height
        return (playerId, height)


print(f"Running Threads ({len(foundPlayers)})")
start_time = time.time()
# thread amount is limited to 10 to prevent reaching the request rate limit
results = ThreadPool(10).imap_unordered(GetPlayerHeight, foundPlayers)

_th = 0
for r in results:
    _th += 1  # I don't really care about the order of threads as long as all of them finish
    if r is not None:
        print("Task", _th, "finished")
        playersHeights[r[0]] = r[1]

print(f"Time taken {time.time() - start_time}s")

SaveData(fileName)


def SortPlayers(amount: int = 24):
    global playerHeights, playersHeights
    sorted = [0]*amount
    for player in playersHeights:
        if (playerHeights.__contains__(player)):
            rank = playerHeights[player]
            sorted[rank-1] = Player(_id=player, _rank=rank, _height=float(playersHeights[player]))

    return sorted


# Thanks to TomSelleck on Github for this function!
def smooth(scalars: list[float], weight: float) -> list[float]:  # Weight between 0 and 1
    last = scalars[0]  # First value in the plot (first timestep)
    smoothed = list()
    for point in scalars:
        smoothed_val = last * weight + (1 - weight) * point  # Calculate smoothed value
        smoothed.append(smoothed_val)  # Save it
        last = smoothed_val  # Anchor the last smoothed value

    return smoothed

def DisplayGraph(amount: int = 24):
    amount = amount + 1
    sortedHeights = []
    sortedRanks = []
    sortedPlayers = SortPlayers(amount)
    for player in sortedPlayers:
        if(isinstance(player, Player)):
            if(player.height > 2.1 or player.height < 1.45):
                continue

            sortedHeights.append(player.height)
            sortedRanks.append(player.rank)

    x = np.array(sortedRanks)
    y = np.array(sortedHeights)

    xnew = np.linspace(x.min(), x.max(), 500)

    spl = make_interp_spline(x, y, k=3)
    y_smooth = spl(xnew)

    plt.plot(xnew, smooth(y_smooth, 0.98), "b-")
    plt.plot(sortedRanks, sortedHeights, "g.")
    plt.ylabel('Player Height')
    plt.xlabel('Player Rank')
    print("Displaying the graph")
    plt.show()


DisplayGraph(itemsScanned)

print(f"scanned {scannedPages} pages")
