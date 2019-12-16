import pytest

def pointchange(point, change):
	x, y = point
	x += change	
	y += change	
	return (x, y)

@pytest.fixture
def supply_point():
	return (1, 2)

@pytest.mark.up
def test_1(supply_point):
	assert pointchange(supply_point, 1) == (2, 3)

@pytest.mark.up
def test_2(supply_point):
	assert pointchange(supply_point, 5) == (6, 7)

@pytest.mark.up
def test_3(supply_point):
	assert pointchange(supply_point, 100) == (101, 102)

@pytest.mark.down
def test_4(supply_point):
	assert pointchange(supply_point, -5) == (-4, -3)

@pytest.mark.skip
def test_5(supply_point):
	assert False == True, "This test is skipped"

@pytest.mark.xfail
def test_6(supply_point):
	assert False == True, "This test's output is muted"
