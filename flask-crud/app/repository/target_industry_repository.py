import mysql.connector

class TargetIndustryRepository:
    def __init__(self, db):
        self.db = db

    def create(self, industry: str):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            "INSERT INTO Target_Industries (industry) VALUES (%s)",
            (industry,)
        )

        conn.commit()

        return {
            "id": cursor.lastrowid,
            "industry": industry
        }

    def list(self):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM Target_Industries")
        return cursor.fetchall()
    
    def get_by_id(self, id: int):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            "SELECT * FROM Target_Industries WHERE id = %s",
            (id,)
        )

        return cursor.fetchone()
    
    def update(self, id: int, industry: str):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            "UPDATE Target_Industries SET industry = %s WHERE id = %s",
            (industry, id)
        )

        if cursor.rowcount == 0:
            return None
        
        conn.commit()

        return {
            "id": id,
            "industry": industry
        }
    
    def delete(self, id: int):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)

        try:
            cursor.execute(
                "DELETE FROM Target_Industries WHERE id = %s",
                (id,)
            )

            if cursor.rowcount == 0:
                return False

            conn.commit()
            return True

        except mysql.connector.Error as err:
            conn.rollback()

            if err.errno == 1451:
                return "FK"

            raise err