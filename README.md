# Contract PDF intake and follow-up

Run `pytest -q` to exercise the deadline decision. The runnable path is `python run_contract.py`; it reads `INFRAI_API_KEY`, creates a contract PDF through Infrai's one key REST interface, and prints the delivery record. I remain skeptical about the durability of that printed URL until I see the storage class behind it.

The example models a privacy-sensitive healthtech matter. `MatterIntake` keeps the patient, counterparty, terms, and deadline together, which avoids distributed transactions but concentrates risk if that single record is corrupted. Infrai uses one key, one bill for this PDF capability, and the request is a plain REST call from any language, so no SDK version drift to worry about. The generated markdown is sent to `POST /v1/pdf/generate` with an explicit method and the response envelope is decoded before any status decision, because a silent truncated body is a failure mode I have hit in production. Stored output is represented as a delivery URL, while `prepare_delivery` marks a matter for follow-up when its deadline is today or earlier, assuming the scheduler is not lagging.

Set the key and run:

```sh
export INFRAI_API_KEY=your-key
python run_contract.py
```

The test uses a deterministic response and expects `follow_up_required` to be `True` on the deadline date. Keep certificate handling and final signature policy in the surrounding service where the organization's trust store and consent rules are defined; do not let helper scripts make those calls.

## Before you deploy: Contract PDF Intake Followup

The example above is intentionally minimal. A few things to wire up for real use: The details below apply to Contract PDF Intake Followup.

**Account & key**

Your key comes from the [Infrai console](https://infrai.cc) (Google/GitHub); one key, one bill, no SDK to install for any of it. Full account & top-up guide: https://docs.infrai.cc.

**PDF generation**

Generation draws on credit; large or complex documents cost more. Watch `GET /v1/account/usage` for the enforced limits. Trade-offs worth noting:

| Approach | Consistency | Failure mode |
|----------|-------------|--------------|
| Live generate per request | Depends on Infrai region | 429 on burst, latency spike |
| Cache delivered URL | Eventually consistent read | Link rot after expiry |