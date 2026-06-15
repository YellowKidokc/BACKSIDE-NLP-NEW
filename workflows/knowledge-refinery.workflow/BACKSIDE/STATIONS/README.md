# STATIONS

Station tier of the Backside topology. Stations are pipeline steps — they bind models to prompts, scripts, and IO contracts with gates.

**If you are an LLM working in here, read `READ_FIRST.md` before doing anything.**

```
STATIONS/
  READ_FIRST.md              <-- start here
  STATION_INVENTORY.md       <-- what exists, in prose
  stations_registry.yml      <-- source of truth (yaml)
  new_station.py             <-- the duplicator
  new_station.bat            <-- thin wrapper
  stations/
    _TEMPLATE/               <-- canonical template, do not edit for one-offs
    01_sci_embed/  ...       <-- one folder per station
```

Mental model:

```
WORKFLOW -> STATION -> MODEL -> PROMPT -> SCRIPT -> OUTPUT -> GATE -> NEXT STATION
```

To create a station: `new_station.bat NUMBER name --lane LANE --model M-XXX --status draft`.
