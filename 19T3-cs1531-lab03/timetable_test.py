import pytest
from timetable import *
def test_timetable():
    #given example
    assert timetable([date(2019,9,27), date(2019,9,30)], [time(14,10), time(10,30)]) == [datetime(2019,9,27,10,30), datetime(2019,9,27,14,10), datetime(2019,9,30,10,30), datetime(2019,9,30,14,10)]
    
    #multiple date, 1 time
    assert timetable([date(2019,9,27), date(2019,9,30)], [time(10,30)]) == [datetime(2019,9,27,10,30), datetime(2019,9,30,10,30)]
    
    #1 date multiple time
    assert timetable([date(2019,9,27)], [time(14,10), time(10,30)]) == [datetime(2019,9,27,10,30), datetime(2019,9,27,14,10)]
    
    #1 date 1 time
    assert timetable([date(2019,9,27)],[time(14,10)]) == [datetime(2019,9,27,14,10)]
    
    with pytest.raises(Exception):
       timetable([date(2019,9,27)]) 
 