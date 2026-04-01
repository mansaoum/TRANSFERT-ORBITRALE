import pytest
from transfert_hohmann import hohmann_dv, simulate_leo_to_geo, tsiolkovsky, R_earth


def test_hohmann_dv_values():
    r_leo = R_earth + 500e3
    r_geo = R_earth + 35786e3

    params = hohmann_dv(r_leo, r_geo)

    assert pytest.approx(params['dv_total'], rel=1e-2) == 3840  # ~3,84 km/s
    assert params['dv1'] > 0
    assert params['dv2'] > 0
    assert pytest.approx(params['t_transfer']/3600, rel=0.03) == 5.0  # ~5 h


def test_tsiolkovsky_mass():
    mi = 2000
    params = hohmann_dv(R_earth + 500e3, R_earth + 35786e3)
    mf, mfuel = tsiolkovsky(mi, params['dv_total'])

    assert 700 < mfuel < 1100
    assert mf < mi


def test_simulation_finish_close_to_geo():
    r_leo = R_earth + 500e3
    r_geo = R_earth + 35786e3

    result = simulate_leo_to_geo(r_leo, r_geo, dt=30.0)

    assert pytest.approx(result['r_final']/1000, rel=0.02) == 42164
    assert abs(result['v_final'] - (params := hohmann_dv(r_leo, r_geo))['v2']) < 200
    assert abs(result['dv2_applied'] - params['dv2']) < 250
