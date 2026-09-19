# Idea Reality Check

**A Claude Skill that audits your idea instead of applauding it.**

Ask an AI assistant what it thinks of your business idea and you will usually get encouragement.
It restates the idea more eloquently than you did, suggests some features, adds a few generic
risks as a disclaimer, and you leave feeling validated. Months later you find out the thing nobody
told you: the payment rail you needed does not exist in your country, or the "market" was four
hundred people, or you would have had to sell nine units a day forever just to match what you
already earn freelancing.

This skill replaces that conversation with an adversarial audit.

---

## What it does

Six phases, in order:

| Phase | What happens |
|---|---|
| **1. Falsifiable restatement** | Your idea is compressed into one sentence that can be proven wrong, then broken into a ranked stack of assumptions |
| **2. Evidence** | Research into who already sells this, who tried and stopped, what people actually pay for, and how many customers genuinely exist |
| **3. Local market** | The idea is run through *your* country's payments, regulation, purchasing power, infrastructure, and channels — the part most analyses skip |
| **4. Arithmetic** | A bottom-up financial model: break-even, LTV/CAC, payback, 24-month trajectory, sensitivity, and the comparison against what your hours currently earn |
| **5. Verdict** | One of six graded outcomes, with kill criteria, what would have to be true to change it, and the cheapest experiment that could disprove the idea |
| **6. Self-audit** | The report is checked against a written anti-sycophancy checklist before you see it |

Every number carries an epistemic tag — `[sourced]`, `[derived]`, or `[assumed]` — so you can see
exactly which parts of the analysis are evidence and which are guesses. A report that is mostly
`[assumed]` says so at the top, because that is itself a finding.

## The six verdicts

**BUILD** — evidence supports it now · **NARROW** — real, but only for a specific segment ·
**TEST** — plausible, resting on one unverified assumption · **NOT-AS-A-BUSINESS** — worth making,
not as income · **REFRAME** — the insight is right, the business model is wrong ·
**STOP** — the evidence is against it in any executable form

`STOP` requires three concrete, sourced facts. "Most startups fail" is not one of them.

---

## Why local market reality is the core of this

A SaaS idea that works in the United States can be dead on arrival in Iran, Nigeria, Argentina, or
Indonesia — not because of the idea, but because of recurring billing, sanctions, purchasing power,
app store access, or the fact that the only real distribution channel is a messaging app the
founder's framework has never heard of.

Most validation advice was written in one country and assumes its conditions are universal. This
skill treats them as variables, and distinguishes clearly between a **risk** (reduces your odds)
and a **blocker** (ends the idea in its current form — and then looks for the version that routes
around it).

Country-specific annexes live in `references/locales/`. Iran ships with the skill. Contributions
for other markets are the most valuable thing you can add — see [CONTRIBUTING.md](CONTRIBUTING.md).

---

## Installation

**Quick install:** download the latest `.skill` file from
[Releases](https://github.com/blindmagnet/idea-reality-check/releases)
and add it in Claude → Settings → Capabilities → Skills.

**Claude Code / Claude Desktop**

```bash
git clone https://github.com/blindmagnet/idea-reality-check.git
cp -r idea-reality-check ~/.claude/skills/
```

**Claude.ai** — package it and upload:

```bash
cd idea-reality-check && zip -r ../idea-reality-check.skill .
```

Then add it from Settings → Capabilities → Skills.

The skill triggers on its own when you describe an idea and ask whether it is worth building,
whether anyone would pay, or what the competition looks like. You can also invoke it explicitly.

## Usage

Just describe the idea:

> I want to build a tool that lets physiotherapy clinics send automated appointment reminders over
> WhatsApp. I'm in Tehran, clinics here mostly use paper diaries. Is this worth building?

You will be asked two things — which market, and what you need the idea to earn — and then the
audit runs.

### Running the model directly

```bash
python scripts/unit_economics.py --example > config.json   # template to edit
python scripts/unit_economics.py config.json               # readable output
python scripts/unit_economics.py config.json --markdown    # report-ready tables
python scripts/unit_economics.py config.json --json        # machine-readable
```

No dependencies. Python 3.8+. It reports break-even volume and month, LTV/CAC, CAC payback, a
month-by-month trajectory, the opportunity-cost comparison in effective hourly rate, and a
sensitivity table showing which single assumption the outcome hangs on.

---

## Structure

```
idea-reality-check/
├── SKILL.md                              # the skill itself
├── references/
│   ├── assumption-stack.md               # decomposing an idea into ranked assumptions
│   ├── research-playbook.md              # what to search for, source quality, reading silence
│   ├── local-market-lens.md              # the eight-dimension local checklist
│   ├── unit-economics.md                 # model inputs, benchmark ranges, distortions to catch
│   ├── verdict-and-report.md             # verdict criteria and the report template
│   ├── anti-sycophancy.md                # the self-audit checklist
│   └── locales/
│       └── iran.md                       # country annex
└── scripts/
    └── unit_economics.py                 # the financial model
```

## What this is not

It is not a business plan writer, a pitch deck generator, or an investor memo tool. Those assume
the idea is already worth pursuing. This skill exists to find out whether it is.

It also does not pretend to certainty it does not have. Where evidence could not be found, the
report says so and tells you what to go check. The goal is not to be right about your idea — it is
to make sure that if it fails, it fails for a reason nobody could have told you in advance.

## License

MIT — see [LICENSE](LICENSE).

## Contributing

Locale annexes for new markets are the highest-value contribution. Improvements to the framework,
the benchmark ranges, or the anti-sycophancy checklist are equally welcome.
See [CONTRIBUTING.md](CONTRIBUTING.md).
