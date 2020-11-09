import pytest

from rotkehlchen.accounting.structures import Balance, BalanceSheet
from rotkehlchen.constants.assets import A_BTC, A_DAI, A_ETH, A_EUR, A_USD
from rotkehlchen.errors import InputError
from rotkehlchen.fval import FVal


def test_balance_addition():
    a = Balance(amount=FVal('1.5'), usd_value=FVal('1.6'))
    b = Balance(amount=FVal('2.5'), usd_value=FVal('2.7'))
    c = Balance(amount=FVal('3'), usd_value=FVal('3.21'))

    result = Balance(amount=FVal('7'), usd_value=FVal('7.51'))
    assert result == a + b + c
    assert a + b + c == result
    result += c
    assert result == Balance(amount=FVal('10'), usd_value=FVal('10.72'))

    with pytest.raises(InputError):
        result = a + 5

    d = {'amount': 10, 'usd_value': 11}
    e = {'amount': '5', 'usd_value': '6'}
    f = {'amount': FVal('20'), 'usd_value': FVal('22')}
    result = Balance(amount=FVal('38'), usd_value=FVal('42.21'))
    assert result == c + d + e + f
    assert c + d + e + f == result

    with pytest.raises(InputError):
        result = a + {'foo': 1}
    with pytest.raises(InputError):
        result = a + {'amount': 'fasd', 'usd_value': 1}
    with pytest.raises(InputError):
        result = a + {'amount': 1, 'usd_value': 'dsad'}


def test_balance_sheet_addition():
    a = BalanceSheet(
        assets={
            A_USD: Balance(amount=FVal('2'), usd_value=FVal('2')),
            A_ETH: Balance(amount=FVal('1.5'), usd_value=FVal('450')),
        },
        liabilities={
            A_DAI: Balance(amount=FVal('5'), usd_value=FVal('5.1')),
            A_ETH: Balance(amount=FVal('0.5'), usd_value=FVal('150')),
        },
    )
    b = BalanceSheet(
        assets={
            A_EUR: Balance(amount=FVal('3'), usd_value=FVal('3.5')),
            A_ETH: Balance(amount=FVal('3'), usd_value=FVal('900')),
            A_BTC: Balance(amount=FVal('1'), usd_value=FVal('10000')),
        },
        liabilities={
            A_DAI: Balance(amount=FVal('10'), usd_value=FVal('10.2')),
        },
    )
    assert a != b
    c = BalanceSheet(
        assets={
            A_EUR: Balance(amount=FVal('3'), usd_value=FVal('3.5')),
            A_USD: Balance(amount=FVal('2'), usd_value=FVal('2')),
            A_ETH: Balance(amount=FVal('4.5'), usd_value=FVal('1350')),
            A_BTC: Balance(amount=FVal('1'), usd_value=FVal('10000')),
        },
        liabilities={
            A_DAI: Balance(amount=FVal('15'), usd_value=FVal('15.3')),
            A_ETH: Balance(amount=FVal('0.5'), usd_value=FVal('150')),
        },
    )
    assert a + b == c


def test_balance_sheet_subtraction():
    a = BalanceSheet(
        assets={
            A_USD: Balance(amount=FVal('2'), usd_value=FVal('2')),
            A_ETH: Balance(amount=FVal('3'), usd_value=FVal('900')),
        },
        liabilities={
            A_DAI: Balance(amount=FVal('5'), usd_value=FVal('5.1')),
            A_ETH: Balance(amount=FVal('0.5'), usd_value=FVal('150')),
        },
    )
    b = BalanceSheet(
        assets={
            A_EUR: Balance(amount=FVal('3'), usd_value=FVal('3.5')),
            A_ETH: Balance(amount=FVal('1.5'), usd_value=FVal('450')),
            A_BTC: Balance(amount=FVal('1'), usd_value=FVal('10000')),
        },
        liabilities={
            A_DAI: Balance(amount=FVal('10'), usd_value=FVal('10.2')),
        },
    )
    assert a != b
    c = BalanceSheet(
        assets={
            A_EUR: Balance(amount=FVal('-3'), usd_value=FVal('-3.5')),
            A_USD: Balance(amount=FVal('2'), usd_value=FVal('2')),
            A_ETH: Balance(amount=FVal('1.5'), usd_value=FVal('450')),
            A_BTC: Balance(amount=FVal('-1'), usd_value=FVal('-10000')),
        },
        liabilities={
            A_DAI: Balance(amount=FVal('-5'), usd_value=FVal('-5.1')),
            A_ETH: Balance(amount=FVal('0.5'), usd_value=FVal('150')),
        },
    )
    assert a - b == c


def test_balance_sheet_serialize():
    a = BalanceSheet(
        assets={
            A_USD: Balance(amount=FVal('2'), usd_value=FVal('2')),
            A_ETH: Balance(amount=FVal('3'), usd_value=FVal('900')),
        },
        liabilities={
            A_DAI: Balance(amount=FVal('5'), usd_value=FVal('5.1')),
            A_ETH: Balance(amount=FVal('0.5'), usd_value=FVal('150')),
        },
    )
    a.serialize() == {
        'assets': {
            'USD': {'amount': '2', 'usd_value': '2'},
            'ETH': {'amount': '3', 'usd_value': '900'},
        },
        'liabilities': {
            'DAI': {'amount': '5', 'usd_value': '5.1'},
            'ETH': {'amount': '0.5', 'usd_value': '150'},
        }
    }


def test_balance_sheet_to_dict():
    a = BalanceSheet(
        assets={
            A_USD: Balance(amount=FVal('2'), usd_value=FVal('2')),
            A_ETH: Balance(amount=FVal('3'), usd_value=FVal('900')),
        },
        liabilities={
            A_DAI: Balance(amount=FVal('5'), usd_value=FVal('5.1')),
            A_ETH: Balance(amount=FVal('0.5'), usd_value=FVal('150')),
        },
    )
    a.to_dict() == {
        'assets': {
            'USD': {'amount': FVal('2'), 'usd_value': FVal('2')},
            'ETH': {'amount': FVal('3'), 'usd_value': FVal('900')},
        },
        'liabilities': {
            'DAI': {'amount': FVal('5'), 'usd_value': FVal('5.1')},
            'ETH': {'amount': FVal('0.5'), 'usd_value': FVal('150')},
        }
    }
