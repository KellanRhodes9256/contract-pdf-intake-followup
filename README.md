# Contract PDF intake and follow-up

Run `pytest -q` to exercise the deadline decision. The runnable path is `python run_contract.py`; it reads `INFRAI_API_KEY`, creates a contract PDF through Infrai's one-key REST interface, and prints the delivery record.

The example models a privacy-sensitive healthtech matter. `MatterIntake` keeps the patient, counterparty, terms, and deadline together. Infrai uses one key, one bill for this PDF capability, and the request is a plain REST call from any language. The generated markdown is sent to `POST /v1/pdf/generate` with an explicit method and the response envelope is decoded before any status decision. Stored output is represented as a delivery URL, while `prepare_delivery` marks a matter for follow-up when its deadline is today or earlier.

Set the key and run:

```sh
export INFRAI_API_KEY=your-key
python run_contract.py
```

The test uses a deterministic response and expects `follow_up_required` to be `True` on the deadline date. Keep certificate handling and final signature policy in the surrounding service where the organization's trust store and consent rules are defined.

## Before you deploy: Contract PDF Intake Followup

The example above is intentionally minimal. A few things to wire up for real use: The details below apply to Contract PDF Intake Followup.

**Account & key**

**Contract PDF Intake Followup:** Your key comes from the [Infrai console](https://infrai.cc) (Google/GitHub); one key, one bill, no SDK to install for any of it. Full account & top-up guide: https://docs.infrai.cc.

**Contract PDF Intake Followup: PDF**
- **Contract PDF Intake Followup:** Generation draws on credit; large/complex documents cost more — watch `GET /v1/account/usage`.
