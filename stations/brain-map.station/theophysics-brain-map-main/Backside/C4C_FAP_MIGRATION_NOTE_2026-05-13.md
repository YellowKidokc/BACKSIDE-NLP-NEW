# C4C / FAP Migration Note

Date: 2026-05-13

## New X-drive homes

- `X:\brain\C4C-wiki` copied from `D:\C4C-wiki`
- `X:\brain\C4C` copied from the real vault at `O:\_ Theophysics_Case_for_Christ`
- `X:\brain\FAP` copied from `D:\FAP`

## Important source-path note

`D:\C4C` is not a real folder. It is a malformed junction:

`D:\C4C -> C:\O:\_ Theophysics_Case_for_Christ\`

Because that target path is invalid, the migration used the real existing vault:

`O:\_ Theophysics_Case_for_Christ`

## Verification

- `C4C-wiki`: 862 files, 15 directories, 37.583 MB copied.
- `FAP`: 63 files, 59 directories, 0.249 MB copied.
- `C4C`: 2,496 real content files, 161 directories, 678.497 MB copied.

The C4C source also contains Synology `@eaDir` metadata folders. Those were not treated as required content. Excluding `@eaDir` and `.stfolder`, the C4C copy has zero missing files.

## Copy logs

Logs are in:

`C:\Users\lowes\Documents\Codex\2026-05-13\do-they-have-like-a-nlp`

- `robocopy_C4C-wiki_to_Xbrain.log`
- `robocopy_C4C_realvault_to_Xbrain.log`
- `robocopy_FAP_to_Xbrain.log`
- `robocopy_C4C_to_Xbrain.log` records the failed attempt against the malformed `D:\C4C` junction.
