import speedtest, DatabaseController, sys, logging, os

log = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=os.environ.get("LOGLEVEL", "INFO"))

s = speedtest.Speedtest()
dbc = DatabaseController.DatabaseController()


def getSpeedTestResults():
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
        if (s.get_best_server()):
            log.info("Connected to server "+s.best["host"])
            s.download()
            s.upload(pre_allocate=False)
            results["server"] = s.best["host"]
            results["bytes_sent"] = str(s.results.bytes_sent)
            results["bytes_rec"] = str(s.results.bytes_received)
            results["download_rate"] = str(int(s.results.download))
            results["upload_rate"] = str(int(s.results.upload))
            results["ping"] = str(s.results.ping)
            results["url"] = s.results.share()
            log.info("Sending results to database")
            dbc.addResults(results)
    except:
        error = sys.exc_info()[0]
        log.exception(error)
        dbc.addResults(results)


if __name__ == "__main__":
    getSpeedTestResults()