import pytest
from datetime import datetime
from pytest_tr_odoo.fixtures import env
from pytest_tr_odoo import utils
from .test_openacademy1 import os_model, session


@pytest.fixture
def wizard_model(env):
    return env['openacademy.wizard']


'''
openacademy.wizard
'''


def test_default_session(wizard_model, session):
    wizard = wizard_model.with_context({'active_id': session.id}).create({})
    assert wizard.session_id == session


@pytest.mark.parametrize('test_input,expected', [
    ({'attendee_ids': [(0, 0,
                        {'name': 'name lastname',
                         'email': 'name@gmail.com'})]},
     ['name@gmail.com']),
    ({'attendee_ids': [(0, 0,
                        {'name': 'name lastname',
                         'email': 'name@gmail.com'}),
                       (0, 0,
                        {'name': 'gandum black',
                         'email': 'black@hotmail.com'})]},
     ['name@gmail.com', 'black@hotmail.com']),
])
def test_subscribe(wizard_model, session, test_input, expected):
    wizard = wizard_model\
        .with_context({'active_id': session.id})\
        .create(test_input)
    wizard.subscribe()

    def validate(value):
        print(value)
        assert value in expected
    map(validate, session.attendee_ids.mapped('email'))




@pytest.fixture
def MultipleWizard_model(env):
    return env['openacademy.multi_wizard']

def test_default_sessionmulti(MultipleWizard_model, session):
    wizardm = MultipleWizard_model.with_context({'active_ids': session.id}).create({})
    assert wizardm.session_ids == session

@pytest.mark.parametrize('test_input,expected', [
    ({'attendee_ids': [(0, 0,
                        {'name': 'name lastname',
                         'email': 'name@gmail.com'})]},
     ['name@gmail.com']),
    ({'attendee_ids': [(0, 0,
                        {'name': 'name lastname',
                         'email': 'name@gmail.com'}),
                       (0, 0,
                        {'name': 'gandum black',
                         'email': 'black@hotmail.com'})]},
     ['name@gmail.com', 'black@hotmail.com']),
])
def test_subscribemulti(MultipleWizard_model, session, test_input, expected):
    wizardm = MultipleWizard_model\
        .with_context({'active_ids': session.id})\
        .create(test_input)
    wizardm.subscribe()

    def validate(value):
        assert value in expected
    map(validate, session.attendee_ids.mapped('email'))

