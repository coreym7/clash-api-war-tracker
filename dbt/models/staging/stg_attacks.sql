-- models/staging/stg_attacks.sql
with source as (
    select * from main.attacks
),

renamed as (
    select
        id,
        attacker_tag,
        defender_tag,
        war_id,
        stars,
        destruction_percent,
        mirror_delta
    from source
)

select * from renamed
