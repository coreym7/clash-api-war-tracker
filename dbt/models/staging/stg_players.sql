-- stg_players.sql
-- Staging model to clean and rename fields from the raw players table

select
  tag as player_tag,
  name,
  active,
  first_seen,
  last_seen
from main.players
where active = 1
