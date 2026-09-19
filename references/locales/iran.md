# Locale annex — Iran

*Last reviewed: 2026-09. Conditions here change faster than in most markets — treat every specific
as needing re-verification, and re-check anything that decides a verdict.*

This annex exists because generic startup reasoning is wrong about Iran in specific, predictable
ways, and those errors are usually expensive. Read it alongside `local-market-lens.md`, not
instead of it.

## The structural fact that governs everything

Iran's internet economy is largely **disconnected from the global payment and platform system, and
internally quite complete.** Both halves matter.

International rails — Stripe, PayPal, Paddle, Lemon Squeezy, the Apple and Google app stores, and
most global SaaS billing — are not available to an Iranian individual or company. Any model that
assumes them is blocked, not disadvantaged.

Domestically, there is a mature, fully functional ecosystem: Shetab card switching, local payment
gateways, local app stores, local cloud, local marketplaces. A domestic business does not need the
international system at all. The two worlds do not connect cleanly, and where they do, the
connection is fragile and periodically closed.

So the first question for any Iranian idea is: **which side of that line does this business live
on?** Ideas that die on one side are entirely viable on the other.

## Payments

### Domestic — the normal case, and it works
Card payment through Shetab is universal and reliable. Getting a gateway involves a choice between
two routes, and the distinction matters for a solo founder:

- **درگاه مستقیم (direct gateway)** from a PSP — requires a registered business, a business bank
  account, and, for e-commerce, **نماد اعتماد الکترونیکی (eNamad)**. Lower fees, more paperwork.
- **پرداخت‌یار (payment facilitator)** — Zarinpal, Vandar, IDPay, Zibal, PayStar, ParsPal and
  others act as an intermediary. Faster to set up, lighter requirements, higher fees, and settlement
  through the facilitator rather than directly. This is the normal route for freelancers and small
  projects, and it is a genuine, legal channel.

Requirements shift with regulation — eNamad and tax-registration rules in particular have been
tightened repeatedly — so verify the current state with the facilitator's own documentation rather
than an old blog post before treating it as settled.

### Recurring billing — verify before assuming either way
This is the single most important thing to check for any subscription idea here.

Card-on-file recurring billing in the international sense is not how this market works. What does
exist is **پرداخت خودکار / direct debit (پرداخت مستقیم)** — a mandate-based service offered by
some payment providers (Vandar and Digipay's subscription gateway both market one), which the user
authorises once and which then pulls from their account. It has its own eligibility requirements
and is not universally available to every business type.

The practical consequence for a small founder: assume the smooth Stripe-style subscription is
unavailable until proven otherwise, and design around one of these instead — direct-debit mandate
where the provider will grant it, prepaid credit/wallet top-ups, or explicit period renewal where
the customer re-pays each cycle. The last of these has materially worse retention than automatic
billing, and the model must reflect that, not hope otherwise.

### Receiving money from abroad
Difficult, and the difficulty is the business constraint, not a technicality. Normal international
routes are unavailable. What people actually use — intermediaries, accounts held abroad, crypto,
informal transfer (حواله/صرافی) — varies in cost, legality across jurisdictions, reliability, and
risk, and the mix changes with enforcement.

For an audit: if the idea's revenue comes from outside Iran, **the receiving mechanism is a
first-class assumption and belongs in the top three of the stack**, not in an appendix. Do not
recommend a specific workaround; establish that the founder has a route that works for them, cost
it honestly, and note the fragility. A founder who has already solved this has a real advantage;
one who has not has an unsolved problem more important than their product.

## Purchasing power and pricing

- Price in **toman** and expect to state prices in toman; the rial/toman distinction and the
  informal convention of dropping zeros both appear in everyday pricing.
- Currency instability is a modelling requirement, not a caveat. Costs denominated in foreign
  currency (servers abroad, APIs, domains) against revenue in toman can invert a margin within a
  year. Model in toman, state the exchange assumption explicitly, and sensitivity-test it.
- Local price anchors are far below international ones for the same category of software. A price
  taken from a US SaaS comparable will be wrong by an order of magnitude. Anchor against what
  Iranian products in the same category actually charge.
- Labour is inexpensive relative to software priced internationally, so "hire someone to do it
  manually" is a stronger competitor here than in high-wage markets. Any tool replacing human work
  must beat that comparison, and often cannot.
- B2B budgets exist and are real, but sales cycles are relationship-led and slower than a founder
  modelling self-serve signup expects.

## Regulation and legal form

- Business registration (ثبت شرکت) and tax registration are required for a direct gateway, and the
  tax system's requirements for online businesses have been tightened in recent years. A founder
  operating informally should know that this affects which payment routes are open to them.
- **eNamad** is the e-commerce trust mark and is a practical prerequisite for much of the
  ecosystem, including direct gateways and some advertising platforms.
- Sector licensing is real: health, education, financial services, and anything publishing content
  all have permit regimes worth checking specifically rather than assuming.
- Data and content rules exist and are enforced unevenly; anything handling personal, health, or
  financial data should be checked rather than assumed permissible.

## Infrastructure and platform access

- Domestic hosting and cloud are mature and inexpensive; using them keeps a business inside the
  working half of the system. Hosting abroad brings a payment problem, an access problem, and
  sometimes a latency problem for local users.
- **Access to foreign APIs and services is a live constraint**: many providers geo-block Iranian
  IPs, and many require an international card to pay for. An idea whose core depends on a foreign
  AI API, map provider, or SaaS dependency has a dependency risk that is structural, not
  occasional. This deserves explicit treatment in the assumption stack.
- App distribution: Google Play and the App Store are not reliable channels. Domestic stores —
  Cafe Bazaar, Myket — are the real distribution, along with direct APK and PWA. iOS is a genuine
  problem for consumer apps and can invalidate a product plan aimed at higher-income users.
- Internet disruption and filtering are a real operating risk. A business whose revenue stops
  during an outage should carry that in the model rather than as a footnote.

## Distribution channels that work here

Founders often model channels that barely exist locally and ignore the ones that do.

- **Telegram, Instagram, WhatsApp, Eitaa, Bale** carry a great deal of commerce and community.
  Instagram in particular functions as a storefront, catalogue, and support channel for large
  numbers of small businesses. Presence and access to these platforms varies with filtering, which
  is itself a channel risk.
- **Domestic ad networks and in-app advertising** exist and are purchasable in toman.
- **Divar and Sheypoor** for classifieds and local transactions; **Digikala** for retail goods;
  a marketplace listing is often the real route to demand rather than an owned website.
- **Karlancer, Ponisha and similar freelance platforms** for service-based offerings.
- SEO in Persian works and is comparatively under-exploited in many niches.
- B2B runs on personal networks, industry associations, trade exhibitions, and referral. A cold
  email campaign is not a channel here.

## Cultural and behavioural notes

- Prepayment resistance from unfamiliar sellers is common; trust markers (eNamad, a real address, a
  phone number that is answered, visible prior customers) do measurable work.
- Subscription as a habit is less established than in Western markets — another reason the
  recurring-payment question is decisive rather than incidental.
- Nowruz and the Persian calendar govern business rhythm: the fiscal year, the multi-week slowdown
  around Nowruz, and religious holidays all belong in any monthly trajectory model.
- The Persian internet is a nearly separate information space. Research in Persian, on Persian
  platforms; an English-only search will find no competitors and will be wrong.

## Where the advantage actually is

The honest asymmetry, and it is worth stating plainly in any report where it applies: **an Iranian
founder's cost base is very low by international standards.** For work that can be delivered
digitally and paid for through a route the founder has already solved, a revenue that would be
unviable in Europe or North America can be a good income here. Freelance and service businesses
serving abroad, remote contract work, and digital products sold through an intermediary that
handles receiving are the categories where this advantage is largest.

The binding constraint in almost every one of those cases is not demand, skill, or cost — it is
**getting paid**. An audit of any outward-facing Iranian idea that does not resolve the receiving
question has not audited the idea.

## Checklist for an Iran-based audit

1. Which side of the line — domestic revenue, or foreign revenue? This determines everything else.
2. If foreign revenue: what is the receiving route, does the founder already have it working, what
   does it cost, and how fragile is it?
3. If the model is a subscription: which recurring mechanism, and is it actually available to this
   founder's business type?
4. Does the product depend on any foreign API or service that blocks Iranian access or requires an
   international card?
5. If it is an app: what is the distribution route, and does iOS matter to this audience?
6. Is the price anchored to Iranian comparables rather than international ones?
7. Is the model in toman, with the exchange-rate assumption stated and stress-tested?
8. Which of the channels above is the real route to the customer, and what does it cost?
9. Does the business need eNamad, registration, or a sector licence — and can the founder get it?
10. Does the trajectory account for Nowruz and the local fiscal calendar?
