# ExtractorEngine — pulls valuable logic fragments from corrupted tasks

class ExtractorEngine:
    @staticmethod
    def salvage(code: str) -> list:
        lines = code.splitlines()
        return [l.strip() for l in lines if "def" in l or "class" in l]
