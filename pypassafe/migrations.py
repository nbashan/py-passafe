class MigrateableObject:
    def update_to_last(self) -> "MigrateableObject":
        raise NotImplementedError()
