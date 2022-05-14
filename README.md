# Motivation

Wouldn't it be cool to track your club's Club League performance? Many interesting metrics come to mind, such as:

- Played tickets per player per season
- Win rate per player and/or per map
- Brawler pick rates
- and many, many more...

One possible way to keep track of all this information is with pen and paper, but this would get way too tedious. A more efficient approach would be to maintain an Excel spreadsheet, but again, this can get very tedious over time. There must be a way to track all this information with minimal effort. This is where the Brawl Stars API comes into play.

# Brawl Stars API

When searching on Google for a Brawl Stars API, there are two main results:

- An unofficial Brawl Stars API called BrawlAPI (https://brawlapi.com/)
- The official Brawl Stars API (https://developer.brawlstars.com/)

The BrawlAPI does not seem to provide any information related to Club League. Neither does the official Brawl Stars API, or does it?

With the official Brawl Stars API one can retrieve the battlelog of any player. The Club League matches also appear in the battlelog, right? Does this mean that one can retrieve the battlelog and then extract the Club League games? The answer is yes, but it is not that straightforward.

# Brawl Stars API Battlelog Endpoint

Let's understand what the Brawl Stars API battlelog endpoint (`/players/{playerTag}/battlelog`) returns with the sample JSON in the expand tab below.

<details>
  <summary>Sample JSON</summary>

```
{
  "items": [
    {
      "battleTime": "20220512T060224.000Z",
      "event": {
        "id": 15000023,
        "mode": "heist",
        "map": "G.G. Mortuary"
      },
      "battle": {
        "mode": "heist",
        "type": "ranked",
        "result": "defeat",
        "duration": 81,
        "trophyChange": -4,
        "starPlayer": {
          "tag": "#VLGJ0PYJ",
          "name": "amir_krall T R",
          "brawler": {
            "id": 16000002,
            "name": "BULL",
            "power": 9,
            "trophies": 526
          }
        },
        "teams": [
          [
            {
              "tag": "#2CV9G8CY9",
              "name": "puuki",
              "brawler": {
                "id": 16000009,
                "name": "DYNAMIKE",
                "power": 9,
                "trophies": 512
              }
            },
            {
              "tag": "#J0RR88U9",
              "name": "gedenli52",
              "brawler": {
                "id": 16000007,
                "name": "JESSIE",
                "power": 8,
                "trophies": 502
              }
            },
            {
              "tag": "#VLGJ0PYJ",
              "name": "amir_krall T R",
              "brawler": {
                "id": 16000002,
                "name": "BULL",
                "power": 9,
                "trophies": 526
              }
            }
          ],
          [
            {
              "tag": "#9PV0PG9GP",
              "name": "PropagandaPanda",
              "brawler": {
                "id": 16000048,
                "name": "GROM",
                "power": 6,
                "trophies": 374
              }
            },
            {
              "tag": "#PYGUJPUQG",
              "name": "SReading",
              "brawler": {
                "id": 16000013,
                "name": "POCO",
                "power": 9,
                "trophies": 583
              }
            },
            {
              "tag": "#8V9VQQLLQ",
              "name": "AngelOfDeath",
              "brawler": {
                "id": 16000038,
                "name": "SURGE",
                "power": 9,
                "trophies": 481
              }
            }
          ]
        ]
      }
    },
    {
      "battleTime": "20220512T055828.000Z",
      "event": {
        "id": 15000530,
        "mode": "heist",
        "map": "Can't touch this"
      },
      "battle": {
        "mode": "heist",
        "type": "teamRanked",
        "result": "defeat",
        "duration": 79,
        "trophyChange": 5,
        "starPlayer": {
          "tag": "#8RCYGRGYY",
          "name": "Матвей про",
          "brawler": {
            "id": 16000006,
            "name": "BARLEY",
            "power": 9,
            "trophies": 14
          }
        },
        "teams": [
          [
            {
              "tag": "#8RCYGRGYY",
              "name": "Матвей про",
              "brawler": {
                "id": 16000006,
                "name": "BARLEY",
                "power": 9,
                "trophies": 14
              }
            },
            {
              "tag": "#YPVYLQR8U",
              "name": "босс бебрус",
              "brawler": {
                "id": 16000056,
                "name": "EVE",
                "power": 10,
                "trophies": 14
              }
            },
            {
              "tag": "#98J8VP8JU",
              "name": "Настя",
              "brawler": {
                "id": 16000030,
                "name": "EMZ",
                "power": 9,
                "trophies": 14
              }
            }
          ],
          [
            {
              "tag": "#LCYVPU020",
              "name": "bot 1",
              "brawler": {
                "id": 16000043,
                "name": "EDGAR",
                "power": 11,
                "trophies": 14
              }
            },
            {
              "tag": "#9PV0PG9GP",
              "name": "PropagandaPanda",
              "brawler": {
                "id": 16000003,
                "name": "BROCK",
                "power": 9,
                "trophies": 14
              }
            },
            {
              "tag": "#PYGUJPUQG",
              "name": "SReading",
              "brawler": {
                "id": 16000057,
                "name": "JANET",
                "power": 6,
                "trophies": 14
              }
            }
          ]
        ]
      }
    },
    {
      "battleTime": "20220512T055654.000Z",
      "event": {
        "id": 15000530,
        "mode": "heist",
        "map": "Can't touch this"
      },
      "battle": {
        "mode": "heist",
        "type": "teamRanked",
        "result": "defeat",
        "duration": 84,
        "starPlayer": null,
        "teams": [
          [
            {
              "tag": "#8RCYGRGYY",
              "name": "Матвей про",
              "brawler": {
                "id": 16000006,
                "name": "BARLEY",
                "power": 9,
                "trophies": 14
              }
            },
            {
              "tag": "#YPVYLQR8U",
              "name": "босс бебрус",
              "brawler": {
                "id": 16000056,
                "name": "EVE",
                "power": 10,
                "trophies": 14
              }
            },
            {
              "tag": "#98J8VP8JU",
              "name": "Настя",
              "brawler": {
                "id": 16000030,
                "name": "EMZ",
                "power": 9,
                "trophies": 14
              }
            }
          ],
          [
            {
              "tag": "#LCYVPU020",
              "name": "bot 1",
              "brawler": {
                "id": 16000043,
                "name": "EDGAR",
                "power": 11,
                "trophies": 14
              }
            },
            {
              "tag": "#9PV0PG9GP",
              "name": "PropagandaPanda",
              "brawler": {
                "id": 16000003,
                "name": "BROCK",
                "power": 9,
                "trophies": 14
              }
            },
            {
              "tag": "#PYGUJPUQG",
              "name": "SReading",
              "brawler": {
                "id": 16000057,
                "name": "JANET",
                "power": 6,
                "trophies": 14
              }
            }
          ]
        ]
      }
    }
  ],
  "paging": {
    "cursors": {}
  }
}
```

</details>

The sample JSON contains three entries where each one corresponds to a game. A short summary:

- **Game 1:** Regular Heist game on 'G.G. Mortuary', defeat, lost 4 trophies
- **Game 2:** Club League Power Match round 2 on 'Can't touch this', defeat, gained 5 Club League trophies
- **Game 3:** Club League Power Match round 1 on 'Can't touch this', defeat

This indicates that games which last over multiple rounds such as Club League Power Matches and Power League games have separate entries for each round. But how exactly can Club League games be identified? Upon further investigation of multiple battlelog JSONs, there are some attributes which can be used for identification:

- Club League games which are Power Matches have `"type": "teamRanked"` (independent of if played solo or with club members)
- Power League games which are played in a team have `"type": "teamRanked"`
- Power League games which are played solo have `"type": "soloRanked"`
- Regular games which are neither Club League Power Matches nor Power League games have `"type": "Ranked"`

*Note: It was not investigated what the `"type"` for Club League games which are no Power Matches is, as our club only plays Power Matches.*

The observations above make it clear that Club League Power Matches can be identified with `"type": "teamRanked"`. However, Power League games which are played in a team also have `"type": "teamRanked"`. How can they be distinguished from each other? Further investigation suggests:

- Power League games do not have the key `"trophyChange"` but Club League Power Matches do. Further, the values for the key `"trophyChange"` for Club League Power Matches are either 3, 5, 7 or 9, depending on if played solo or in a team and if won or lost.

This results in a unique identifier for Club League Power Matches in the battlelog! Written in pseudocode it is like this:

`if "type" == "teamRanked" and "trophyChange" in [3, 5, 7, 9] then it is a Club League Power Match`

However, this is not the full story yet. When looking at the sample JSON above, one recognizes that Game 3, which is the first round of a Club League Power Match, does not have the key `"trophyChange"`. Only the second round which is Game 2 does. This makes sense, as the final round determines how much trophies are lost or gained depending on the outcome of the previous rounds. A Club League Power Match could also last three rounds, then there would be three entries and the key `"trophyChange"` would be only on the third one.

For the sake of simplicity with regards to the technical implementation, only the final round of a Club League Power Match is considered. This means, the one with the key `"trophyChange"`. The rounds prior to the final round are not considered and generally also not as important.

Therefore, one can stick with the identifier `if "type" == "teamRanked" and "trophyChange" in [3, 5, 7, 9] then it is a Club League Power Match`.

If one wanted to also track the non-final rounds, one would have to work with a different identifier than ` "trophyChange" in [3, 5, 7, 9]`. One possibility would be to look for entries with the same players as in the final round, as of course all rounds of a Club League Power Match are played by the same players. However, as stated above, only the final round of a Club League Power Match which has the key `"trophyChange"` is considered in this implementation.

# Technical Implementation

The script `get_club_members.py` retrieves the club members via the club members endpoint (`/clubs/{clubTag}/members`) and stores them in the database table `club_members`. Then, the script `get_club_league_games.py` iterates through all members in the table `club_members` and retrieves their Club League Power Matches via the battlelog endpoint (`/players/{playerTag}/battlelog`) and stores them in the database table `club_league_games`. As multiple club members can have the same Club League Power Matches in their battlelog, there is a duplication filter based on the Club League Power Match timestamp, so that only each unique Club League Power Match is stored in the table `club_league_games`.

The table `club_members` looks as follows:
| player_tag    | player_name   |
| ------------- | ------------- |
| '#9GQ2R82CC'  | 'Konni83'     |
| '#PQ82UU20R'  | 'Masha'       |
| '#9CCQRLY02'  | 'aegiman'     |
| ...           | ...           |

The table `club_league_games` looks as follows:
| game_timestamp         | game_json                                                                                                         |
| ---------------------- | ----------------------------------------------------------------------------------------------------------------- |
| '20220508T202244.000Z' | '{"battleTime": "20220508T202244.000Z", "event": {"id": 15000306, "mode": "hotZone", "map": "Dueling Beetles"}... |
| '20220508T202845.000Z' | '{"battleTime": "20220508T202845.000Z", "event": {"id": 15000306, "mode": "hotZone", "map": "Dueling Beetles"}... |
| '20220508T203533.000Z' | '{"battleTime": "20220508T203533.000Z", "event": {"id": 15000026, "mode": "brawlBall", "map": "Pinhole Punt"}...  |
| ...                    | ...                                                                                                               |

There is an argument whether one should store the raw JSON of a Club League Power Match in the table or pre-process it in a way which makes the data more human-readable. It was decided to store the raw JSON in the table and leave any processing to the consuming application.

An important point one has to be aware of is that the battlelog changes over time. Therefore, the script `get_club_league_games.py` has to run regularly to catch all Club League Power Matches. An example schedule could look as follows:

1. Run the script `get_club_members.py` shortly before a Club League season starts to get the latest club member list.
2. Run the script `get_club_league_games.py` multiple times during the Club League season to catch all Club League Power Matches. The duplication filter prevents that the same Club League Power Match gets stored multiple times.

As a free cloud-hosted database I can recommend the PostgreSQL Hobby Dev plan on Heroku (https://elements.heroku.com/addons/heroku-postgresql). With up to 10'000 rows and 1 GB of storage you can store plenty of Club League Power Matches data. Also, as it is cloud-hosted, the data can be accessed from anywhere.

The next step is to automate the execution of the scripts on Heroku so that the data collecting runs 24/7 without manual intervention. Further, a consuming application will be built to visualize the collected data and draw insights from it.
