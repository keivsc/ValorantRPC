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
# Note: Configuration will now be automatic
{
    "version": "v2.3",
    "configVers":"v1.3",
    "region":"",
    "regions":["na", "eu", "latam", "br", "ap", "kr", "pbe"],
    "clientID": 876945941628858398,
    "language":"",
    "languages":["en-US","ja-JP","ko-KR"],
    "presenceRefreshRate": 3,
    "presence":{
        "show_rank": true
    },
    "startup":{
        "launch_timeout":60
    }

}
```

# Custom Client
### You can learn to connect to your own client [here](https://github.com/keivsc/ValorantRPC/wiki/Custom-Application)