import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from utils import recommend

def test_recommend():
    assert recommend(0.7, 0.5) == "Kündigung wahrscheinlich: Kundenbindung verstärken!"
    assert recommend(0.3, 0.5) == "Kein akutes Risiko"
