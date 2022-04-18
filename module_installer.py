import sys
import subprocess

module = ['geopy']
# implement pip as a subprocess:
for i in module:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install',
                           i])