-- models/staging/stg_participation.sql
with source as (
    select * from main.participation
),

renamed as (
    select
        id,
        player_tag,
        war_id,
        in_war,
        new_stars
    from source
)

select * from renamed
