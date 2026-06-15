# Scripts And Runbooks

Included scripts:

- `generate_reading_levels.py`
- `run_all_reading_levels.ps1`
- `combine_mda_reader_html.py`

Recommended order:

1. Run `run_all_reading_levels.ps1`.
2. Run `combine_mda_reader_html.py`.
3. Spot-check `03_READER_HTML/index.html`.
4. Only then move updated HTML toward deploy.

Do not call Proof complete just because the Proof tab renders.
