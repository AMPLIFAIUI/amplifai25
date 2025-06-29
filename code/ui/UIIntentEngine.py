# UIIntentEngine — real-time preview/override for user-facing outputs

class UIIntentEngine:
    @staticmethod
    def morph_response(text: str) -> str:
        if "error" in text.lower():
            return "⚠️ A system issue occurred. Please retry."
        return text
