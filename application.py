from weaving_analyser.analyser import WeavingAnalyzer
import sys
import requests
from weaving_analyser.api import APIhandler

#* usage: python application.py --ttl xx

def main() -> None:
    weaving_analyzer = WeavingAnalyzer()
    api_handler = APIhandler()

    try:
        api_handler.ping()
    except requests.exceptions.ConnectionError as e:
        print("API server failed or is not running.")
        return

    del api_handler # delete api_handler to avoid memory leak
    
    num_args = len(sys.argv)
    ttl = None
    if num_args >= 3:
        try:
            ttl = int(sys.argv[2])
        except ValueError:
            print("Invalid ttl value.\n usage: python application.py --ttl <n_seconds>")
            return

    try:
        weaving_analyzer.start(ttl)
    except KeyboardInterrupt:
        weaving_analyzer.stop()


if __name__ == '__main__':
    main()
