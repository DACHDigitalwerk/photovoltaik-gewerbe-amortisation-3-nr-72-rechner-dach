import pytest
from pv_gewerbe_dach import (
    calculate_eeg_blended_tariff,
    calculate_section_7g_first_year_shield,
    check_section_3_nr_72_eligibility,
    simulate_pv_20y_comparison,
)


def test_eligibility_single_unit_under_30kwp():
    assert check_section_3_nr_72_eligibility(29.9, units=1) is True
    assert check_section_3_nr_72_eligibility(30.0, units=1) is True


def test_eligibility_single_unit_over_30kwp():
    assert check_section_3_nr_72_eligibility(30.1, units=1) is False


def test_eligibility_multi_unit_up_to_100kwp():
    assert check_section_3_nr_72_eligibility(85.0, units=3) is True
    assert check_section_3_nr_72_eligibility(95.0, units=3) is False
    assert check_section_3_nr_72_eligibility(105.0, units=4) is False


def test_eeg_blended_tariff_partial_feed_in():
    assert calculate_eeg_blended_tariff(10.0, full_feed_in=False) == pytest.approx(7.86, rel=1e-3)
    # 40 kWp: (10*7.86 + 30*6.80)/40 = 282.6 / 40 = 7.065
    assert calculate_eeg_blended_tariff(40.0, full_feed_in=False) == pytest.approx(7.065, rel=1e-3)


def test_eeg_blended_tariff_full_feed_in():
    assert calculate_eeg_blended_tariff(10.0, full_feed_in=True) == pytest.approx(12.47, rel=1e-3)
    assert calculate_eeg_blended_tariff(50.0, full_feed_in=True) > calculate_eeg_blended_tariff(50.0, full_feed_in=False)


def test_section_7g_72_5_percent_first_year_deduction():
    res = calculate_section_7g_first_year_shield(100000.0, marginal_tax_rate=0.42, use_iab=True, use_sonder_afa=True)
    assert res["pct_deducted_y0_y1"] == pytest.approx(72.5, rel=1e-3)
    assert res["total_deduction_y0_y1"] == pytest.approx(72500.0, rel=1e-3)
    assert res["tax_shield_y0_y1"] == pytest.approx(30450.0, rel=1e-3)


def test_section_7g_sonder_afa_only_without_iab():
    res = calculate_section_7g_first_year_shield(100000.0, marginal_tax_rate=0.40, use_iab=False, use_sonder_afa=True)
    assert res["pct_deducted_y0_y1"] == pytest.approx(45.0, rel=1e-3)
    assert res["tax_shield_y0_y1"] == pytest.approx(18000.0, rel=1e-3)


def test_simulate_20y_comparison_29_9_kwp():
    sim = simulate_pv_20y_comparison(kwp=29.9, net_capex=39795.0, marginal_tax_rate=0.42, units=1)
    assert sim["eligible_3_nr_72"] is True
    assert sim["cum_cf_20y_tax_free"] > sim["cum_cf_20y_taxable_7g"]


def test_simulate_20y_comparison_85_kwp():
    sim = simulate_pv_20y_comparison(kwp=85.0, net_capex=101000.0, marginal_tax_rate=0.44, units=1)
    assert sim["eligible_3_nr_72"] is False
    assert sim["tax_shield_y0_y1"] > 30000.0


def test_invalid_inputs_raise_value_error():
    with pytest.raises(ValueError):
        check_section_3_nr_72_eligibility(0.0, units=1)
    with pytest.raises(ValueError):
        calculate_section_7g_first_year_shield(-5000.0, 0.42)
