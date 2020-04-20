# ColorCB
Make a csv file of countries that have similar colors in EU4

Place this in the same folder as your eu4.exe file

run simply by using _python color_cb.py_

run with optional arguments _python color_cb.py <distance> <mode>_

distance is a float that finds the color distance between two colors, smaller means the colors must be more similar

mode is either euclidean (fast but simple) or deltaE (CIELAB color comparision, takes about 2 minutes to run, but much closer to human perception, also needs another import to work)
