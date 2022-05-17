CREATE TABLE club_league_games(
    game_timestamp TEXT PRIMARY KEY,
    season TEXT,
    event_day TEXT,
    mode TEXT,
    map TEXT,
    result TEXT,
    trophy_change INT,
    
    player1_tag TEXT,
    player1_name TEXT,
    player1_brawler TEXT,
    player1_is_club_member BOOLEAN,

    player2_tag TEXT,
    player2_name TEXT,
    player2_brawler TEXT,
    player2_is_club_member BOOLEAN,

    player3_tag TEXT,
    player3_name TEXT,
    player3_brawler TEXT,
    player3_is_club_member BOOLEAN,

    player4_tag TEXT,
    player4_name TEXT,
    player4_brawler TEXT,
    player4_is_club_member BOOLEAN,

    player5_tag TEXT,
    player5_name TEXT,
    player5_brawler TEXT,
    player5_is_club_member BOOLEAN,

    player6_tag TEXT,
    player6_name TEXT,
    player6_brawler TEXT,
    player6_is_club_member BOOLEAN
);
