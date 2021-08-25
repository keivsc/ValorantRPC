# ValorantRPC

#### Discord Rich Presence Client for VALORANT

# Installation
- Download the latest [release](https://github.com/keivsc/ValorantRPC/releases/) and run it

[![Discord](https://img.shields.io/badge/discord-join-7389D8?style=flat&logo=discord)](https://discord.gg/dFZzaaHYGG)

# Features
- Show current match and livestats
- In queue status
- Current playing agent & map
- Display Rank (toggleable)

# Examples
- Profile <br/>
![alt text](https://cdn.discordapp.com/attachments/701967775580815380/877752234685902968/unknown.png)

- In Lobby <br/>
![alt text](https://cdn.discordapp.com/attachments/701967775580815380/877753154811346984/unknown.png)

- In Queue <br/>
![alt text](https://cdn.discordapp.com/attachments/701967775580815380/877753370704744458/unknown.png)

- In Game <br/>
![alt text](https://cdn.discordapp.com/attachments/701967775580815380/877766232512802816/unknown.png)

# Configuration

```json
# Note: dont copy everything here as listed such as comments (json aren't allowed to have comments)

{
    "version": "v2.0",
    "configVers":"v1.2",
    "regions":["", "na", "eu", "latam", "br", "ap", "kr", "pbe"], # change the first item in the list to your prefered region (this is done automatically)
    "clientID": 876945941628858398, 
    "language":"", # change this to your prefered language (listed below)
    "languages":["ar-AE","de-DE","en-US","es-ES","es-MX","fr-FR","id-ID","it-IT","ja-JP","ko-KR","pl-PL","pt-BR","ru-RU","th-TH","tr-TR","vi-VN","zh-CN","zh-TW"],
    "presenceRefreshRate": 3,
    "presence":{
        "show_rank": True, # display your rank in the status
    },
    "startup":{
        "launch_timeout":60, # time before rpc close if VALORANT is not detected
    }

}
```

# Custom Client
### You can learn to connect to your own client [here](https://github.com/keivsc/ValorantRPC/wiki/Custom-Application)
