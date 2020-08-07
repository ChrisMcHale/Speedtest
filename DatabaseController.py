from datetime import datetime
import mysql.connector, json, logging

log = logging.getLogger(__name__)


class DatabaseController:
    db = mysql.connector.connect()
    config = ''
    cursor = ''

    def __init__(self):
        #Get the configuration values when we're instantiated
        global config
        config = self.getConfig()

    def connectToDB(self):
        global db
        global cursor
        #Attempt to connect the database using values from the configuration file
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
        #Create a cursor so that we can execute prepared statements against the database
        cursor = db.cursor(prepared=True)
        return cursor

    def disconnectFromDB(self):
        global db
        global cursor
        #Attempt a clean disconnection from the database
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
        #Define the prepared statement we should use to enter the results into our database table
        query = """INSERT INTO results (date, sent, recieved, download, upload, ping, server, url) VALUES (%s,%s,%s,%s,%s,
        %s,%s,%s) """
        #Create and populate a tuple containing the results, from the passed results dictionary, that we want to enter into the database
        #In addition, prepend the tuple with the current date and time
        qtuple = (
        str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")), results.get("bytes_sent"), results.get("bytes_rec"), results.get("download_rate"),
        results.get("upload_rate"), results.get("ping"), results.get("server"), results.get("url"))
        try:
            #Connect to the Database
            self.connectToDB()
            log.info("Inserting values")
            #Execute the prepared statement, loaded with the results tuple
            cursor.execute(query, qtuple)
            #Commit the changes to the datebase
            db.commit()
            log.info(str(cursor.rowcount) + " record inserted")
            #Disconnect cleanly
            self.disconnectFromDB()
        except mysql.connector.Error as error:
            log.exception(" Error {}".format(error))

    def getConfig(self):
        try:
            #Open the database config file
            with open('database.json') as config_file:
                #Create and populate the config object so we can access the values later
                config = json.load(config_file)
            return config
        except IOError:
            log.exception("I/O Error when opening configuration file")

