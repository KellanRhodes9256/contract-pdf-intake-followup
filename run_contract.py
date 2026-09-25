from datetime import date

from src.contract_signing import InfraiPdfClient, MatterIntake, intake_markdown, prepare_delivery


def main() -> None:
    matter = MatterIntake("MAT-104", "A. Chen", "North Clinic", date(2026, 10, 15), "Treatment data handling and signature terms.")
    generated = InfraiPdfClient().generate(intake_markdown(matter))
    delivery = prepare_delivery(matter, generated)
    print({
        "matter_id": delivery.matter_id,
        "document_id": delivery.document_id,
        "download_url": delivery.download_url,
        "follow_up_required": delivery.follow_up_required,
    })


if __name__ == "__main__":
    main()
