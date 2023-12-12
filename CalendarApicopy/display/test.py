import os
script_dir = os.path.dirname(os.path.abspath(__file__))
print(script_dir)

print("Current working directory:", os.getcwd())
print("font path: " + script_dir + "/Arial_Bold.ttf")