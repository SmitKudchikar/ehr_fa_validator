class DFA:
    def __init__(self, start_state, accepting_states):
        self.start_state = start_state
        self.accepting_states = set(accepting_states)
        self.transitions = {}

    def add_transition(self, state, symbol, next_state):
        self.transitions[(state, symbol)] = next_state

    def get_next_state(self, state, symbol):
        """Return next state if transition exists, else None."""
        return self.transitions.get((state, symbol))

    def run(self, events):
        state = self.start_state
        anomalies = []
        for ev in events:
            key = (state, ev.event_type)
            if key not in self.transitions:
                anomalies.append(f"Invalid transition: {state} -> {ev.event_type}")
            else:
                state = self.transitions[key]
        return state, anomalies
