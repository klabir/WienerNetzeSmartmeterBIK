# Bruno collection for Wiener Netze Smartmeter API

Import the `bruno/` folder into Bruno. The requests use variables you can define in a Bruno environment:

## Required variables

- `access_token`
- `b2c_api_url`
- `b2b_api_url`
- `alt_api_url`
- `b2c_api_key`
- `b2b_api_key`
- `customer_id`
- `zaehlpunktnummer`

## Optional variables (per request)

- `date_from` (ISO timestamp, e.g. `2024-02-06T00:00:00.000Z`)
- `date_to` (ISO timestamp, e.g. `2024-02-07T00:00:00.000Z`)
- `day_view_resolution` (`HOUR` or `QUARTER-HOUR`)
- `date_from_day` (date only, e.g. `2024-02-01`)
- `date_to_day` (date only, e.g. `2024-02-07`)
- `wertetyp` (`METER_READ`, `DAY`, `QUARTER_HOUR`)
- `date_until` (ISO timestamp, e.g. `2024-02-07T00:00:00.000Z`)
- `start_at` / `end_at` (ISO timestamp for events)
- `event_name`
- `event_type` (`ZEITPUNKT` or `ZEITSPANNE`)
- `ereignis_id`
- `rolle` (`V001`, `V002`, `E001`, `E002`)
- `zeitpunkt_von` / `zeitpunkt_bis`
