from seasons import minutes_output
import datetime

def test_minutes_output():
    assert minutes_output(datetime.date(2023, 11, 19), datetime.date(2023, 11, 18)) == "One thousand, four hundred forty minutes"