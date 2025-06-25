from typing import Dict


class HealthService:
    """Tiny service that encapsulates our *business* logic.

    Right now it does almost nothing, but placing logic in a service layer keeps
    views thin and makes unit‑testing easier.
    """

    def ping(self) -> Dict[str, str]:
        return {
            "message": "pong",
        }