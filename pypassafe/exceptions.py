class BrokenDB(Exception):
    def __init__(self, expected_hash: bytes, actual_hash: bytes, hash_algorithm: str):
        self.expected_hash = expected_hash
        self.actual_hash = actual_hash
        self.hash_algorithm = hash_algorithm


class WrongMaster(Exception):
    pass
