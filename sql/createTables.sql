
CREATE TABLE IF NOT EXISTS JUGADORES_FUTBOL_DB.RAW.PLAYERS (
    player_id                               NUMBER PRIMARY KEY,
    first_name                              STRING,
    last_name                               STRING,
    name                                    STRING,
    last_season                             NUMBER,
    current_club_id                         NUMBER,
    player_code                             STRING,
    country_of_birth                        STRING,
    city_of_birth                           STRING,
    country_of_citizenship                  STRING,
    date_of_birth                           TIMESTAMP_NTZ,
    sub_position                            STRING,
    position                                STRING,
    foot                                    STRING,
    height_in_cm                            NUMBER,
    contract_expiration_date                DATE,
    agent_name                              STRING,
    image_url                               STRING,
    international_goals                     NUMBER,
    international_caps                      NUMBER,
    current_national_team_id                NUMBER,
    url                                     STRING,
    current_club_domestic_competition_id    STRING,
    current_club_name                       STRING,
    market_value_in_eur                     NUMBER,
    highest_market_value_in_eur             NUMBER
);

CREATE TABLE IF NOT EXISTS JUGADORES_FUTBOL_DB.RAW.CLUBS (
    club_id                                 NUMBER PRIMARY KEY,
    club_code                               STRING,
    name                                    STRING,
    domestic_competition_id                 STRING,
    total_market_value                      NUMBER,
    squad_size                              NUMBER,
    average_age                             NUMBER,
    foreigners_number                       NUMBER,
    foreigners_percentage                   NUMBER(4,1),
    national_team_players                   NUMBER,
    stadium_name                            STRING,
    stadium_seats                           NUMBER,
    net_transfer_record                     STRING,
    coach_name                              STRING,
    last_season                             NUMBER,
    filename                                STRING,
    url                                     STRING
);


CREATE TABLE IF NOT EXISTS JUGADORES_FUTBOL_DB.RAW.COMPETITIONS (
    competition_id                          STRING PRIMARY KEY,
    competition_code                        STRING,
    name                                    STRING,
    sub_type                                STRING,
    type                                    STRING,
    country_id                              NUMBER,
    country_name                            STRING,
    domestic_league_code                    STRING,
    confederation                           STRING,
    total_clubs                             NUMBER,
    url                                     STRING
);

CREATE TABLE IF NOT EXISTS JUGADORES_FUTBOL_DB.RAW.PLAYER_VALUATIONS (
    player_id                               NUMBER PRIMARY KEY,
    date                                    DATE PRIMARY KEY,
    market_value_in_eur                     NUMBER,
    current_club_name                       STRING,
    current_club_id                         NUMBER,
    player_club_domestic_competition_id     STRING
);

CREATE TABLE IF NOT EXISTS JUGADORES_FUTBOL_DB.RAW.APPEARANCES (
    appearance_id                           STRING,
    game_id                                 NUMBER,
    player_id                               NUMBER,
    player_club_id                          NUMBER,
    player_current_club_id                  NUMBER,
    date                                    DATE,
    player_name                             STRING,
    competition_id                          STRING,
    yellow_cards                            NUMBER,
    red_cards                               NUMBER,
    goals                                   NUMBER,
    assists                                 NUMBER,
    minutes_played                          NUMBER
);

-- TABLAS TEMPORALES PARA CARGA IDEMPOTENTE

CREATE TABLE IF NOT EXISTS JUGADORES_FUTBOL_DB.RAW.STAGING_PLAYERS (
    player_id                               NUMBER PRIMARY KEY,
    first_name                              STRING,
    last_name                               STRING,
    name                                    STRING,
    last_season                             NUMBER,
    current_club_id                         NUMBER,
    player_code                             STRING,
    country_of_birth                        STRING,
    city_of_birth                           STRING,
    country_of_citizenship                  STRING,
    date_of_birth                           TIMESTAMP_NTZ,
    sub_position                            STRING,
    position                                STRING,
    foot                                    STRING,
    height_in_cm                            NUMBER,
    contract_expiration_date                DATE,
    agent_name                              STRING,
    image_url                               STRING,
    international_goals                     NUMBER,
    international_caps                      NUMBER,
    current_national_team_id                NUMBER,
    url                                     STRING,
    current_club_domestic_competition_id    STRING,
    current_club_name                       STRING,
    market_value_in_eur                     NUMBER,
    highest_market_value_in_eur             NUMBER
);

CREATE TABLE IF NOT EXISTS JUGADORES_FUTBOL_DB.RAW.STAGING_CLUBS (
    club_id                                 NUMBER PRIMARY KEY,
    club_code                               STRING,
    name                                    STRING,
    domestic_competition_id                 STRING,
    total_market_value                      NUMBER,
    squad_size                              NUMBER,
    average_age                             NUMBER,
    foreigners_number                       NUMBER,
    foreigners_percentage                   NUMBER(4,1),
    national_team_players                   NUMBER,
    stadium_name                            STRING,
    stadium_seats                           NUMBER,
    net_transfer_record                     STRING,
    coach_name                              STRING,
    last_season                             NUMBER,
    filename                                STRING,
    url                                     STRING
);


CREATE TABLE IF NOT EXISTS JUGADORES_FUTBOL_DB.RAW.STAGING_COMPETITIONS (
    competition_id                          STRING PRIMARY KEY,
    competition_code                        STRING,
    name                                    STRING,
    sub_type                                STRING,
    type                                    STRING,
    country_id                              NUMBER,
    country_name                            STRING,
    domestic_league_code                    STRING,
    confederation                           STRING,
    total_clubs                             NUMBER,
    url                                     STRING
);

CREATE TABLE IF NOT EXISTS JUGADORES_FUTBOL_DB.RAW.STAGING_PLAYER_VALUATIONS (
    player_id                               NUMBER,
    date                                    DATE,
    market_value_in_eur                     NUMBER,
    current_club_name                       STRING,
    current_club_id                         NUMBER,
    player_club_domestic_competition_id     STRING
);

CREATE TABLE IF NOT EXISTS JUGADORES_FUTBOL_DB.RAW.STAGING_APPEARANCES (
    appearance_id                           STRING,
    game_id                                 NUMBER,
    player_id                               NUMBER,
    player_club_id                          NUMBER,
    player_current_club_id                  NUMBER,
    date                                    DATE,
    player_name                             STRING,
    competition_id                          STRING,
    yellow_cards                            NUMBER,
    red_cards                               NUMBER,
    goals                                   NUMBER,
    assists                                 NUMBER,
    minutes_played                          NUMBER
);

