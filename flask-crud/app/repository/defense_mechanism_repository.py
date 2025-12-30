import mysql.connector

class DefenseMechanismRepository:
    def __init__(self, db):
        self.db = db

    def create(self, mechanism: str):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            "INSERT INTO Defense_Mechanisms (mechanism) VALUES (%s)",
            (mechanism,)
        )

        conn.commit()

        return {
            "id": cursor.lastrowid,
            "mechanism": mechanism
        }

    def list(self):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM Defense_Mechanisms")
        return cursor.fetchall()
    
    def get_by_id(self, id: int):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            "SELECT * FROM Defense_Mechanisms WHERE id = %s",
            (id,)
        )

        return cursor.fetchone()
    
    def update(self, id: int, mechanism: str):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            "UPDATE Defense_Mechanisms SET mechanism = %s WHERE id = %s",
            (mechanism, id)
        )

        if cursor.rowcount == 0:
            return None
        
        conn.commit()

        return {
            "id": id,
            "mechanism": mechanism
        }
    
    def delete(self, id: int):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)

        try:
            cursor.execute(
                "DELETE FROM Defense_Mechanisms WHERE id = %s",
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