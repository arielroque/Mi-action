import os
import sqlite3
import collections
from datetime import datetime
from constants import General


class Persistence:
    def get_heart_data(self):
        conn = sqlite3.connect("data/"+General.DATABASE_NAME)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM heart;
        """)

        heart_data = collections.OrderedDict()

        for line in cursor.fetchall():
            if(line[2] not in heart_data.keys()):
                l = []
                l.append(line[1])
                heart_data[line[2]] = l
            else:
                heart_data[line[2]].append(line[1])

        keys = list(heart_data.keys())
        keys.reverse()

        values = list(heart_data.values())
        values.reverse()

        response = []
        hearts = []
        dates = []

        for i in range(len(values)):
            if(i > 9):
                break
            average = sum(values[i])/len(values[i])
            hearts.append(average)
            dates.append(keys[i])
        conn.close()

        response.append(dates)
        response.append(hearts)

        return response

    def get_steps_data(self):

        conn = sqlite3.connect("data/"+General.DATABASE_NAME)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM steps;
        """)

        stepData = collections.OrderedDict()

        for line in cursor.fetchall():
            if(line[2] not in stepData.keys()):
                l = []
                l.append(line[1])
                stepData[line[2]] = l
            else:
                stepData[line[2]].append(line[1])

        keys = list(stepData.keys())
        keys.reverse()

        values = list(stepData.values())
        values.reverse()

        response = []
        steps = []
        dates = []

        for i in range(len(values)):
            if(i > 9):
                break
            average = sum(values[i])/len(values[i])
            steps.append(average)
            dates.append(keys[i])

        conn.close()

        response.append(dates)
        response.append(steps)

        return response

    def insert_heart_rate(self, heart_rate):

        date = datetime.today().strftime('%d/%m')

        conn = sqlite3.connect("data/"+General.DATABASE_NAME)
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO heart(qtd, heartDate)
        VALUES (%d,'%s')
        """ % (heart_rate, date))

        conn.commit()
        conn.close()

    def insert_steps(self, steps):
        date = datetime.today().strftime('%d/%m')

        conn = sqlite3.connect("data/"+General.DATABASE_NAME)
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO steps (qtd, stepDate)
        VALUES (%d,'%s')
        """ % (steps, date))

        conn.commit()
        conn.close()

    def prepare_database(self):
        folders = os.listdir("data")
        print("banco")
        print(folders)

        if(General.DATABASE_NAME not in folders):
            conn = sqlite3.connect("data/"+General.DATABASE_NAME)
            c = conn.cursor()

            sql = """CREATE TABLE steps(
                    id INTEGER unique PRIMARY KEY AUTOINCREMENT,
                    qtd INT NOT NULL,
                    stepDate DATE
                    )
                """
            c.executescript(sql)
            conn.commit()

            sql2 = """CREATE TABLE heart(
                    id INTEGER unique PRIMARY KEY AUTOINCREMENT,
                    qtd INT NOT NULL,
                    heartDate DATE
                    )
                """
            c.executescript(sql2)
            conn.commit()

            conn.close()
