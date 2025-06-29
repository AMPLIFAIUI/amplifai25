# QuarantineEngine
class QuarantineEngine:
    @staticmethod
    def verify(output: str) -> bool:
        return "error" not in output.lower() and len(output.strip()) > 10
