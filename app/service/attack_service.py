class AttackService:
    def __init__(self, repository):
        self.repo = repository

    def create(self, attack_type: int, target_industry: int,
               country: str, year: int, financial_loss: float, affected_users: int):
        return self.repo.create(attack_type, target_industry, 
                                country, year, financial_loss, affected_users)

    def list(self):
        return self.repo.list()

    def get_by_id(self, external_id: str):
        return self.repo.get_by_id(external_id)
    
    def update(self, external_id: str, attack_type: int = None,
               target_industry: int = None, country: str = None, year: int = None,
               financial_loss: float = None, affected_users: int = None):
        return self.repo.update(external_id, attack_type, target_industry,
                               country, year, financial_loss, affected_users)
    
    def delete(self, external_id: str):
        return self.repo.delete(external_id)

    def statistics(self):
        return self.repo.statistics()




