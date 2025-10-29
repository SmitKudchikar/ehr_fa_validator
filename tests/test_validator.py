from app.models.ehr_event import EHREvent
from datetime import datetime

def validate_sequence(events, dfa):
    events_sorted = sorted(events, key=lambda e: e.timestamp)
    state, anomalies = dfa.run(events_sorted)

    # Example domain-specific checks
    for e in events_sorted:
        if e.abha_id and not validate_abha(e.abha_id):
            anomalies.append(f"Invalid ABHA format for {e.patient_id}")

    return {"final_state": state, "is_valid": state in dfa.accepting_states, "anomalies": anomalies}

def validate_abha(abha_id):
    import re
    return bool(re.match(r"^\d{2}-\d{4}-\d{4}-\d{4}$", abha_id))
