activate_this='/home/pi/Documents/greenhouse/venv/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))
import sys
sys.path.insert(0, '/home/pi/Documents/greenhouse')
from app import application as application
