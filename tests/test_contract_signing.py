import json
from datetime import date

import pytest

from src.contract_signing import InfraiPdfClient, MatterIntake, prepare_delivery


class FakeResponse:
    status = 200
    def read(self):
        return json.dumps({"ok": True, "data": {"id": "pdf-7", "url": "https://files.example/pdf-7"}, "error": None, "metadata": {}}).encode()


def test_deadline_requires_follow_up_and_preserves_delivery():
    matter = MatterIntake("M-1", "P", "Clinic", date(2026, 9, 5), "terms")
    generated = InfraiPdfClient("test-key", lambda request: FakeResponse()).generate("terms")
    delivery = prepare_delivery(matter, generated, today=date(2026, 9, 5))
    assert delivery.document_id == "pdf-7"
    assert delivery.download_url.endswith("pdf-7")
    assert delivery.follow_up_required is True


def test_prepare_delivery_rejects_response_without_document_id():
    matter = MatterIntake("M-1", "P", "Clinic", date(2026, 9, 5), "terms")

    with pytest.raises(ValueError, match="missing id or job_id"):
        prepare_delivery(matter, {"url": "https://files.example/pdf"})
