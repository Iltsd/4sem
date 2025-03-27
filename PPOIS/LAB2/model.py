import sqlite3
import xml.dom.minidom


# Модель (Model)
class TournamentModel:
    def __init__(self, db_name="tournaments.db"):
        self.conn = sqlite3.connect(db_name)
        self.create_table()

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS tournaments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            date TEXT,
            sport TEXT,
            winner TEXT,
            prize_money REAL,
            winner_earnings REAL
        )''')
        self.conn.commit()

    def add_tournament(self, name, date, sport, winner, prize_money):
        winner_earnings = prize_money * 0.6
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO tournaments (name, date, sport, winner, prize_money, winner_earnings) VALUES (?, ?, ?, ?, ?, ?)",
                       (name, date, sport, winner, prize_money, winner_earnings))
        self.conn.commit()

    def get_all_tournaments(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM tournaments")
        return cursor.fetchall()

    def search_tournaments(self, conditions):
        query = "SELECT * FROM tournaments WHERE 1=1"
        params = []
        if "name" in conditions and conditions["name"]:
            query += " AND name LIKE ?"
            params.append(f"%{conditions['name']}%")
        if "date" in conditions and conditions["date"]:
            query += " AND date = ?"
            params.append(conditions["date"])
        if "sport" in conditions and conditions["sport"]:
            query += " AND sport = ?"
            params.append(conditions["sport"])
        if "winner" in conditions and conditions["winner"]:
            query += " AND winner LIKE ?"
            params.append(f"%{conditions['winner']}%")
        if "prize_min" in conditions and conditions["prize_min"]:
            query += " AND prize_money >= ?"
            params.append(conditions["prize_min"])
        if "prize_max" in conditions and conditions["prize_max"]:
            query += " AND prize_money <= ?"
            params.append(conditions["prize_max"])
        cursor = self.conn.cursor()
        cursor.execute(query, params)
        return cursor.fetchall()

    def delete_tournaments(self, conditions):
        query = "DELETE FROM tournaments WHERE 1=1"
        params = []
        if "name" in conditions and conditions["name"]:
            query += " AND name LIKE ?"
            params.append(f"%{conditions['name']}%")
        if "date" in conditions and conditions["date"]:
            query += " AND date = ?"
            params.append(conditions["date"])
        if "sport" in conditions and conditions["sport"]:
            query += " AND sport = ?"
            params.append(conditions["sport"])
        if "winner" in conditions and conditions["winner"]:
            query += " AND winner LIKE ?"
            params.append(f"%{conditions['winner']}%")
        if "prize_min" in conditions and conditions["prize_min"]:
            query += " AND prize_money >= ?"
            params.append(conditions["prize_min"])
        if "prize_max" in conditions and conditions["prize_max"]:
            query += " AND prize_money <= ?"
            params.append(conditions["prize_max"])
        cursor = self.conn.cursor()
        cursor.execute(query, params)
        deleted = cursor.rowcount
        self.conn.commit()
        return deleted

    def save_to_xml(self, filename):
        doc = xml.dom.minidom.Document()
        root = doc.createElement("tournaments")
        doc.appendChild(root)
        for row in self.get_all_tournaments():
            tournament = doc.createElement("tournament")
            for i, field in enumerate(["id", "name", "date", "sport", "winner", "prize_money", "winner_earnings"]):
                child = doc.createElement(field)
                child.appendChild(doc.createTextNode(str(row[i])))
                tournament.appendChild(child)
            root.appendChild(tournament)
        with open(filename, "w", encoding="utf-8") as f:
            f.write(doc.toprettyxml(indent="  "))
