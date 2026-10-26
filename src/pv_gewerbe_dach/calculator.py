"""Core calculation engine for DACH commercial PV systems (? 3 Nr. 72 EStG vs. ? 7g EStG & ? 48 EEG)."""
from dataclasses import dataclass
from typing import Dict, Any


def check_section_3_nr_72_eligibility(kwp: float, units: int = 1, total_taxpayer_kwp: float | None = None) -> bool:
    """
    Checks whether a PV system in Germany qualifies for tax exemption under ? 3 Nr. 72 EStG (2026):
    - Max 30.0 kWp per residential/commercial unit
    - Max 100.0 kWp per taxpayer across all units
    """
    if kwp <= 0 or units < 1:
        raise ValueError("kwp must be > 0 and units >= 1")
    total_kwp = total_taxpayer_kwp if total_taxpayer_kwp is not None else kwp
    max_unit_limit = min(100.0, units * 30.0)
    return kwp <= max_unit_limit and total_kwp <= 100.0


def calculate_eeg_blended_tariff(kwp: float, full_feed_in: bool = False) -> float:
    """
    Calculates capacity-weighted EEG blended feed-in tariff in Ct/kWh (? 48 EEG up to 100 kWp).
    """
    if kwp <= 0:
        raise ValueError("kwp must be positive")
    tier1 = min(kwp, 10.0)
    tier2 = max(0.0, min(kwp - 10.0, 30.0))
    tier3 = max(0.0, kwp - 40.0)
    if full_feed_in:
        r1, r2, r3 = 12.47, 10.45, 10.45
    else:
        r1, r2, r3 = 7.86, 6.80, 5.56
    return round((tier1 * r1 + tier2 * r2 + tier3 * r3) / kwp, 4)


def calculate_section_7g_first_year_shield(
    net_capex: float,
    marginal_tax_rate: float,
    use_iab: bool = True,
    use_sonder_afa: bool = True,
) -> Dict[str, float]:
    """
    Computes ? 7g EStG depreciation and immediate tax shield through the end of Year 1:
    - 50% IAB (? 7g Abs. 1 EStG) in Year 0
    - 40% Sonder-AfA (? 7g Abs. 5 EStG) on remaining 50% basis (= 20% of CAPEX)
    - 5% linear AfA (? 7 Abs. 1 EStG) on remaining 50% basis (= 2.5% of CAPEX)
    Total Year 0+1 depreciation with full ? 7g = 72.5% of net_capex.
    """
    if net_capex <= 0:
        raise ValueError("net_capex must be > 0")
    if not (0.0 <= marginal_tax_rate <= 0.65):
        raise ValueError("marginal_tax_rate must be between 0.0 and 0.65")

    iab = net_capex * 0.50 if use_iab else 0.0
    rem_basis = net_capex - iab
    sonder_afa = rem_basis * 0.40 if use_sonder_afa else 0.0
    linear_afa_y1 = rem_basis * 0.05
    total_deduction_y0_y1 = iab + sonder_afa + linear_afa_y1
    pct_deducted = round((total_deduction_y0_y1 / net_capex) * 100.0, 2)
    tax_shield = round(total_deduction_y0_y1 * marginal_tax_rate, 2)

    return {
        "iab_amount": round(iab, 2),
        "sonder_afa_amount": round(sonder_afa, 2),
        "linear_afa_y1": round(linear_afa_y1, 2),
        "total_deduction_y0_y1": round(total_deduction_y0_y1, 2),
        "pct_deducted_y0_y1": pct_deducted,
        "tax_shield_y0_y1": tax_shield,
        "effective_net_equity_y1": round(net_capex - tax_shield, 2),
    }


def simulate_pv_20y_comparison(
    kwp: float,
    net_capex: float,
    spec_yield_kwh: float = 980.0,
    self_consumption_share: float = 0.62,
    grid_price_ct: float = 26.5,
    marginal_tax_rate: float = 0.42,
    units: int = 1,
    full_feed_in: bool = False,
    discount_rate: float = 0.04,
) -> Dict[str, Any]:
    """
    Runs a 20-year cashflow & NPV comparison between Regime A (? 3 Nr. 72 EStG tax-free)
    and Regime B (? 7g EStG taxable with 72.5% Y0/Y1 depreciation).
    """
    eligible_3_72 = check_section_3_nr_72_eligibility(kwp, units=units)
    feed_ct = calculate_eeg_blended_tariff(kwp, full_feed_in=full_feed_in)
    eff_self = 0.0 if full_feed_in else self_consumption_share
    opex_pa = net_capex * 0.012

    shield_info = calculate_section_7g_first_year_shield(net_capex, marginal_tax_rate, True, True)
    rem_basis = net_capex * 0.50
    book_after_y5 = rem_basis * 0.35  # 17.5% of net_capex spread over years 6..20

    cum_cf_a = -net_capex
    cum_cf_b = -net_capex + shield_info["iab_amount"] * marginal_tax_rate
    npv_a = -net_capex
    npv_b = cum_cf_b

    for y in range(1, 21):
        kwh = kwp * spec_yield_kwh * ((1.0 - 0.004) ** (y - 1))
        grid_eur = (grid_price_ct / 100.0) * ((1.022) ** (y - 1))
        ebitda = (kwh * eff_self * grid_eur) + (kwh * (1.0 - eff_self) * (feed_ct / 100.0)) - opex_pa

        if y == 1:
            afa_y = shield_info["sonder_afa_amount"] + shield_info["linear_afa_y1"]
        elif y <= 5:
            afa_y = shield_info["linear_afa_y1"]
        else:
            afa_y = book_after_y5 / 15.0

        tax_b = (ebitda - afa_y) * marginal_tax_rate
        cf_a = ebitda
        cf_b = ebitda - tax_b

        cum_cf_a += cf_a
        cum_cf_b += cf_b
        df = (1.0 + discount_rate) ** y
        npv_a += cf_a / df
        npv_b += cf_b / df

    return {
        "kwp": kwp,
        "eligible_3_nr_72": eligible_3_72,
        "eeg_blended_ct": feed_ct,
        "tax_shield_y0_y1": shield_info["tax_shield_y0_y1"],
        "cum_cf_20y_tax_free": round(cum_cf_a, 2),
        "cum_cf_20y_taxable_7g": round(cum_cf_b, 2),
        "npv_tax_free": round(npv_a, 2),
        "npv_taxable_7g": round(npv_b, 2),
    }
