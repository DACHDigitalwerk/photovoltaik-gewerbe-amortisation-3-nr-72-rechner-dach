"""CLI for pv_gewerbe_dach."""
import argparse
import json
from .calculator import simulate_pv_20y_comparison


def main() -> None:
    parser = argparse.ArgumentParser(description="DACH Gewerbe-PV ? 3 Nr. 72 EStG vs. ? 7g IAB/Sonder-AfA Calculator")
    parser.add_argument("--kwp", type=float, default=29.9, help="PV capacity in kWp")
    parser.add_argument("--capex", type=float, default=39795.0, help="Net CAPEX in EUR/CHF")
    parser.add_argument("--tax-rate", type=float, default=0.42, help="Marginal tax rate (0..0.60)")
    parser.add_argument("--units", type=int, default=1, help="Number of residential/commercial units")
    args = parser.parse_args()

    res = simulate_pv_20y_comparison(
        kwp=args.kwp,
        net_capex=args.capex,
        marginal_tax_rate=args.tax_rate,
        units=args.units,
    )
    print(json.dumps(res, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
