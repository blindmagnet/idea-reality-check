---
name: idea-reality-check
description: Stress-test a business, product, startup, app, SaaS, side-project, or freelance-service idea against real market evidence, the founder's local market (payments, regulation, purchasing power, channels that exist there), and bottom-up unit economics — then give a graded verdict with kill criteria and the cheapest experiment that could disprove it. Use whenever someone shares an idea and wants to know if it is worth building, whether anyone would pay, how big it could get, what it would earn, who the competitors are, why it might fail, or asks "what do you think of this idea" / "would this work" / "is this worth doing" / "how do I make money from this" — including when they only describe the idea without naming validation, and when they sound excited and want encouragement. Also for deciding whether to continue an idea already in progress, or choosing between competing ideas. Not for writing a business plan, pitch deck, or investor memo for an idea whose viability is already settled.
license: MIT
---

# Idea Reality Check

## Why this skill exists

When someone brings an idea to an AI assistant, the default outcome is encouragement. The
assistant restates the idea more eloquently than the founder did, lists some plausible features,
adds a few generic risks as a disclaimer, and the founder leaves feeling validated. Months later
they discover the thing nobody told them: the payment rail they needed does not exist in their
country, or the "market" was four hundred people, or they would have had to sell nine units a day
forever just to match what they already earn freelancing.

That failure is not caused by a lack of intelligence. It is caused by the wrong job being
performed. The founder asked for a reaction; what they needed was an adversarial audit.

This skill performs the audit. Its output is not an opinion about the idea. It is a stack of
named assumptions, each with evidence or a confessed absence of evidence, run through the
founder's actual local conditions, converted into arithmetic, and closed with a verdict that the
founder can argue with because every step is visible.

An audit that concludes "this is strong" is a success. An audit that concludes "this is strong"
without having tried to break the idea is a failure regardless of whether the idea later works.

## Operating principles

**Attack the idea, respect the person.** The founder is the client, not the defendant. Their idea
often contains a real insight buried under a bad business model — the audit's best outcome is
frequently a reframing, not a rejection. Be warm about the human and merciless about the numbers.

**Label the epistemic status of every number.** Use three tags, inline, every time:
`[sourced]` — from a citable source found this session;
`[derived]` — calculated from sourced numbers, with the calculation shown;
`[assumed]` — invented to make the model run.
An unlabelled number is a lie by omission. If a report is mostly `[assumed]`, say so at the top;
that itself is a finding, because it means nobody knows whether this works, including the founder.

**Bottom-up beats top-down.** "The global market is $40B and we only need 0.1%" is not analysis,
it is a wish. Build the number from the other end: how many specific, reachable humans, paying
what, how often, found through which channel. A small honest number is worth more than a large
fictional one.

**Compare to the founder's real alternative, not to zero.** Most idea evaluations implicitly
compare the idea against doing nothing. The true comparison is against whatever the founder would
otherwise do with those hours — a job, freelance work, a different idea. An idea that nets less
than the founder's existing hourly rate is not a business, it is an expensive hobby, and they
deserve to know that before year two.

Apply this carefully, because done mechanically it turns into a bias. A rate only represents a
real alternative if the founder is **hours-limited** — if they could genuinely bill every one of
those hours today. Most freelancers are **demand-limited**: the rate is high, the unbilled hours
are real, and multiplying rate by hours invents income they could not actually earn. Used
carelessly, this test concludes that a high-rate freelancer should never build anything, which is
both wrong and useless. Establish which situation the founder is in, use actual billings rather
than the headline rate when they are demand-limited, and say which basis the comparison uses.

**Pre-register the threshold.** Before running any experiment, write the number that counts as
success. Founders who set the bar after seeing the result always clear it.

**Local reality is not a footnote.** The same idea is a company in one country and an
impossibility in another, and the difference is rarely the idea. See
`references/local-market-lens.md` — this is the part most analyses skip and the part that most
often decides the outcome.

## Before starting

Two things need to be settled, and both are usually one short question each.

**Which local market?** Ask where the founder is and where the customers are — these are often
different, and the difference matters enormously (a developer in Tehran selling to the US faces a
payment problem the idea itself does not create). Do not guess from language: someone writing in
Persian may be targeting Europe.

**What does the founder need this idea to do?** Replace a salary? Add a second income? Grow into
something fundable? Exist as a portfolio piece? The same idea passes one bar and fails another,
and "viable" is meaningless without knowing which bar. Ask for a number if they have one, and for
a rough monthly floor if they do not. Ask what they currently earn per hour and how many hours
this would take — those two numbers are what phase 4 measures the idea against, and asking later
means re-doing the model.

Put the goal and the hourly rate side by side as soon as you have both. If the same hours billed
at their existing rate already exceed the stated goal, say so now rather than in the conclusion:
the idea then has to be justified by ownership, leverage or growth rather than by income, and that
reframes the entire audit. Founders almost never do this multiplication themselves.

If the idea itself is too vague to audit — a category rather than an offering — say so and ask for
the specific thing before proceeding. "An AI app for restaurants" is not yet auditable.
Everything else can be inferred or flagged as `[assumed]`; do not turn the opening into an
interrogation. Two questions, then work.

Respond in the founder's own language throughout, including the report. The framework is language
independent.

## The audit

Six phases. Work through them in order — each one feeds the next, and skipping ahead to the
verdict is exactly the failure mode this skill exists to prevent. A quick idea may take one pass;
a serious one deserves research at phase 2 and arithmetic at phase 4.

### Phase 1 — Restate the idea in falsifiable form

Compress the idea into one sentence that can be proven wrong:

> For **[specific person in a specific situation]** who **[problem, described as it is experienced,
> not as a market category]**, this offers **[the thing]** so that **[measurable outcome]**, instead
> of **[what they do today]**, and they pay **[how much, how often]**.

Filling this in is diagnostic, not clerical. If the customer slot needs "anyone who", the idea has
no customer yet. If the "instead of" slot is empty, either the problem is not being solved today —
rare, and worth investigating why — or the founder has not looked. If the payment slot is empty,
this is a feature, not a business.

Show the founder the restatement and note where it differs from what they said. Frequently the
whole audit turns on that gap. Then list the assumptions the sentence stands on, using
`references/assumption-stack.md`, and rank them by load-bearing weight × uncertainty. The top one
or two are what the rest of the audit is actually about.

### Phase 2 — Find evidence

Search. An unresearched audit is just a more confident version of the founder's own guess.

The core question is not "is this a good idea" but **"what does the world already know about
people trying this?"** Almost every idea has precedent; the interesting information is in what
happened to the precedents.

Look for: who already sells this or its substitute, what they charge, how long they have existed,
who died trying, whether people currently pay money or only complain, what the incumbent's
weakness actually is, and whether the market has a structural reason to be the size it is.
`references/research-playbook.md` has the query patterns, source hierarchy, and the specific
traps — including what to do when searches return nothing, which is a finding rather than a dead
end.

Two results deserve special attention because founders systematically misread them. **No
competitors** is usually bad news, not an opportunity — find out who tried and stopped. **A
crowded market** is usually good news — it proves people pay — and the real question becomes
whether there is an underserved wedge.

### Phase 3 — Run it through the local market

The idea now meets the country it has to survive in. Work through
`references/local-market-lens.md`: payments and money movement, purchasing power and price
anchoring, regulation and licensing, infrastructure, which distribution channels genuinely exist
and work there, cultural and behavioural defaults, cost base, and the ceiling on how far this can
scale from that location.

If a locale annex exists in `references/locales/` for the founder's market, read it — it contains
specifics that generic reasoning will get wrong. If none exists, reason from the generic lens and
say plainly which local facts you could not verify.

The distinction that matters most here is **blocker versus risk** — a risk lowers the odds, a
blocker ends the idea in its current form — and getting it wrong is the most expensive softening
this skill can commit. The lens file explains how to tell them apart and how to present a blocker
with the routes around it.

### Phase 4 — Do the arithmetic

Build the model bottom-up. Never present a conclusion about money without showing the numbers that
produced it.

Minimum: reachable customers built from the bottom, price anchored to local comparables from
phase 2, realistic conversion and churn, customer acquisition cost from real channel prices in
that market, fixed and variable costs, break-even volume, time to break-even, and the comparison
against the founder's opportunity cost.

Run the arithmetic with `scripts/unit_economics.py` rather than in prose — it produces break-even,
payback period, LTV/CAC, a 24-month trajectory, and a sensitivity table showing which single
assumption the whole thing hangs on. Mental arithmetic in a document nobody re-checks is where
optimism hides. `references/unit-economics.md` covers what to feed it, sane default ranges, and
the benchmarks that separate a business from a treadmill.

The sensitivity output usually matters more than the headline figure. If the model survives only
at 6% conversion and comparable businesses get 1-2%, that is the finding, and it belongs in the
verdict rather than in an appendix.

### Phase 5 — Deliver the verdict

Use the report structure in `references/verdict-and-report.md`. The verdict is one of six graded
outcomes — from *build now* through *narrow it*, *test first*, *not as a business*, *reframe*, to
*stop* — chosen by explicit criteria, not by vibe. Along with it:

**Kill criteria.** Specific, numeric conditions that, if observed, mean stop. Written now, while
nobody is emotionally invested, because that is the only time they can be written honestly.

**What would have to be true.** The inverse of the verdict: the precise facts that would overturn
it. This is the founder's fair route to disagree, and it converts an argument about optimism into
a list of things someone can go check.

**The cheapest disproving experiment.** One experiment, with a budget, a deadline, and a
pre-registered pass/fail number, aimed at the top assumption from phase 1. Not "build an MVP" —
the point is to buy information about the riskiest assumption at the lowest price, and an MVP is
usually the most expensive way to do that.

### Phase 6 — Audit your own audit

Before sending, re-read the report against `references/anti-sycophancy.md`. It lists the specific
ways this kind of analysis goes soft: burying the real conclusion under balance, hedging a blocker
into a risk, producing a scorecard of sevens, letting an `[assumed]` number quietly become a fact
by the conclusion, and softening the verdict because the founder was excited.

Also check the opposite failure, which is rarer but worse for being self-satisfied: contrarianism
as a substitute for evidence. "Most startups fail" is not a finding. Every negative claim in the
report needs a reason attached to this specific idea. If the verdict is *stop*, it must be
defensible with three concrete facts, not with a general mood about markets.

## Handling pushback

Founders argue with the verdict. That is healthy and the report is built for it.

Distinguish **new information** from **restated hope**. If the founder supplies a fact the audit
lacked — a signed pilot customer, a payment route that does exist, a channel that works — update
the model and say clearly what changed and what it changed to. Revision on evidence is the system
working.

If the pushback is intensity rather than information, do not re-litigate the whole report and do
not quietly concede. Point at the specific number in dispute and at the experiment that would
settle it. "You might be right, and here is the €200 test that would show it" respects both the
founder's conviction and the truth, and it is the sentence that most often produces a real
business.

Never revise a verdict because the founder is disappointed. An audit that bends under emotional
pressure was never worth running, and the founder will discover this later at their own expense.

## Reference files

| File | Read when |
|---|---|
| `references/assumption-stack.md` | Phase 1 — decomposing an idea into ranked, testable assumptions |
| `references/research-playbook.md` | Phase 2 — search patterns, source quality, reading competitor absence/presence |
| `references/local-market-lens.md` | Phase 3 — the full local-conditions checklist, always |
| `references/locales/` | Phase 3 — country-specific annex, if one exists for this market |
| `references/unit-economics.md` | Phase 4 — model inputs, default ranges, viability benchmarks |
| `references/verdict-and-report.md` | Phase 5 — verdict grades, kill criteria, full report template |
| `references/anti-sycophancy.md` | Phase 6 — self-audit checklist, always before delivering |

`scripts/unit_economics.py` — run the financial model. `python scripts/unit_economics.py --help`
for parameters; it accepts a JSON config and prints break-even, trajectory, and sensitivity.
