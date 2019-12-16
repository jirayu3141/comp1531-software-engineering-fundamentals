from pointutil import fn_get, fn_create, fn_update, fn_delete, reset_data

def test_point_createget():
    reset_data()
    fn_create(2, 3)
    assert fn_get() == (2, 3)

def test_point_checkempty():
    reset_data()
    assert fn_get() == (0, 0)