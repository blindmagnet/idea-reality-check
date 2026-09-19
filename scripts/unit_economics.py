#!/usr/bin/env python3
"""
unit_economics.py — bottom-up viability model for the idea-reality-check skill.

Takes a JSON config of business assumptions and reports break-even, LTV/CAC,
CAC payback, a month-by-month trajectory, the comparison against the founder's
opportunity cost, and a one-at-a-time sensitivity table.

The sensitivity table is usually the most valuable output: it shows which single
assumption the whole model hangs on, which is what the founder's first experiment
should test.

Usage
-----
    python unit_economics.py config.json
    python unit_economics.py config.json --markdown          # report-ready tables
    python unit_economics.py config.json --months 36
    python unit_economics.py config.json --opportunity-month 12
    python unit_economics.py --example > config.json         # starting template

Founder time — one convention, to avoid counting the same hours twice
---------------------------------------------------------------------
Put the founder's hours in `founder_hours_per_month` ONLY. They are valued there
at `founder_alternative_hourly_rate` for the opportunity-cost comparison.

`cac` is out-of-pocket acquisition spend (ads, commissions, tools) — cash, not time.
`one_time_build_cost` is cash spent building — not the founder's unpaid hours.

If the founder pays someone else to acquire or to build, that IS cash and belongs in
those fields. Their own hours appear once, in the opportunity-cost section, which is
where the honest comparison lives.

No third-party dependencies. Python 3.8+.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, field
from typing import Dict, List, Optional

EXAMPLE_CONFIG: Dict = {
    "_comment": "All money in one currency. Label each input [sourced]/[derived]/[assumed] "
                "in the report; this file just holds the numbers.",
    "currency": "USD",
    "model_type": "subscription",              # "subscription" or "one_time"

    "price_per_period": 25.0,                  # charged per month (or per sale if one_time)
    "payment_fee_pct": 3.0,                    # gateway + platform commission, %
    "payment_fee_fixed": 0.10,                 # fixed fee per transaction

    "variable_cost_per_customer": 2.0,         # hosting/support/COGS per customer per month
    "fixed_costs_monthly": 120.0,              # tools, infra, anything volume-independent
    "one_time_build_cost": 1500.0,             # upfront CASH to recover (not founder hours)

    "cac": 40.0,                               # out-of-pocket acquisition spend per customer
                                               # — cash only; founder hours go below
    "monthly_churn_pct": 6.0,                  # ignored when model_type is one_time
    "new_customers_per_month": 6,              # realistic acquisition rate
    "acquisition_ramp_months": 3,              # months to reach that rate (linear ramp)

    "reachable_customers": 350,                # bottom-up ceiling on the addressable pool
    "founder_hours_per_month": 100.0,          # all founder time: building, selling, support
    "founder_alternative_hourly_rate": 28.0,   # what those hours earn elsewhere
    "founder_goal_monthly": None,              # target monthly income, if stated — the model
                                               # checks it against the opportunity cost

    "sensitivity": {                           # low/high bounds for one-at-a-time analysis
        "price_per_period": [15.0, 40.0],
        "cac": [20.0, 90.0],
        "monthly_churn_pct": [3.0, 12.0],
        "new_customers_per_month": [3, 12],
    },
}

REQUIRED = ["price_per_period", "fixed_costs_monthly", "cac"]


# --------------------------------------------------------------------------- #
# model
# --------------------------------------------------------------------------- #

@dataclass
class Result:
    currency: str
    model_type: str
    net_price: float
    contribution_per_customer: float
    lifetime_months: Optional[float]
    ltv: float
    ltv_cac: Optional[float]
    cac_payback_months: Optional[float]
    breakeven_customers: Optional[float]
    sustaining_customers: Optional[float]
    breakeven_month: Optional[int]
    full_recovery_month: Optional[int]
    reachable_customers: Optional[float]
    breakeven_share_of_reachable: Optional[float]
    trajectory: List[Dict] = field(default_factory=list)
    steady_state_customers: Optional[float] = None
    warnings: List[str] = field(default_factory=list)


def _net_price(cfg: Dict) -> float:
    gross = float(cfg["price_per_period"])
    fee_pct = float(cfg.get("payment_fee_pct", 0.0)) / 100.0
    fee_fixed = float(cfg.get("payment_fee_fixed", 0.0))
    return gross * (1 - fee_pct) - fee_fixed


def _acquisitions(cfg: Dict, month: int) -> float:
    """New customers acquired in a given month, respecting the ramp."""
    target = float(cfg.get("new_customers_per_month", 0))
    ramp = int(cfg.get("acquisition_ramp_months", 0) or 0)
    if ramp <= 0 or month > ramp:
        return target
    return target * month / ramp


def run_model(cfg: Dict, months: int = 24) -> Result:
    warnings: List[str] = []

    model_type = cfg.get("model_type", "subscription")
    recurring = model_type != "one_time"
    currency = cfg.get("currency", "USD")

    net_price = _net_price(cfg)
    var_cost = float(cfg.get("variable_cost_per_customer", 0.0))
    fixed = float(cfg.get("fixed_costs_monthly", 0.0))
    build = float(cfg.get("one_time_build_cost", 0.0))
    cac = float(cfg["cac"])
    churn = float(cfg.get("monthly_churn_pct", 0.0)) / 100.0
    reachable = cfg.get("reachable_customers")
    reachable = float(reachable) if reachable else None

    contribution = net_price - var_cost

    if net_price <= 0:
        warnings.append(
            "Net price is zero or negative after payment fees — the fee structure alone "
            "makes this price unworkable."
        )
    if contribution <= 0:
        warnings.append(
            "Contribution per customer is zero or negative: every customer served loses "
            "money before any fixed cost or acquisition spend. No volume fixes this."
        )

    # lifetime / LTV
    if recurring:
        if churn <= 0:
            warnings.append(
                "Churn is zero, which is not a real outcome. LTV is unbounded and every "
                "downstream ratio is meaningless — set a realistic churn rate."
            )
            lifetime = None
            ltv = float("inf") if contribution > 0 else contribution
        else:
            lifetime = 1.0 / churn
            ltv = contribution * lifetime
    else:
        lifetime = 1.0
        ltv = contribution

    ltv_cac = (ltv / cac) if cac > 0 and ltv not in (float("inf"),) else (
        float("inf") if cac == 0 else None
    )

    payback = (cac / contribution) if contribution > 0 else None
    if payback is not None and recurring and churn > 0 and lifetime and payback > lifetime:
        warnings.append(
            f"CAC payback ({payback:.1f} months) exceeds the average customer lifetime "
            f"({lifetime:.1f} months): customers leave before they have repaid what it "
            f"cost to acquire them. Growth makes the loss larger, not smaller."
        )

    # Two different break-even numbers, and the gap between them matters.
    #
    # "Naive" break-even ignores acquisition: contribution * N = fixed. It answers
    # "how many paying customers cover the fixed costs", which is the number founders
    # picture — but a subscription business must keep buying replacements for churned
    # customers forever, so it understates what is actually required to stand still.
    #
    # "Sustaining" break-even includes that treadmill: at N customers, churn removes
    # N*churn per month, each replacement costs CAC, so the real condition is
    #   contribution * N = fixed + N * churn * CAC
    # which has no solution at all when churn * CAC >= contribution — the business
    # cannot break even at ANY volume. That case is invisible in the naive number and
    # is exactly the trap this metric exists to expose.
    if contribution > 0:
        breakeven_customers = fixed / contribution
    else:
        breakeven_customers = None

    sustaining_customers: Optional[float] = None
    if recurring and contribution > 0:
        replacement_cost = churn * cac
        if replacement_cost >= contribution:
            warnings.append(
                f"Replacing churned customers costs {replacement_cost:,.2f} per customer "
                f"per month, which meets or exceeds the {contribution:,.2f} each one "
                f"contributes. The business cannot break even at any volume: every "
                f"customer added makes the monthly loss larger. Churn or CAC has to "
                f"change, not scale."
            )
        else:
            sustaining_customers = fixed / (contribution - replacement_cost)
            if breakeven_customers and sustaining_customers > breakeven_customers * 1.5:
                warnings.append(
                    f"Covering fixed costs takes {breakeven_customers:.0f} customers, but "
                    f"holding that level against churn takes {sustaining_customers:.0f} — "
                    f"the acquisition treadmill nearly doubles the real requirement."
                )
    elif not recurring and contribution > 0:
        # a one-time sale pays its own CAC out of its own contribution
        if cac >= contribution:
            warnings.append(
                f"Acquisition costs {cac:,.2f} per sale but each sale contributes only "
                f"{contribution:,.2f}. Every sale loses money; no volume fixes this."
            )
        else:
            sustaining_customers = fixed / (contribution - cac)
            # A one-time product must keep finding NEW buyers forever. The honest
            # question is not what share of the market it needs, but how long the
            # market lasts at the rate the model requires.
            if reachable and sustaining_customers > 0:
                supply_months = reachable / sustaining_customers
                if supply_months < months:
                    warnings.append(
                        f"At the {sustaining_customers:.1f} sales/month needed to break "
                        f"even, the reachable market of {reachable:,.0f} is exhausted in "
                        f"about {supply_months:.0f} months. A one-time product cannot "
                        f"resell to the same buyer, so revenue ends there unless the "
                        f"market replenishes or the product is repriced as recurring."
                    )

    be_share = None
    # Measure the share against the number actually required to stand still. When no
    # such number exists (the treadmill case above), report no share at all rather than
    # the naive one — a reassuring "0.6% of the market" printed beneath "cannot break
    # even at any volume" is worse than printing nothing.
    # Only meaningful for a subscription, where the requirement is a STOCK of customers
    # that can be compared against the pool. For one-time sales the requirement is a
    # monthly RATE, and dividing it by a lifetime pool compares two different units —
    # it produces a reassuringly small percentage that means nothing.
    unreachable = recurring and contribution > 0 and sustaining_customers is None
    share_basis = (None if (unreachable or not recurring)
                   else (sustaining_customers or breakeven_customers))
    if share_basis is not None and reachable:
        be_share = share_basis / reachable * 100.0
        if be_share > 100:
            warnings.append(
                f"Break-even requires {share_basis:.0f} customers but only "
                f"{reachable:.0f} are reachable — break-even is impossible within the "
                f"addressable market as modelled."
            )
        elif be_share > 30:
            warnings.append(
                f"Break-even requires {be_share:.0f}% of the entire reachable market. "
                f"Shares above roughly 30% are rarely achieved by a new entrant."
            )

    # trajectory
    trajectory: List[Dict] = []
    customers = 0.0
    ever_acquired = 0.0     # cumulative, so the market cap works for one-time sales too
    cumulative = -build
    breakeven_month: Optional[int] = None
    full_recovery_month: Optional[int] = None

    for m in range(1, months + 1):
        new = _acquisitions(cfg, m)
        if reachable:
            # a subscription can re-fill churned slots; a one-time sale cannot resell
            # to the same customer, so it is capped by everyone ever acquired
            consumed = customers if recurring else ever_acquired
            new = min(new, max(0.0, reachable - consumed))
        ever_acquired += new

        if recurring:
            churned = customers * churn
            customers = customers - churned + new
        else:
            customers = new  # one-time: only this month's buyers generate revenue

        revenue = customers * net_price
        variable = customers * var_cost
        acquisition = new * cac
        costs = variable + fixed + acquisition
        profit = revenue - costs
        cumulative += profit

        if breakeven_month is None and profit > 0:
            breakeven_month = m
        if full_recovery_month is None and cumulative > 0:
            full_recovery_month = m

        trajectory.append({
            "month": m,
            "new": round(new, 1),
            "customers": round(customers, 1),
            "revenue": round(revenue, 2),
            "costs": round(costs, 2),
            "profit": round(profit, 2),
            "cumulative": round(cumulative, 2),
        })

    steady = None
    if recurring and churn > 0:
        steady = float(cfg.get("new_customers_per_month", 0)) / churn
        if reachable:
            steady = min(steady, reachable)

    if breakeven_month is None:
        warnings.append(
            f"The business is never monthly-profitable within {months} months at these "
            f"assumptions."
        )
    if full_recovery_month is None and build > 0:
        warnings.append(
            f"The upfront investment of {build:,.0f} {currency} is not recovered within "
            f"{months} months."
        )

    return Result(
        currency=currency,
        model_type=model_type,
        net_price=net_price,
        contribution_per_customer=contribution,
        lifetime_months=lifetime,
        ltv=ltv,
        ltv_cac=ltv_cac,
        cac_payback_months=payback,
        breakeven_customers=breakeven_customers,
        sustaining_customers=sustaining_customers,
        breakeven_month=breakeven_month,
        full_recovery_month=full_recovery_month,
        reachable_customers=reachable,
        breakeven_share_of_reachable=be_share,
        trajectory=trajectory,
        steady_state_customers=steady,
        warnings=warnings,
    )


def opportunity_cost(cfg: Dict, res: Result, at_month: Optional[int] = None) -> Optional[Dict]:
    hours = cfg.get("founder_hours_per_month")
    rate = cfg.get("founder_alternative_hourly_rate")
    if not hours or rate is None:
        return None

    hours = float(hours)
    rate = float(rate)
    idx = (at_month or len(res.trajectory)) - 1
    if idx < 0 or idx >= len(res.trajectory):
        return None

    row = res.trajectory[idx]
    effective = row["profit"] / hours if hours else 0.0
    alternative = hours * rate

    # first month where the idea beats the alternative
    beats_month = next(
        (r["month"] for r in res.trajectory if r["profit"] >= alternative), None
    )

    out = {
        "month": row["month"],
        "monthly_profit": row["profit"],
        "hours_per_month": hours,
        "effective_hourly": effective,
        "alternative_hourly": rate,
        "alternative_monthly": alternative,
        "ratio": (effective / rate) if rate else None,
        "beats_alternative_month": beats_month,
        "goal_monthly": None,
        "goal_vs_alternative": None,
        "goal_note": None,
    }

    # The goal-versus-alternative check. Founders state a target income and an hourly
    # rate separately, and nobody puts them side by side — but when the same hours
    # billed at their existing rate already exceed the target, the idea is not the
    # shortest route to the goal, and that is worth knowing before year two rather
    # than after it. This is frequently the single most useful line in a report.
    goal = cfg.get("founder_goal_monthly")
    if goal:
        goal = float(goal)
        out["goal_monthly"] = goal
        out["goal_vs_alternative"] = alternative / goal if goal else None

        # Always report when the idea itself reaches the goal — it is needed whether or
        # not the alternative also clears it, and reporting only one of the two forces
        # the reader back into the trajectory table by hand.
        goal_month = next(
            (r["month"] for r in res.trajectory if r["profit"] >= goal), None)
        out["goal_reached_month"] = goal_month
        reached = (f"The idea itself reaches the goal in month {goal_month}."
                   if goal_month else
                   f"The idea itself never reaches the goal within the horizon; its best "
                   f"month is {max(r['profit'] for r in res.trajectory):,.0f}.")

        if alternative >= goal:
            out["goal_note"] = (
                f"These {hours:.0f} hours billed at the founder's existing rate earn "
                f"{alternative:,.0f} — {alternative / goal:.1f}× the stated goal of "
                f"{goal:,.0f}. {reached} If the founder is hours-limited (they could bill "
                f"every one of those hours today), the goal is already reachable without "
                f"this idea and it has to be justified by ownership, leverage, or growth "
                f"rather than income. If they are demand-limited — the hours exist but "
                f"the billable work does not — this comparison overstates the "
                f"alternative, and the relevant figure is what they actually bill, not "
                f"their rate. Establish which before drawing the conclusion."
            )
        else:
            out["goal_note"] = reached
    return out


def sensitivity(cfg: Dict, months: int, metric_month: int = 12) -> List[Dict]:
    """One-at-a-time: vary each parameter to its bounds, hold the rest, report the swing."""
    spec = cfg.get("sensitivity") or {}
    if not spec:
        return []

    # A misspelled parameter would otherwise be skipped in silence, quietly removing a
    # row from the table that decides what the founder tests first.
    for param, bounds in spec.items():
        if param not in cfg:
            print(f"warning: sensitivity parameter '{param}' is not a key in the config "
                  f"— skipped (typo?)", file=sys.stderr)
        elif not isinstance(bounds, (list, tuple)) or len(bounds) != 2:
            print(f"warning: sensitivity parameter '{param}' needs exactly two bounds "
                  f"[low, high] — skipped", file=sys.stderr)

    idx = min(metric_month, months) - 1

    def profit_at(c: Dict) -> Optional[float]:
        r = run_model(c, months)
        return r.trajectory[idx]["profit"] if idx < len(r.trajectory) else None

    base_cfg = {k: v for k, v in cfg.items()}
    base = profit_at(base_cfg)

    rows = []
    for param, bounds in spec.items():
        if param not in cfg or not isinstance(bounds, (list, tuple)) or len(bounds) != 2:
            continue
        low_cfg = dict(cfg); low_cfg[param] = bounds[0]
        high_cfg = dict(cfg); high_cfg[param] = bounds[1]
        low, high = profit_at(low_cfg), profit_at(high_cfg)
        if low is None or high is None:
            continue
        rows.append({
            "parameter": param,
            "base_value": cfg[param],
            "low_value": bounds[0],
            "high_value": bounds[1],
            "base_profit": round(base, 2) if base is not None else None,
            "low_profit": round(low, 2),
            "high_profit": round(high, 2),
            "swing": round(abs(high - low), 2),
            "flips_sign": (low < 0) != (high < 0),
        })

    rows.sort(key=lambda r: r["swing"], reverse=True)
    return rows


# --------------------------------------------------------------------------- #
# output
# --------------------------------------------------------------------------- #

def _fmt(v: Optional[float], cur: str = "", dp: int = 2) -> str:
    if v is None:
        return "—"
    if v == float("inf"):
        return "∞"
    return f"{v:,.{dp}f}{(' ' + cur) if cur else ''}"


def render(cfg: Dict, res: Result, opp: Optional[Dict], sens: List[Dict],
           months: int, markdown: bool, sens_month: int = 12) -> str:
    cur = res.currency
    recurring = res.model_type != "one_time"
    h1 = "## " if markdown else ""
    out: List[str] = []
    bar = "" if markdown else "=" * 66

    out.append(f"{h1}Unit economics — {res.model_type}" if markdown
               else f"\n{bar}\nUNIT ECONOMICS — {res.model_type.upper()}\n{bar}")

    # headline
    rows = [
        ("Net price per period (after fees)", _fmt(res.net_price, cur)),
        ("Contribution per customer", _fmt(res.contribution_per_customer, cur)),
        ("Avg customer lifetime", f"{res.lifetime_months:.1f} months"
            if res.lifetime_months else "—"),
        ("LTV", _fmt(res.ltv, cur)),
        ("LTV / CAC", _fmt(res.ltv_cac, "", 2)),
        ("CAC payback", f"{res.cac_payback_months:.1f} months"
            if res.cac_payback_months else "—"),
        # For one-time sales these are a RATE (sales per month), not a stock of customers.
        # Labelling them "customers" invites comparison against a lifetime market pool,
        # which is a category error that makes a doomed model look comfortable.
        (("Break-even sales per month (covers fixed costs)" if not recurring
          else "Break-even customers (covers fixed costs)"),
            _fmt(res.breakeven_customers, "", 0)),
        (("Sustaining sales per month (also covers CAC)" if not recurring
          else "Sustaining customers (also replaces churn)"),
            _fmt(res.sustaining_customers, "", 0) if res.sustaining_customers
            else ("unreachable — see warnings" if res.contribution_per_customer > 0 else "—")),
        ("Break-even month (monthly profit > 0)",
            str(res.breakeven_month) if res.breakeven_month else f"not within {months}"),
        ("Upfront cost recovered by month",
            str(res.full_recovery_month) if res.full_recovery_month else f"not within {months}"),
    ]
    if res.breakeven_share_of_reachable is not None:
        rows.append(("Sustaining level as share of reachable market",
                     f"{res.breakeven_share_of_reachable:.1f}%"))
    if res.steady_state_customers:
        rows.append(("Steady-state customers (acquisition = churn)",
                     _fmt(res.steady_state_customers, "", 0)))

    if markdown:
        out.append("\n| Metric | Value |\n|---|---|")
        out += [f"| {k} | {v} |" for k, v in rows]
    else:
        out.append("")
        out += [f"  {k:<42} {v}" for k, v in rows]

    # interpretation of LTV/CAC
    if res.ltv_cac not in (None, float("inf")):
        if res.ltv_cac < 1:
            verdict = "below 1 — every customer acquired loses money; growth deepens the hole"
        elif res.ltv_cac < 3:
            verdict = "between 1 and 3 — fragile; works only with patience or capital"
        else:
            verdict = "above 3 — healthy"
        line = (f"**LTV/CAC is {res.ltv_cac:.2f}**: {verdict}." if markdown
                else f"LTV/CAC is {res.ltv_cac:.2f}: {verdict}.")
        out.append(("\n> " if markdown else "\n  → ") + line)

    # trajectory
    out.append(("\n" + h1 + "Trajectory") if markdown else f"\n{bar}\nTRAJECTORY\n{bar}")
    shown = [r for r in res.trajectory
             if r["month"] <= 6 or r["month"] % 3 == 0 or r["month"] == months]
    if markdown:
        out.append("\n| Month | New | Customers | Revenue | Costs | Profit | Cumulative |")
        out.append("|---|---|---|---|---|---|---|")
        for r in shown:
            out.append(f"| {r['month']} | {r['new']:.1f} | {r['customers']:.1f} | "
                       f"{r['revenue']:,.0f} | {r['costs']:,.0f} | {r['profit']:,.0f} | "
                       f"{r['cumulative']:,.0f} |")
    else:
        out.append(f"\n  {'Mo':>3} {'New':>6} {'Cust':>8} {'Revenue':>11} "
                   f"{'Costs':>11} {'Profit':>11} {'Cumul.':>12}")
        for r in shown:
            out.append(f"  {r['month']:>3} {r['new']:>6.1f} {r['customers']:>8.1f} "
                       f"{r['revenue']:>11,.0f} {r['costs']:>11,.0f} "
                       f"{r['profit']:>11,.0f} {r['cumulative']:>12,.0f}")

    # opportunity cost
    if opp:
        out.append(("\n" + h1 + "Opportunity cost") if markdown
                   else f"\n{bar}\nOPPORTUNITY COST\n{bar}")
        lines = [
            f"Month {opp['month']} profit: {_fmt(opp['monthly_profit'], cur)}",
            f"Founder hours: {opp['hours_per_month']:.0f}/month",
            f"Effective rate: {_fmt(opp['effective_hourly'], cur)}/hour",
            f"Alternative rate: {_fmt(opp['alternative_hourly'], cur)}/hour "
            f"({_fmt(opp['alternative_monthly'], cur)}/month)",
        ]
        if opp["ratio"] is not None:
            lines.append(f"The idea pays {opp['ratio'] * 100:.0f}% of the alternative "
                         f"at month {opp['month']}.")
        lines.append(
            f"First month it beats the alternative: {opp['beats_alternative_month']}"
            if opp["beats_alternative_month"]
            else f"It never beats the alternative within {months} months."
        )
        out += [("- " if markdown else "  ") + l for l in lines]
        if opp.get("goal_note"):
            out.append(("\n> " if markdown else "\n  → ") + opp["goal_note"])

    # sensitivity
    if sens:
        out.append(("\n" + h1 + f"Sensitivity (month {sens_month} profit)") if markdown
                   else f"\n{bar}\nSENSITIVITY — MONTH {sens_month} PROFIT\n{bar}")
        if markdown:
            out.append("\n| Parameter | Low | → profit | High | → profit | Swing | Flips sign |")
            out.append("|---|---|---|---|---|---|---|")
            for s in sens:
                out.append(f"| {s['parameter']} | {s['low_value']} | {s['low_profit']:,.0f} | "
                           f"{s['high_value']} | {s['high_profit']:,.0f} | "
                           f"{s['swing']:,.0f} | {'yes' if s['flips_sign'] else 'no'} |")
        else:
            out.append(f"\n  {'Parameter':<28}{'low→profit':>16}{'high→profit':>16}"
                       f"{'swing':>12}")
            for s in sens:
                flag = "  *flips sign*" if s["flips_sign"] else ""
                out.append(f"  {s['parameter']:<28}"
                           f"{s['low_value']!s:>6}→{s['low_profit']:>9,.0f}"
                           f"{s['high_value']!s:>6}→{s['high_profit']:>9,.0f}"
                           f"{s['swing']:>12,.0f}{flag}")
        top = sens[0]
        line = (f"The model is most sensitive to **{top['parameter']}**"
                if markdown else
                f"The model is most sensitive to {top['parameter']}")
        line += " — this is what the first experiment should test."
        out.append(("\n> " if markdown else "\n  → ") + line)
        flippers = [s["parameter"] for s in sens if s["flips_sign"]]
        if flippers:
            out.append(("> " if markdown else "  → ") +
                       f"Profit changes sign within the tested range for: "
                       f"{', '.join(flippers)}. The outcome is not robust to these.")

    if res.warnings:
        out.append(("\n" + h1 + "Warnings") if markdown else f"\n{bar}\nWARNINGS\n{bar}")
        out += [("- " if markdown else "  ! ") + w for w in res.warnings]

    out.append("\nEvery figure above inherits the epistemic tag of the input that produced it. "
               "Label them [sourced]/[derived]/[assumed] in the report." if markdown
               else "\n  Note: every figure inherits the tag of its input. Label them\n"
                    "  [sourced]/[derived]/[assumed] in the report.\n")
    return "\n".join(out)


def main() -> int:
    p = argparse.ArgumentParser(
        description="Bottom-up unit economics model for idea validation.")
    p.add_argument("config", nargs="?", help="path to JSON config ('-' for stdin)")
    p.add_argument("--months", type=int, default=24, help="trajectory horizon (default 24)")
    p.add_argument("--opportunity-month", type=int, default=None, metavar="N",
                   help="month at which to compare against the founder's alternative "
                        "(default: the last month of the horizon)")
    p.add_argument("--sensitivity-month", type=int, default=12, metavar="N",
                   help="month whose profit the sensitivity table varies (default 12)")
    p.add_argument("--markdown", action="store_true", help="markdown tables for the report")
    p.add_argument("--json", action="store_true", help="raw JSON output")
    p.add_argument("--example", action="store_true", help="print a template config and exit")
    args = p.parse_args()

    if args.example:
        print(json.dumps(EXAMPLE_CONFIG, indent=2, ensure_ascii=False))
        return 0

    if not args.config:
        p.error("a config file is required (or use --example to print a template)")

    try:
        raw = sys.stdin.read() if args.config == "-" else open(
            args.config, encoding="utf-8").read()
        cfg = json.loads(raw)
    except FileNotFoundError:
        print(f"error: config file not found: {args.config}", file=sys.stderr)
        return 1
    except json.JSONDecodeError as e:
        print(f"error: config is not valid JSON — {e}", file=sys.stderr)
        return 1

    missing = [k for k in REQUIRED if k not in cfg]
    if missing:
        print(f"error: config is missing required keys: {', '.join(missing)}\n"
              f"run with --example to see a complete template", file=sys.stderr)
        return 1

    res = run_model(cfg, args.months)
    opp = opportunity_cost(cfg, res, args.opportunity_month)
    sens = sensitivity(cfg, args.months, args.sensitivity_month)

    if args.json:
        print(json.dumps({
            "summary": {
                "currency": res.currency,
                "model_type": res.model_type,
                "net_price": res.net_price,
                "contribution_per_customer": res.contribution_per_customer,
                "lifetime_months": res.lifetime_months,
                "ltv": None if res.ltv == float("inf") else res.ltv,
                "ltv_cac": None if res.ltv_cac == float("inf") else res.ltv_cac,
                "cac_payback_months": res.cac_payback_months,
                "breakeven_customers": res.breakeven_customers,
                "sustaining_customers": res.sustaining_customers,
                "breakeven_month": res.breakeven_month,
                "full_recovery_month": res.full_recovery_month,
                "breakeven_share_of_reachable_pct": res.breakeven_share_of_reachable,
                "steady_state_customers": res.steady_state_customers,
            },
            "trajectory": res.trajectory,
            "opportunity_cost": opp,
            "sensitivity": sens,
            "warnings": res.warnings,
        }, indent=2, ensure_ascii=False))
        return 0

    print(render(cfg, res, opp, sens, args.months, args.markdown,
                 args.sensitivity_month))
    return 0


if __name__ == "__main__":
    sys.exit(main())
