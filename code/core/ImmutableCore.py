# ImmutableCore — final gating layer before logic execution

class ImmutableCore:
    @staticmethod
    def validate_and_commit(logic: str) -> bool:
        if "self-destruct" in logic or "format_disk" in logic:
            return False
        return True  # Allow commit to memory
