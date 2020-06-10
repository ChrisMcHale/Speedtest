from datetime import datetime
import mysql.connector, json, logging

log = logging.getLogger(__name__)


class DatabaseController:
    db = mysql.connector.connect()
    config = ''
    cursor = ''

    def __init__(self):
        global config
        config = self.getConfig()

    def connectToDB(self):
        global db
        global cursor
        try:
            log.info("Connecting to Database")
            db = mysql.connector.connect(
                host=config['HOST'],
                user=config['USER'],
                password=config['PASS'],
                database=config['DB']
            )
            log.info("Connected")
        except mysql.connector.Error as error:
            log.error("Connection Error".format(error))
        cursor = db.cursor(prepared=True)
        return cursor

    def disconnectFromDB(self):
        global db
        global cursor
        try:
            log.info("Disconnecting from Database")
            if db.is_connected():
                cursor.close()
                db.close()
                log.info("Disconnected")
        except mysql.connector.Error as error:
            log.exception("Connection Error".format(error))

    def addResults(self, results):
        global cursor
        query = """INSERT INTO results (date, sent, recieved, download, upload, ping, server, url) VALUES (%s,%s,%s,%s,%s,
        %s,%s,%s) """
        qtuple = (
        str(datetime.now()), results.get("bytes_sent"), results.get("bytes_rec"), results.get("download_rate"),
        results.get("upload_rate"), results.get("ping"), results.get("server"), results.get("url"))
        try:
            self.connectToDB()
            log.info("Inserting values")
            cursor.execute(query, qtuple)
            db.commit()
            log.info(str(cursor.rowcount) + " record inserted")
            self.disconnectFromDB()
        except mysql.connector.Error as error:
            log.exception(" Error {}".format(error))

    def getConfig(self):
        try:
            with open('database.json') as config_file:
                config = json.load(config_file)
            return config
        except IOError:
            log.exception("I/O Error when opening configuration file")

