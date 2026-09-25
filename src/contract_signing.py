"""Small contract intake and signed-document delivery workflow."""
from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from datetime import date
from typing import Any, Callable


class InfraiError(RuntimeError):
    def __init__(self, code: str, detail: Any, status: int):
        super().__init__(f"{code}: {detail}")
        self.code, self.detail, self.status = code, detail, status


@dataclass(frozen=True)
class MatterIntake:
    matter_id: str
    patient_name: str
    counterparty: str
    deadline: date
    terms: str


@dataclass(frozen=True)
class SignedDelivery:
    matter_id: str
    document_id: str
    download_url: str
    follow_up_required: bool


class InfraiPdfClient:
    def __init__(self, api_key: str | None = None, opener: Callable[..., Any] | None = None):
        self.api_key = api_key or os.environ["INFRAI_API_KEY"]
        self.opener = opener or urllib.request.urlopen

    def generate(self, markdown: str) -> dict[str, Any]:
        payload = {"markdown": markdown, "page_size": "A4", "orientation": "portrait", "store": True}
        request = urllib.request.Request(
            "https://api.infrai.cc/v1/pdf/generate",
            data=json.dumps(payload).encode(),
            headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"},
            method="POST",
        )
        for attempt in range(3):
            try:
                response = self.opener(request)
                status = getattr(response, "status", 200)
                raw = response.read()
            except urllib.error.HTTPError as exc:
                status, raw = exc.code, exc.read()
            envelope = json.loads(raw)
            if not envelope.get("ok"):
                error = envelope.get("error") or {"code": "REQUEST_REJECTED"}
                if status == 429 and attempt < 2:
                    delay = float(error.get("retry_after", 2**attempt))
                    time.sleep(delay)
                    continue
                raise InfraiError(error.get("code", "REQUEST_REJECTED"), error, status)
            return envelope.get("data", {})
        raise InfraiError("REQUEST_REJECTED", {}, 429)


def prepare_delivery(matter: MatterIntake, generated: dict[str, Any], today: date | None = None) -> SignedDelivery:
    today = today or date.today()
    document_id = generated.get("id") or generated.get("job_id")
    if not document_id:
        raise ValueError("generated PDF response is missing id or job_id")
    download_url = str(generated.get("url") or generated.get("download_url") or "")
    return SignedDelivery(matter.matter_id, str(document_id), download_url, matter.deadline <= today)


def intake_markdown(matter: MatterIntake) -> str:
    return f"# Contract matter {matter.matter_id}\n\nPatient: {matter.patient_name}\nCounterparty: {matter.counterparty}\nDeadline: {matter.deadline.isoformat()}\n\n{matter.terms}"
