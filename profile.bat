python -m cProfile -o trading.cprof trading.py --noplot
pyprof2calltree -k -i trading.cprof