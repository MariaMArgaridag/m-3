import mysql.connector
from utils.id_mapper import IdMapper

class AttackRepository:
    def __init__(self, db):
        self.db = db
        self.id_mapper = IdMapper()

    def create(self, attack_type: int, target_industry: int, 
               country: str, year: int, financial_loss: float, affected_users: int):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)

        try:
            cursor.execute(
                """INSERT INTO global_cyber_threats
                (`Attack Type`, `Target Industry`, Country, Year,
                `Financial Loss (in Million $)`, `Number of Affected Users`)
                VALUES (%s, %s, %s, %s, %s, %s)""",
                (attack_type, target_industry, country, year, 
                 financial_loss, affected_users)
            )

            conn.commit()
            internal_id = cursor.lastrowid
            external_id = self.id_mapper.get_external_id(internal_id, 'attack')

            return {
                "id": external_id,
                "attack_type": attack_type,
                "target_industry": target_industry,
                "country": country,
                "year": year,
                "financial_loss": financial_loss,
                "affected_users": affected_users
            }
        except:
            return None

    def list(self):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT
                gct.Id AS internal_id,
                gct.Country,
                gct.Year,
                gct.`Financial Loss (in Million $)` AS financial_loss,
                gct.`Number of Affected Users` AS affected_users,
                atp.Id AS attack_type_id,
                atp.Type AS attack_type,
                src.Id AS attack_source_id,
                src.Source AS attack_source,
                ti.Id AS target_industry_id,
                ti.Industry AS target_industry
            FROM global_cyber_threats gct
            JOIN Attack_Types atp ON atp.Id = gct.`Attack Type`
            JOIN Attack_Sources src ON src.Id = gct.`Attack Source`
            JOIN Target_Industries ti ON ti.Id = gct.`Target Industry`
            ORDER BY gct.Id DESC
            """
        )
        
        rows = cursor.fetchall()
        result = []

        for row in rows:
            external_id = self.id_mapper.get_external_id(row["internal_id"], 'attack')
            result.append({
                "id": external_id,
                "country": row["Country"],
                "year": row["Year"],
                "financial_loss": float(row["financial_loss"]),
                "affected_users": row["affected_users"],
                "attack_type": {
                    "id": self.id_mapper.get_external_id(row["attack_type_id"], 'attack_type'),
                    "type": row["attack_type"]
                },
                "target_industry": {
                    "id": self.id_mapper.get_external_id(row["target_industry_id"], 'target_industry'),
                    "industry": row["target_industry"]
                }
            })

        return result
    
    def get_by_id(self, external_id: str):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        
        internal_id = self.id_mapper.get_internal_id(external_id)
        if internal_id is None:
            return None

        cursor.execute(
            """
            SELECT
                gct.Id AS internal_id,
                gct.Country,
                gct.Year,
                gct.`Financial Loss (in Million $)` AS financial_loss,
                gct.`Number of Affected Users` AS affected_users,
                atp.Id AS attack_type_id,
                atp.Type AS attack_type,
                ti.Id AS target_industry_id,
                ti.Industry AS target_industry
            FROM global_cyber_threats gct
            JOIN Attack_Types atp ON atp.Id = gct.`Attack Type`
            JOIN Target_Industries ti ON ti.Id = gct.`Target Industry`
            WHERE gct.Id = %s
            """,
            (internal_id,)
        )

        row = cursor.fetchone()
        if row is None:
            return None

        return {
            "id": external_id,
            "country": row["Country"],
            "year": row["Year"],
            "financial_loss": float(row["financial_loss"]),
            "affected_users": row["affected_users"],
            "attack_type": {
                "id": self.id_mapper.get_external_id(row["attack_type_id"], 'attack_type'),
                "type": row["attack_type"]
            },
            "target_industry": {
                "id": self.id_mapper.get_external_id(row["target_industry_id"], 'target_industry'),
                "industry": row["target_industry"]
            }
        }
    
    def update(self, external_id: str, attack_type: int = None,
               target_industry: int = None, country: str = None, year: int = None,
               financial_loss: float = None, affected_users: int = None):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        
        internal_id = self.id_mapper.get_internal_id(external_id)
        if internal_id is None:
            return None

        # Busca dados atuais
        cursor.execute(
            "SELECT * FROM global_cyber_threats WHERE Id = %s",
            (internal_id,)
        )
        current = cursor.fetchone()
        if current is None:
            return None

        # Atualiza apenas campos fornecidos
        attack_type = attack_type if attack_type is not None else current['Attack Type']
        target_industry = target_industry if target_industry is not None else current['Target Industry']
        country = country if country is not None else current['Country']
        year = year if year is not None else current['Year']
        financial_loss = financial_loss if financial_loss is not None else float(current['Financial Loss (in Million $)'])
        affected_users = affected_users if affected_users is not None else current['Number of Affected Users']

        cursor.execute(
            """
            UPDATE global_cyber_threats
            SET
                `Attack Type` = %s,
                `Target Industry` = %s,
                Country = %s,
                Year = %s,
                `Financial Loss (in Million $)` = %s,
                `Number of Affected Users` = %s
            WHERE Id = %s
            """,
            (attack_type, target_industry, country, year, 
             financial_loss, affected_users, internal_id)
        )

        if cursor.rowcount == 0:
            return None
        
        conn.commit()

        return {
            "id": external_id,
            "attack_type": attack_type,
            "target_industry": target_industry,
            "country": country,
            "year": year,
            "financial_loss": financial_loss,
            "affected_users": affected_users
        }
    
    def delete(self, external_id: str):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        
        internal_id = self.id_mapper.get_internal_id(external_id)
        if internal_id is None:
            return False

        cursor.execute(
            "DELETE FROM global_cyber_threats WHERE Id = %s",
            (internal_id,)
        )

        if cursor.rowcount == 0:
            return False

        conn.commit()
        self.id_mapper.clear_mapping(external_id)
        return True

    def statistics(self):
        """
        Retorna estatísticas sobre ataques:
        - Total de ataques
        - Ataques por tipo
        - Ataques por país
        - Ataques por ano
        - Perda financeira total
        - Total de usuários afetados
        """
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)

        # Estatísticas gerais
        cursor.execute(
            """
            SELECT
                COUNT(*) AS total_attacks,
                SUM(`Financial Loss (in Million $)`) AS total_financial_loss,
                SUM(`Number of Affected Users`) AS total_affected_users,
                AVG(`Financial Loss (in Million $)`) AS avg_financial_loss,
                AVG(`Number of Affected Users`) AS avg_affected_users
            FROM global_cyber_threats
            """
        )
        general_stats = cursor.fetchone()

        # Ataques por tipo
        cursor.execute(
            """
            SELECT
                atp.Id AS attack_type_id,
                atp.Type AS attack_type,
                COUNT(gct.Id) AS count,
                SUM(gct.`Financial Loss (in Million $)`) AS total_loss,
                SUM(gct.`Number of Affected Users`) AS total_users
            FROM global_cyber_threats gct
            JOIN Attack_Types atp ON atp.Id = gct.`Attack Type`
            GROUP BY atp.Id, atp.Type
            ORDER BY count DESC
            """
        )
        by_type = cursor.fetchall()

        # Ataques por país
        cursor.execute(
            """
            SELECT
                Country,
                COUNT(*) AS count,
                SUM(`Financial Loss (in Million $)`) AS total_loss,
                SUM(`Number of Affected Users`) AS total_users
            FROM global_cyber_threats
            GROUP BY Country
            ORDER BY count DESC
            LIMIT 10
            """
        )
        by_country = cursor.fetchall()

        # Ataques por ano
        cursor.execute(
            """
            SELECT
                Year,
                COUNT(*) AS count,
                SUM(`Financial Loss (in Million $)`) AS total_loss,
                SUM(`Number of Affected Users`) AS total_users
            FROM global_cyber_threats
            GROUP BY Year
            ORDER BY Year DESC
            """
        )
        by_year = cursor.fetchall()

        # Mapear IDs externos
        by_type_mapped = []
        for item in by_type:
            by_type_mapped.append({
                "attack_type": {
                    "id": self.id_mapper.get_external_id(item["attack_type_id"], 'attack_type'),
                    "type": item["attack_type"]
                },
                "count": item["count"],
                "total_financial_loss": float(item["total_loss"] or 0),
                "total_affected_users": item["total_users"] or 0
            })

        return {
            "general": {
                "total_attacks": general_stats["total_attacks"],
                "total_financial_loss": float(general_stats["total_financial_loss"] or 0),
                "total_affected_users": general_stats["total_affected_users"] or 0,
                "avg_financial_loss": float(general_stats["avg_financial_loss"] or 0),
                "avg_affected_users": float(general_stats["avg_affected_users"] or 0)
            },
            "by_type": by_type_mapped,
            "by_country": [
                {
                    "country": item["Country"],
                    "count": item["count"],
                    "total_financial_loss": float(item["total_loss"] or 0),
                    "total_affected_users": item["total_users"] or 0
                }
                for item in by_country
            ],
            "by_year": [
                {
                    "year": item["Year"],
                    "count": item["count"],
                    "total_financial_loss": float(item["total_loss"] or 0),
                    "total_affected_users": item["total_users"] or 0
                }
                for item in by_year
            ]
        }




