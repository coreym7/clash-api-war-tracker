-- models/staging/stg_wars.sql
with source as (
    select * from main.wars
),

renamed as (
    select
        id,
        start_time,
        end_time,
        clan_name,
        clan_tag,
        result
    from source
)

select * from renamed
