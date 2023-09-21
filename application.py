from weaving_analyser.analyser import WeavingAnalyzer
import sys
from signal import signal, SIGINT

#* usage: python application.py --ttl xx

def main() -> None:
    weaving_analyzer = WeavingAnalyzer()
    signal(SIGINT, weaving_analyzer.stop)

    num_args = len(sys.argv)
    if num_args >= 3:

        ttl = int(sys.argv[2])
        weaving_analyzer.start(ttl)

    else:
        weaving_analyzer.start()


if __name__ == '__main__':
    main()
