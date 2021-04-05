import pytest
from datetime import datetime
from odoo import exceptions
from pytest_tr_odoo.fixtures import env
from pytest_tr_odoo import utils


@pytest.fixture
def openacademy_model(env):
    return env['openacademy.openacademy']


@pytest.fixture
def os_model(env):
    return env['openacademy.session']


@pytest.mark.parametrize('test_input,expected', [
    ({'first_name':'namenew','last_name':'lastnamenew','value':9} #test_input
    ,'namenew lastnamenew')#expected  
])
def test_compute_full_name(openacademy_model,test_input,expected):
    openacademy = openacademy_model.create(test_input)
    assert openacademy.full_name == expected


@pytest.mark.parametrize('test_input,expected', [
    ({'first_name': 'namenew', 'last_name': 'lastnamenew', 'value': 9,
        'num': 0}, 'Copy of lastnamenew'),
    ({'first_name': 'Radchapoom', 'last_name': 'lastnamenew', 'value': 10,
        'num': 1}, 'Copy of lastnamenew (1)'),
    ])
def test_copy_last_name(openacademy_model, test_input, expected):
    openacademy = openacademy_model.create(test_input)
    for l in range(test_input['num']):
        openacademy.copy()
    assert openacademy._copy_last_name() == expected


@pytest.mark.parametrize('test_input,expected', [
    ({'first_name': 'namenew', 'last_name': 'lastnamenew', 'value': 9,
        'num': 0}, 'Copy of lastnamenew'),
    ({'first_name': 'Radchapoom', 'last_name': 'lastnamenew', 'value': 10,
        'num': 1}, 'Copy of lastnamenew (1)'),
    ])
def test_copy(monkeypatch, mocker, openacademy_model, test_input, expected):
    openacademy = openacademy_model.create(test_input)
    monkeypatch.setattr(type(openacademy), '_copy_last_name', lambda a: 'Copy')
    spy = mocker.spy(type(openacademy), '_copy_last_name')
    data = openacademy.copy()
    assert spy.called
    assert data.last_name == 'Copy'



'''
session
'''
@pytest.mark.parametrize('test_input,expected', [
    ({'name': 'time1', 'start_date': '2021-04-01'},
        '2021-04-01'),
    ({'name': 'time2', 'start_date': '2021-04-02', 'duration': 1},
        '2021-04-02'),
        ({'name': 'time3', 'start_date': '2021-04-03', 'duration': 2},
        '2021-04-04'),
    ])
def test_compute_end_date(os_model, test_input, expected):
    session = os_model.create(test_input)
    session.end_date.strftime('%Y-%m-%d')
    assert session.end_date.strftime('%Y-%m-%d') == expected


@pytest.mark.parametrize('test_input,expected', [
    ({'name': 'time0', 'start_date': False, 'end_date': '2021-01-01'},
     False),
    ({'name': 'time1', 'start_date': '2021-04-01',
         'end_date': '2021-04-02'},
        2),
    ({'name': 'time2', 'start_date': '2021-04-02',
        'end_date': '2021-04-02'},
        1),
        ({'name': 'time3', 'start_date': '2021-04-03',
         'end_date': '2021-04-06'},   
        4),
    ])
def test_inverse_end_date(os_model, test_input, expected):
    session = os_model.create(test_input)
    assert session.duration == expected


@pytest.mark.parametrize('test_input,expected', [
    ({'name': 'time1', 'duration': 1},
     24),
    ({'name': 'time2', 'duration': 2},
     48),
])
def test__compute_hours(os_model, test_input, expected):
    session = os_model.create(test_input)
    assert session.hours == expected


@pytest.mark.parametrize('test_input,expected', [
    ({'name': 'time1', 'hours': 24},
     1),
    ({'name': 'time2', 'hours': 96},
     4),
])
def test_inverse_hours(os_model, test_input, expected):
    session = os_model.create(test_input)
    assert session.duration == expected


@pytest.mark.parametrize('test_input,expected', [
    ({'name': 'chair1', 'seats': -1,
      'attendee_ids': [(0, 0,
                        {'name': 'nisit odoo',
                         'email': 'nisit@gmail.com'})]},0),
    ({'name': 'chair2', 'seats': 0,
      'attendee_ids': [(0, 0,
                        {'name': 'natsuksa toy',
                         'email': 'natsuksa@gmail.com'})]},0),
    ({'name': 'Inevitables', 'seats': 1,
      'attendee_ids': [(0, 0,
                        {'name': 'gandum Red',
                         'email': 'gandum@gmail.com'})]},100),
])
def test_compute_taken_seats(os_model, test_input, expected):
    session = os_model.create(test_input)
    assert session.taken_seats == expected


@pytest.mark.parametrize('test_input,expected', [
    ({'name': 'gandum', 'seats': -1,
      'attendee_ids': [(0, 0,
                        {'name': 'name lastname',
                         'email': 'name@gmail.com'})]},
     {'warning': {
         'title': 'Incorrect \'seats\' value',
         'message': 'The number of available seatsmay not be negative'
         }}),

    ({'name': 'gandum', 'seats': 0,
      'attendee_ids': [(0, 0,
                        {'name': 'name lastname',
                         'email': 'name@gmail.com'})]},
     {'warning': {
         'title': 'Too many attendees',
         'message': 'Increase seats or remove excess attendees'
         }}),

    ({'name': 'gandum', 'seats': 2,
      'attendee_ids': [(0, 0,
                        {'name': 'name lastname',
                         'email': 'name@gmail.com'}),
                        (0, 0,
                        {'name': 'name lastname',
                         'email': 'name@gmail.com'})]},
     False),
])
def test_verify_valid_seats(os_model, test_input, expected):
    session = os_model.create(test_input)
    verify = session._verify_valid_seats()

    if expected:
        assert verify == expected
    else:
        assert not verify


@pytest.fixture
def partner(env):
    return env['res.partner'].create({
        'name': 'name lingmodel'
    })

@pytest.mark.parametrize('test_input,expected', [
    ({'name': 'gandum', 'seats': 10,
      'attendee_ids': []}, 'A session\'s instructor can\'t be an attendee')
])
def test_check_instructor_not_in_attendees(os_model,
                                           partner,
                                           test_input, expected):
    test_input['instructor_id'] = partner.id
    test_input['attendee_ids'].append((4, partner.id))
    with pytest.raises(exceptions.ValidationError) as excinfo:
        os_model.create(test_input)
    assert excinfo.value.name == expected
         



'''
wizard
'''
@pytest.fixture
def session(os_model):
    return os_model.create({
        'name': 'sendTOwizard'
    })

