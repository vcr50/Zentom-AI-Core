def build_replay_packet(incident: dict, model_output: dict, policy_output: dict) -> dict:
    return {
        "incident": incident,
        "model_output": model_output,
        "policy_output": policy_output,
    }

