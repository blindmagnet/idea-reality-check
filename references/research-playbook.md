# Research Playbook

An unresearched audit is the founder's own guess wearing a suit. This phase exists to replace
opinion with evidence — and, where evidence cannot be found, to say so loudly enough that the
absence itself becomes a finding.

The governing question is not *"is this a good idea?"* It is **"what does the world already know
about people who tried this?"** Almost every idea has precedent. The precedents are the data.

## What to search for, in order

Work down this list. Stop early if the first two answer the question decisively — a blocker found
in the first ten minutes saves the rest of the audit.

### 1. The direct competitors
Who sells this exact thing today? For each: what they charge, what tier structure, how long they
have existed, roughly how big they appear to be, and which customer they actually serve.

Pricing pages are the single highest-value page on the internet for this work. They reveal the
real price anchor, the real segmentation, and often the real customer (an "Enterprise: contact
us" tier means the money is elsewhere than the founder assumes).

### 2. The substitutes — what people use instead
Usually more important than the direct competitors, and usually missed. The true competitor to a
scheduling product is a notebook; to an analytics product, a spreadsheet; to a marketplace, a
Telegram group. Substitutes are free, entrenched, and good enough, which is why displacing them
requires far more than being better.

Find the substitute by asking what the person does today, then searching for how people currently
handle this problem — forum threads, "how do you manage X" questions, template downloads.

### 3. The graveyard
Who tried this and stopped? Shutdown posts, abandoned repositories, dead domains, "we're winding
down" blog entries, acquisition-for-talent stories. Failed attempts are more informative than
successful ones because founders write honestly on the way out.

Useful queries: the product category plus *shutting down*, *post-mortem*, *why we failed*,
*lessons learned*; the category on a startup-failure list; a domain that redirects nowhere.

### 4. Demand evidence
Distinguish **complaint** from **spending**.

Complaint evidence: forum posts, social threads, review-site one-stars, "I wish someone would
build" comments. Cheap to find, weak as evidence — people complain about things they will never
pay to fix.

Spending evidence: existing paid products with visible traction, search volume on commercial-
intent keywords, active ad campaigns from competitors (someone is paying to acquire this customer,
so the customer has value), agencies or freelancers already charging for the manual version,
procurement or tender listings, job postings for the role the product would replace.

A market where competitors buy ads is a market with money in it. A market where everyone
complains and nobody sells is usually a market where the pain is real and the budget is not.

### 5. Market size, bottom-up
Not the analyst report. Count the actual entities: how many clinics, shops, agencies, developers,
households of the right type exist in the served geography. Directories, trade-association member
lists, registries, marketplace vendor counts, open datasets, government statistics.

If the count is 300 and the price is $20/month, the entire market is $72k/year at 100% penetration.
That calculation, done early, ends a surprising number of audits and saves a surprising number of
months.

### 6. Trend direction
Is this getting easier or harder? Regulation tightening or loosening, a platform closing its API,
a big player entering the space, a technology shift making the whole category free. An idea that
was excellent three years ago may now be a commodity feature of a tool the customer already pays
for.

## Source quality

Not all evidence is equal. Weight accordingly, and say which tier a claim came from when it
matters.

**Strong** — primary and verifiable: live pricing pages, official registries and statistics,
regulator and provider documentation, company filings, app-store listings with review counts,
directories with countable entries, the founder's own customer conversations.

**Medium** — reported but plausible: reputable trade press, industry reports where methodology is
visible, marketplace data, sizeable forum consensus, job-posting patterns.

**Weak** — treat as hypothesis, never as fact: single anecdotes, promotional blog posts,
content-marketing "market size" figures (usually fabricated to sell a report), LLM recall
including your own, vendor case studies, anything with a number that ends in too many zeros.

Be especially wary of the market-size number that circulates. "$X billion by 2030" figures are
marketing artifacts; they are copied between blog posts without anyone re-deriving them. If you
cannot find the methodology, tag it `[weak]` or leave it out.

## When the search returns nothing

This happens, and it is frequently the most important result in the audit. Resist two temptations:
filling the gap with plausible-sounding invention, and concluding the space is empty.

Diagnose which kind of nothing it is:

**Wrong vocabulary.** The industry calls it something else. Try the term a practitioner would use,
not the term a founder would use. Search in the local language as well as English — for many
markets the entire commercial internet is in the local language and an English search finds
nothing.

**Genuinely absent, for a reason.** Someone has tried. Look for why: regulation, a structural
economic problem, the customer not actually paying, a platform that forbids it. Search the
category plus *illegal*, *licence required*, *banned*, *regulation*.

**Genuinely absent, no obvious reason.** Rare, and the interesting case. Treat it as a strong
signal that something is not understood yet rather than as open territory — and lower confidence
in the whole audit accordingly, saying so explicitly.

Whatever the cause: write "I could not find evidence for X" in the report as a finding, with the
searches attempted. A founder who knows the audit has a hole can go fill it. A founder handed a
confident fabrication cannot.

## When the sources exist but cannot be opened

Distinct from finding nothing, and far more dangerous, because it leaves you holding partial
information that feels like knowledge. Search results name the competitors, but the pages
themselves will not load — blocked at the network layer, geo-restricted, behind a login, or simply
unreachable from where this is running. This is the *likely* outcome in exactly the markets the
locale annexes exist to serve.

What you have in that situation is competitor **names** and no competitor **prices**, and those
are not the same evidence at all. Handle it explicitly:

- **Say it in the verdict section, not the appendix.** "Every local vendor domain was unreachable;
  I have names and no prices" belongs where the founder reads it first, because it changes how much
  weight the whole report can carry.
- **Downgrade confidence, and say which conclusions inherit the downgrade.** Pricing, positioning,
  and feature-comparison claims all rest on pages you could not read.
- **Do not substitute inference for the missing page.** A competitor's price guessed from its
  category is `[assumed]`, and labelling it anything else corrupts the model downstream.
- **Hand the founder the list.** They can open those pages in thirty seconds from where they are.
  A short "check these five URLs and tell me the prices" is a far better deliverable than a
  confident number you invented, and it often turns a low-confidence audit into a solid one in a
  single round trip.

## Local-language search

For any non-English market this is not optional. Competitors, prices, complaints, and shutdown
stories exist in the local language and nowhere else. Search the key terms in the local language;
check the platforms that market actually uses rather than the global defaults. A "no competitors"
finding derived only from English-language searching is worthless and should never be reported as
one.

## Recording what you find

Keep a running evidence table as you go — it becomes the appendix of the report, and it is what
lets the founder check the work rather than trust it.

| Claim | Value | Tag | Source | Date |
|---|---|---|---|---|
| Competitor A entry price | €29/mo | `[sourced]` | pricing page, url | 2026-09 |
| Clinics in country | 512 | `[sourced]` | association directory, url | 2026-09 |
| Conversion rate of channel | 1.5% | `[assumed]` | industry rule of thumb, no local data | — |

Include dates. Prices and market conditions move, and a report that gets re-read in six months
should carry its own expiry information.

## What this phase is not

It is not a literature review, and length is not quality. Six well-chosen findings that bear
directly on the top-ranked assumptions beat forty paragraphs of context. If a finding does not
change the verdict, the arithmetic, or the experiment, it does not belong in the report.
