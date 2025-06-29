# ContentBlockSync
class ContentBlockSync:
    store = {}

    @staticmethod
    def update(block_id: str, content: str):
        ContentBlockSync.store[block_id] = content
        return True

    @staticmethod
    def get(block_id: str):
        return ContentBlockSync.store.get(block_id, "")
