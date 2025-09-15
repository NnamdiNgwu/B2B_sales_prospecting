# from pathlib import Path
# import json
# from typing import Dict, Any, Optional

# DATA_ROOT = Path("data_folder") / "settings"
# ORG_PATH = DATA_ROOT / "org.json"

# class SettingsService:
#     def __init__(self) -> None:
#         DATA_ROOT.mkdir(parents=True, exist_ok=True)
#         if not ORG_PATH.exists():
#             ORG_PATH.write_text(json.dumps({}, indent=2), encoding="utf-8")

#     def get_org(self) -> Dict[str, Any]:
#         try:
#             return json.loads(ORG_PATH.read_text(encoding="utf-8"))
#         except Exception:
#             return {}

#     def save_org(self, payload: Dict[str, Any]) -> Dict[str, Any]:
#         ORG_PATH.write_text(json.dumps(payload, indent=2), encoding="utf-8")
#         return payload

# def get_settings_service() -> SettingsService:
#     return SettingsService()