class DefenseMechanismService:
    def __init__(self, repository):
        self.repo = repository

    def create(self, mechanism: str):
        return self.repo.create(mechanism)

    def list(self):
        return self.repo.list()

    def get_by_id(self, external_id: str):
        return self.repo.get_by_id(external_id)
    
    def update(self, external_id: str, mechanism: str):
        return self.repo.update(external_id, mechanism)
    
    def delete(self, external_id: str):
        return self.repo.delete(external_id)

    def statistics(self):
        return self.repo.statistics()