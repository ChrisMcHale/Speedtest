import speedtest, DatabaseController, sys, logging, os

# Initialise and configure the logger
log = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=os.environ.get("LOGLEVEL", "INFO"))

#Declare the globals
s = speedtest.Speedtest()
dbc = DatabaseController.DatabaseController()


def getSpeedTestResults():
    #Pre-populate the results dictionary with fail-state responses
    results = {
        "server": "Unable to determine server",
        "bytes_sent": "0",
        "bytes_rec": "0",
        "download_rate": "0",
        "upload_rate": "0",
        "ping": "0",
        "url": "Unable to determine server"
    }
    log.info("Attempting Speedtest")
    try:
        #Attempt to find the best server to test against
        if (s.get_best_server()):
            log.info("Connected to server "+s.best["host"])
            #If we've located a server, begin the upload and download tests
            s.download()
            s.upload(pre_allocate=False)
            #Populate the results dictionary with real results
            results["server"] = s.best["host"]
            results["bytes_sent"] = str(s.results.bytes_sent)
            results["bytes_rec"] = str(s.results.bytes_received)
            results["download_rate"] = str(int(s.results.download))
            results["upload_rate"] = str(int(s.results.upload))
            results["ping"] = str(s.results.ping)
            results["url"] = s.results.share()
            log.info("Sending results to database")
            #Add the measured metrics to the database
            dbc.addResults(results)
        else:
            #If we can't get a server to test against, submit the fail-state results
            dbc.addResults(results)
    except:
        error = sys.exc_info()[0]
        log.exception(error)
        dbc.addResults(results)


if __name__ == "__main__":
    getSpeedTestResults()