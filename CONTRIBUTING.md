# Contributing

The most valuable contribution to this project is a **locale annex** for a market that does not
have one. Everything else in the skill is reasoning that transfers between countries; the locale
files are the part that cannot be reasoned out from a distance and has to come from someone who
has actually tried to get paid there.

## Adding a locale annex

Create `references/locales/<country>.md`. The Iran annex (`references/locales/iran.md`) is the
reference implementation — match its structure.

### What belongs in one

Write the things a competent outside analyst would get *wrong*, not the things they would get
right. A locale annex is a correction file, not a country profile. If a fact is true nearly
everywhere, it belongs in `local-market-lens.md` instead.

Cover, at minimum:

**Payments** — can a small business take money here, and how? Card penetration, dominant methods,
whether a solo founder can get a gateway, what it requires, what it costs. Most importantly:
**does recurring billing exist, and is it available to an individual or small business?** This
single question decides more subscription ideas than anything else.

**Receiving from abroad** — if the market has restrictions on inbound international payments, say
what actually works and what it costs. Do not recommend anything of questionable legality; state
the constraint and let the founder resolve it.

**Purchasing power and price anchors** — what does the target customer earn, and what do local
products in this category actually charge? A founder pricing against a US comparable will be wrong
by an order of magnitude and needs to know it.

**Regulation** — registration requirements, licensing for common sectors, trust marks, tax
thresholds, data rules. Be specific about what a solo founder can and cannot do without a company.

**Infrastructure and platform access** — cloud availability, app store access, whether foreign
APIs are reachable and payable, connectivity, outage risk.

**Channels that actually work** — the local platforms, marketplaces, ad networks, directories, and
offline routes. This is where generic advice fails hardest: naming the three channels that really
carry commerce in your market is enormously useful.

**Cultural and behavioural defaults** — prepayment trust, subscription habits, decision structures,
seasonality and the local business calendar.

**The structural advantage** — every market has one. Say what it is, because reports about that
market should mention it.

Close with a **checklist** — the numbered questions an auditor should ask about any idea in that
market. This is the part that gets used most.

### Rules for locale content

- **Date it.** Put `Last reviewed: YYYY-MM` at the top. These facts decay.
- **Say what is verifiable and what is not.** "Verify with the provider's current documentation"
  is a legitimate and useful instruction. Confident invention is not.
- **Describe, don't advise.** State what the constraints are and what routes exist. Do not
  recommend circumventing sanctions, tax obligations, or licensing.
- **Write it for an auditor, not a tourist.** No history, no general economic background, no
  cultural essay. Only what changes a verdict.
- **Note what you could not confirm.** A gap you flag is more useful than a gap you fill with a
  guess.

## Improving the framework

Changes to `SKILL.md` and the reference files are welcome. Two things to keep in mind:

**Explain why, not just what.** The skill is written to give a capable model the reasoning behind
each instruction, because that generalises to cases the instructions never anticipated. Rigid rules
in capital letters do not. If you find yourself writing `ALWAYS` or `NEVER`, try explaining the
consequence instead.

**Keep the bias in mind.** Everything here exists to counteract a specific pull toward
encouragement. A change that makes the skill more agreeable, more hedged, or more balanced for the
sake of balance is moving against the point. So is a change that makes it harsh for its own sake —
`anti-sycophancy.md` covers both failure modes, and contributions should respect that symmetry.

## Improving the model

`scripts/unit_economics.py` has no dependencies and should keep it that way, so that it runs
anywhere Python does. If you add a metric, add it to the JSON output as well as the readable
output, and add a corresponding note to `references/unit-economics.md` explaining how to read it —
a number nobody knows how to interpret makes reports worse, not better.

Benchmark ranges in `unit-economics.md` (conversion rates, churn norms) are deliberately broad and
labelled as rules of thumb. If you have better data for a specific category or market, contributing
it with a source is genuinely valuable.

## Testing a change

There is no automated test suite for the reasoning. The practical test:

1. Take three real ideas — one you believe is good, one you believe is bad, one you are unsure
   about.
2. Run the skill on each, before and after your change.
3. Check whether the verdicts became *more accurate*, not merely more positive or more negative.

For `unit_economics.py`, run `--example` through the model and verify the edge cases still behave:
zero churn, negative contribution, a market cap smaller than break-even, and the one-time model.

## Pull requests

Keep them focused — one locale, or one framework change. In the description, say what problem the
change solves and, for locale annexes, how you know the facts (lived experience, provider
documentation, direct verification). That provenance is what makes the file trustworthy to someone
auditing an idea in a country they have never been to.
