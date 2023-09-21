from weaving_analyser.analyser import WeavingAnalyzer
import sys
from signal import signal, SIGINT
import requests

#* usage: python application.py --ttl xx

def main() -> None:
    weaving_analyzer = WeavingAnalyzer()
    signal(SIGINT, weaving_analyzer.stop)

    try:
        weaving_analyzer.api_handler.ping()
    except requests.exceptions.ConnectionError as e:
        print("API server failed or is not running.")
        return

    num_args = len(sys.argv)
    if num_args >= 3:

        ttl = int(sys.argv[2])
        weaving_analyzer.start(ttl)

    else:
        weaving_analyzer.start()


if __name__ == '__main__':
    main()
