# Unit Economics

The purpose of this phase is to convert enthusiasm into arithmetic. Most ideas do not survive
contact with a break-even calculation, and the ones that do become much easier to argue about,
because a disagreement over a number is resolvable and a disagreement over a feeling is not.

Two rules govern everything here. Build **bottom-up**, never top-down. And label every input
`[sourced]`, `[derived]`, or `[assumed]` — the ratio of those tags is itself a finding.

## Inputs to gather

### Price
Anchored to phase 2 comparables in the *customer's* market, not the founder's aspiration. If no
comparable exists, that is a finding: this category may not have an established willingness to pay.
Record the price after fees, not before — gateway percentage, fixed per-transaction cost, currency
conversion, and platform commission all come out before the founder sees anything, and on a
low-priced product they can take 15–30%.

### Reachable customers
Built from the bottom: total entities that exist → those matching the segment → those reachable
through an actual channel → those who will plausibly convert. Each narrowing needs a reason. This
chain is where fantasy is eliminated, because a 40,000-person market usually turns out to be 600
people the founder can actually reach this year.

### Conversion rate
From the channel, not from optimism. Sane reference ranges when no local data exists — use them as
`[assumed]` and flag them:

| Motion | Typical range |
|---|---|
| Cold outreach → reply | 2–10% |
| Cold outreach → paying customer | 0.5–3% |
| Website visitor → free signup | 1–5% |
| Free signup → paid (self-serve) | 1–5% |
| Free trial (card required) → paid | 15–40% |
| Warm referral → paying customer | 20–50% |
| Marketplace listing view → order | 1–3% |

A model that only works at rates above these ranges is a model that only works if this founder
outperforms the industry, which is an assumption, not a plan.

### Churn
For anything recurring, this is the input founders most often set fantastically low. Monthly churn
of 3% is good SaaS; 5–7% is normal for small-business SMB tools; 10%+ means the average customer
lasts under a year and the acquisition cost must be recovered almost immediately. Consumer
subscriptions churn harder than B2B. If churn is unknown, model at 5% and 10% and show both — the
difference is usually startling.

### Customer acquisition cost (CAC)
Real channel prices in the real market: ads, commissions, marketplace fees, tools, anyone paid to
sell. **Cash only.** The founder's own hours do not go here — they are counted once, in the
opportunity-cost comparison below, and putting them in both places double-counts them.

This convention matters because the alternative distortion is just as common: founder time priced
at zero makes manual, unscalable acquisition look free. It is not free, and the opportunity-cost
section is where its true price appears. One place, not zero places and not two.

### Costs
- **Variable per customer**: hosting per user, support time, per-transaction costs, cost of goods.
- **Fixed monthly**: tools, subscriptions, infrastructure, anything paid regardless of volume.
- **One-time build**: upfront *cash* to recover — again, not the founder's unpaid hours.

### Opportunity cost and the goal
What the founder would earn doing something else with those hours. For a freelancer this is
concrete — their hourly rate times the hours the idea consumes. This number is what turns "it makes
$800/month" from a success into a question.

Pass `founder_goal_monthly` as well when the founder has stated a target, because the model then
checks something they almost never check themselves: **whether the same hours, billed at their
existing rate, already exceed the goal.** When they do, the idea is not the shortest route to the
money, and the honest framing is that it must be justified by ownership, leverage, independence,
or the possibility of growing past what hours can earn. That is a perfectly good reason to build
something. It is just a different reason than the one the founder started with, and they deserve
to choose it knowingly.

## Running the model

Use `scripts/unit_economics.py` rather than doing this in prose. Prose arithmetic in a document
nobody re-checks is where optimism hides, and the script also produces the sensitivity table, which
is usually the most valuable output.

Write a JSON config and run it:

```bash
python scripts/unit_economics.py config.json
python scripts/unit_economics.py config.json --markdown             # report-ready tables
python scripts/unit_economics.py config.json --opportunity-month 12 # compare at a chosen month
python scripts/unit_economics.py --example                          # sample config to copy
```

For a REFRAME verdict, write two configs and run both — the reframed model has to be costed, not
just described. See `verdict-and-report.md`.

It reports break-even volume and month, LTV, LTV/CAC, CAC payback period, a month-by-month
trajectory, the comparison against opportunity cost, and a one-at-a-time sensitivity table showing
which single assumption the outcome hangs on.

## Reading the output

**The two break-even numbers.** The script reports both, and the gap between them is the finding.

*Break-even customers* covers the fixed costs and nothing else. It is the number founders picture,
and for a subscription business it is too low, because it ignores that churned customers must be
continuously replaced at full acquisition cost.

*Sustaining customers* is the real requirement: the level at which contribution covers the fixed
costs **and** the monthly cost of replacing everyone who leaves. When it reports *unreachable*, the
replacement cost per customer has met or exceeded what each customer contributes, which means the
business cannot break even at any volume at all — growth makes the monthly loss larger. This is
counter-intuitive enough that founders read early traction as success while the hole deepens, so
say it plainly when it happens.

Compare the sustaining number to the reachable pool, not to the market size. If it requires 140
customers and the realistically reachable pool this year is 200, the idea needs 70% of everything
reachable just to stand still. Say that in exactly those terms.

**LTV/CAC.** Above 3 is healthy. Between 1 and 3 is fragile — it works only with patience and
capital. Below 1 means every customer acquired loses money, and growth accelerates the loss. This
last case deserves a blunt sentence, because it is counter-intuitive and founders often read early
traction as success while the hole deepens.

**CAC payback.** How many months until a customer has repaid what it cost to acquire them. Under
12 months is comfortable for a bootstrapped founder. Beyond 18 months the business requires
financing to grow, which changes what kind of idea this is.

**Time to break-even.** Compare against how long the founder can actually sustain it. An idea that
break-evens in month 26 is not viable for someone with nine months of savings, regardless of how
good it is. This is a fact about the founder, not the idea, and it belongs in the verdict.

**Sensitivity.** The variable with the widest swing is the one the experiment should test. If the
model survives at 6% conversion and dies at 3%, and comparables run at 1–2%, the audit has found
its answer and it is not a good one.

## The opportunity-cost comparison

Present it plainly, because it is the number that most often changes a founder's mind and it is
almost never shown to them:

> Month 12 net: $780/month `[derived]`
> Hours: ~25/week → ~108/month
> Effective rate: **$7.20/hour** `[derived]`
> Current freelance rate: **$28/hour** `[stated]`
>
> At month 12 this pays about a quarter of what the same hours earn freelancing. It becomes a
> better use of time only past roughly 95 customers, which at the modelled acquisition rate is
> month 29.

This is not an argument against the idea. Many people rationally accept a lower rate for equity in
something they own, for independence, or for the option value of a business that could grow. But
that is a decision, and it can only be made once the number is visible.

**Hours-limited or demand-limited?** Before using a rate as the alternative, establish that the
founder could actually bill those hours. A freelancer at a high rate with three unbilled days a
week does not have that alternative available — their real alternative for those hours is zero,
not rate × hours. Applied without this check, the comparison mechanically concludes that anyone
with a high rate should never build anything, which is a bias, not a finding. Use actual recent
monthly billings when the founder is demand-limited, and state in the report which basis the
comparison uses. Two sentences of framing here prevents the most common wrong conclusion this
model can produce.

## Common distortions to catch

**Free founder labour.** Sets the true cost of every manual process to zero and makes unscalable
acquisition look like a strategy.

**Top-down sizing.** "1% of a $2B market." Refuse it, and rebuild from the bottom.

**Churn optimism.** Assuming a 36-month customer lifetime in a category where nothing retains past
eight months.

**Gross revenue as income.** Payment fees, platform commission, taxes, refunds, and cost of goods
all come out first. Report net.

**Ignoring the ramp.** Customer 1 costs far more to acquire than customer 100. A model that assumes
steady-state CAC from month one understates the early hole, which is precisely the period the
founder must survive.

**One-time revenue modelled as recurring.** If the customer buys once, the business must keep
finding new customers forever, and the model needs the acquisition cost repeated every single time.

**Currency mismatch.** Costs in a hard currency and revenue in a soft one, modelled at today's
rate, in a market where the rate moves 30% a year.

## When the numbers cannot be built

Sometimes the inputs genuinely do not exist — a novel category with no comparables. Do not invent
a model and present it as analysis. Instead:

1. State which inputs are unknown, and that this is the actual finding.
2. Run the model backwards: **what would these inputs have to be for this to work?** Break-even at
   $X price requires N customers at C% conversion — is that plausible?
3. Make the cheapest experiment about discovering the single most important unknown input, usually
   price or conversion.

A model with every input tagged `[assumed]` is not a financial analysis. It is a list of things to
find out, and it should be labelled as one.
