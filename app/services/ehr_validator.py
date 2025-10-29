import json
from app.automata.dfa_model import DFA
from app.models.ehr_event import EHREvent
import re


def load_dfa(valid=True):
    """
    Load DFA transitions.
    Set valid=False to load intentionally broken transitions (for testing invalid flows).
    """
    path = (
        "app/automata/transitions_valid.json"
        if valid
        else "app/automata/transitions_invalid.json"
    )

    with open(path) as f:
        transitions = json.load(f)

    dfa = DFA("start", ["completed"])
    for src, mapping in transitions.items():
        for symbol, dst in mapping.items():
            dfa.add_transition(src, symbol, dst)
    return dfa


def validate_sequence(events, dfa):
    """
    Validate an EHR event sequence using the DFA.
    Each event must have 'event_type', 'timestamp', and 'patient_id'.
    """
    anomalies = []
    state = dfa.start_state

    # Sort by timestamp
    events_sorted = sorted(events, key=lambda e: e.timestamp)

    for e in events_sorted:
        next_state = dfa.get_next_state(state, e.event_type)
        if next_state is None:
            anomalies.append(f"Invalid transition from '{state}' on event '{e.event_type}'")
            continue
        state = next_state

        # Optional: validate ABHA ID format (if applicable)
        if hasattr(e, "abha_id") and e.abha_id:
            if not re.match(r"^\d{2}-\d{4}-\d{4}-\d{4}$", e.abha_id):
                anomalies.append(f"Invalid ABHA ID format for patient {e.patient_id}")

    # ✅ Return final validation result
    if not anomalies and state in dfa.accepting_states:
        return {
            "final_state": state,
            "is_valid": True,
            "anomalies": []
        }
    else:
        return {
            "final_state": state,
            "is_valid": False,
            "anomalies": anomalies
        }
