CREATE TABLE OR REPLACE TABLE JUGADORES_FUTBOL_DB.SILVER.FCT_PLAYER_SEASON AS
(
WITH player_base AS (
    SELECT
        player_id,
        last_season AS season,
        current_club_id,
        current_club_domestic_competition_id
    FROM RAW.PLAYERS
),
valuations_season AS (
    SELECT
        player_id,
        YEAR(date) AS season,
        AVG(market_value_in_eur) AS average_market_value
    FROM RAW.PLAYER_VALUATIONS
    GROUP BY player_id, YEAR(date)
),
appearances_season AS (
    SELECT
        player_id,
        YEAR(date) AS season,
        player_current_club_id,
        competition_id,
        SUM(yellow_cards) AS yellow_cards,
        SUM(red_cards) AS red_cards,
        SUM(goals) AS goals,
        SUM(assists) AS assists,
        AVG(minutes_played) AS average_time
    FROM RAW.APPEARANCES
    GROUP BY
        player_id,
        YEAR(date),
        player_current_club_id,
        competition_id
),
player_season_keys AS (
    SELECT player_id, season FROM player_base
    UNION
    SELECT player_id, season FROM valuations_season
    UNION
    SELECT player_id, season FROM appearances_season
)
SELECT
    CAST(k.player_id AS NUMBER) AS player_id,
    CAST(k.season AS NUMBER) AS season,
    CAST(COALESCE(aps.player_current_club_id, pb.current_club_id) AS NUMBER) AS club_id,
    CAST(COALESCE(aps.competition_id, pb.current_club_domestic_competition_id) AS STRING) AS competition_id,
    CAST(COALESCE(aps.yellow_cards, 0) AS NUMBER) AS yellow_cards,
    CAST(COALESCE(aps.red_cards,    0) AS NUMBER) AS red_cards,
    CAST(COALESCE(aps.goals,        0) AS NUMBER) AS goals,
    CAST(COALESCE(aps.assists,      0) AS NUMBER) AS assists,
    CAST(COALESCE(aps.average_time, 0) AS NUMBER) AS average_time,
    CAST(COALESCE(vs.average_market_value, 0) AS NUMBER) AS average_market_value
FROM player_season_keys k
LEFT JOIN appearances_season aps
    ON k.player_id = aps.player_id
   AND k.season = aps.season
LEFT JOIN valuations_season vs
    ON k.player_id = vs.player_id
   AND k.season = vs.season
LEFT JOIN player_base pb
    ON k.player_id = pb.player_id
);

CREATE OR REPLACE SILVER.DIM_PLAYER AS
(
    SELECT

        CAST()
    FROM RAW.PLAYERS
);

CREATE OR REPLACE TABLE JUGADORES_FUTBOL_DB.SILVER.DIM_PLAYER AS
SELECT
    player_id,
    first_name,
    last_name,
    name,
    last_season,
    current_club_id,
    player_code,
    country_of_birth,
    city_of_birth,
    country_of_citizenship,
    date_of_birth::DATE AS date_of_birth,
    sub_position,
    position,
    foot,
    height_in_cm,
    contract_expiration_date,
    agent_name,
    image_url,
    international_goals,
    international_caps,
    current_national_team_id,
    url,
    current_club_domestic_competition_id,
    current_club_name,
    market_value_in_eur,
    highest_market_value_in_eur
FROM JUGADORES_FUTBOL_DB.RAW.PLAYERS;

CREATE OR REPLACE TABLE JUGADORES_FUTBOL_DB.SILVER.DIM_CLUB AS
SELECT *
FROM JUGADORES_FUTBOL_DB.RAW.CLUBS;

CREATE OR REPLACE TABLE JUGADORES_FUTBOL_DB.SILVER.DIM_COMPETITION AS
SELECT *
FROM JUGADORES_FUTBOL_DB.RAW.COMPETITIONS;

