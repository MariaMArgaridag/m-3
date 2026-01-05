import mysql.connector
from utils.id_mapper import IdMapper

class DefenseMechanismRepository:
    def __init__(self, db):
        self.db = db
        self.id_mapper = IdMapper()

    def create(self, mechanism: str):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            "INSERT INTO Defense_Mechanisms (mechanism) VALUES (%s)",
            (mechanism,)
        )

        conn.commit()
        internal_id = cursor.lastrowid
        external_id = self.id_mapper.get_external_id(internal_id, 'defense')

        return {
            "id": external_id,
            "mechanism": mechanism
        }

    def list(self):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM Defense_Mechanisms")
        rows = cursor.fetchall()
        result = []
        for row in rows:
            external_id = self.id_mapper.get_external_id(row['Id'], 'defense')
            result.append({
                "id": external_id,
                "mechanism": row['Mechanism']
            })
        return result
    
    def get_by_id(self, external_id: str):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        
        internal_id = self.id_mapper.get_internal_id(external_id)
        if internal_id is None:
            return None

        cursor.execute(
            "SELECT * FROM Defense_Mechanisms WHERE Id = %s",
            (internal_id,)
        )

        row = cursor.fetchone()
        if row is None:
            return None
        
        return {
            "id": external_id,
            "mechanism": row['Mechanism']
        }
    
    def update(self, external_id: str, mechanism: str):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        
        internal_id = self.id_mapper.get_internal_id(external_id)
        if internal_id is None:
            return None

        cursor.execute(
            "UPDATE Defense_Mechanisms SET Mechanism = %s WHERE Id = %s",
            (mechanism, internal_id)
        )

        if cursor.rowcount == 0:
            return None
        
        conn.commit()

        return {
            "id": external_id,
            "mechanism": mechanism
        }
    
    def delete(self, external_id: str):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        
        internal_id = self.id_mapper.get_internal_id(external_id)
        if internal_id is None:
            return False

        try:
            cursor.execute(
                "DELETE FROM Defense_Mechanisms WHERE Id = %s",
                (internal_id,)
            )

            if cursor.rowcount == 0:
                return False

            conn.commit()
            self.id_mapper.clear_mapping(external_id)
            return True

        except mysql.connector.Error as err:
            conn.rollback()

            if err.errno == 1451:
                return "FK"

            raise err

    def statistics(self):
        """
        Retorna estatísticas sobre mecanismos de defesa:
        - Total de mecanismos
        - Uso de cada mecanismo em ataques
        - Efetividade (baseado em tempo de resolução)
        """
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)

        # Total de mecanismos
        cursor.execute("SELECT COUNT(*) AS total FROM Defense_Mechanisms")
        total = cursor.fetchone()["total"]

        # Uso de cada mecanismo em ataques
        cursor.execute(
            """
            SELECT
                dm.Id AS defense_mechanism_id,
                dm.Mechanism AS mechanism,
                COUNT(gct.Id) AS usage_count,
                AVG(gct.`Incident Resolution Time (in Hours)`) AS avg_resolution_time,
                SUM(gct.`Financial Loss (in Million $)`) AS total_financial_loss,
                SUM(gct.`Number of Affected Users`) AS total_affected_users
            FROM Defense_Mechanisms dm
            LEFT JOIN global_cyber_threats gct ON gct.`Defense Mechanism Used` = dm.Id
            GROUP BY dm.Id, dm.Mechanism
            ORDER BY usage_count DESC
            """
        )
        usage_stats = cursor.fetchall()

        result = {
            "total_defense_mechanisms": total,
            "mechanisms": []
        }

        for item in usage_stats:
            external_id = self.id_mapper.get_external_id(item["defense_mechanism_id"], 'defense')
            result["mechanisms"].append({
                "defense_mechanism": {
                    "id": external_id,
                    "mechanism": item["mechanism"]
                },
                "usage_count": item["usage_count"] or 0,
                "avg_resolution_time_hours": float(item["avg_resolution_time"] or 0),
                "total_financial_loss": float(item["total_financial_loss"] or 0),
                "total_affected_users": item["total_affected_users"] or 0
            })

        return result