# models_intake (front door)

This folder mirrors the model/tool wrapper names with an `_intake` suffix so routing can target a predictable path:

- Wrapper lives in: `X:\knowledge-refinery\BACKSIDE\MODELS\models\<wrapper_name>\`
- Intake mirror lives in: `X:\knowledge-refinery\01_INTAKE\models_intake\<wrapper_name>_intake\`

Rule:
- Intake mirrors are for **inputs/requests** headed to a given model/tool wrapper.
- Outputs land in that mirror's `OUTPUT/` (or get forwarded into the appropriate station packet).

Intake mirrors created for all wrappers currently present under:
- `X:\knowledge-refinery\BACKSIDE\MODELS\models\`

