---
title: "VCC Calculations summary"
confluence_id: 19699040301
confluence_url: https://bainco.atlassian.net/wiki/spaces/OI30/pages/19699040301
version: 2
updated: 2026-08-05T13:50:39.795Z
---

# VCC Calculations summary

[View in Confluence](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19699040301)

# VCC Calculation Assumptions, Business Logic, and Data Quality Rules

### Consolidated from VCC - Data/Calc Q&A

# Executive Summary

The VCC calculation framework follows five core principles:

1.

**Use source-reported financial data whenever available.**

1.

**Use fallback hierarchies instead of derived plug values.**

1.

**Maintain consistency between historical and forecast methodologies.**

1.

**Prefer NULL over misleading or fabricated values.**

1.

**Design for extensibility through configurable taxonomies and calculation frameworks.** [[VCC - Data/Calc Q&A | Teams]](https://teams.microsoft.com/l/message/19:bd624102235240c0956b930994553624@thread.v2/1785785923519?context=%7B%22contextType%22:%22chat%22%7D)

# Section 1: Revenue Growth & Size of Prize

## Revenue Growth Calculation

Projected revenue growth uses CAGR between current revenue and forecast revenue:

Projected CAGR = (Future Revenue ÷ Current Revenue)^(1/Years) - 1

Assumptions:

-

Current revenue is the latest actual revenue.

-

Future revenue comes from analyst consensus forecasts.

-

Growth period is the elapsed time between current and future revenue dates. [[VCC - Data/Calc Q&A | Teams]](https://teams.microsoft.com/l/message/19:bd624102235240c0956b930994553624@thread.v2/1781082634095?context=%7B%22contextType%22:%22chat%22%7D)

## Revenue Size of Prize

Calculates additional revenue achievable if the company grew at peer benchmark rates.

### Formula

Expected Revenue at Benchmark Growth − Current Analyst Forecast Revenue

Benchmarks used:

-

Peer Median Growth

-

Top Quartile Growth

Assumptions:

-

Opportunity is measured versus analyst forecast.

-

Peer growth rates come from peer-set benchmarks.

-

Future growth is compounded over the analysis period. [[VCC - Data/Calc Q&A | Teams]](https://teams.microsoft.com/l/message/19:bd624102235240c0956b930994553624@thread.v2/1781082634095?context=%7B%22contextType%22:%22chat%22%7D), [[VCC - Data/Calc Q&A | Teams]](https://teams.microsoft.com/l/message/19:bd624102235240c0956b930994553624@thread.v2/1781036436165?context=%7B%22contextType%22:%22chat%22%7D)

# Section 2: EBIT & EBITDA Margin Opportunity

## Formula

1

Size of Prize =

2

(Target Margin − Current Margin)

3

× Revenue

Used for:

-

EBIT Margin

-

EBITDA Margin

Assumptions:

-

Revenue remains constant.

-

Margin improvement is the sole driver of opportunity.

-

Benchmarks come from peer median or top quartile values. [[VCC - Data/Calc Q&A | Teams]](https://teams.microsoft.com/l/message/19:bd624102235240c0956b930994553624@thread.v2/1778519770811?context=%7B%22contextType%22:%22chat%22%7D), [[VCC - Data/Calc Q&A | Teams]](https://teams.microsoft.com/l/message/19:bd624102235240c0956b930994553624@thread.v2/1778515676949?context=%7B%22contextType%22:%22chat%22%7D)

# Section 3: Revenue Stack Bar Logic

## Adjusted EBIT Construction

Adjusted EBIT is not sourced directly.

Instead:

1

Adjusted EBIT =

2

Revenue

3

− COGS

4

− SG&A

5

− R&D

or

1

Adjusted EBIT =

2

Revenue

3

− COGS

4

− Selling & Marketing

5

− General & Administrative

6

− R&D

Purpose:

Ensure all components reconcile exactly to revenue.

Example:

1

Revenue = 100

2

3

COGS = 20

4

SG&A = 25

5

6

Adjusted EBIT = 55

Validation:

1

20 + 25 + 55 = 100

Assumption:

Revenue stack must always balance. [[VCC - Data/Calc Q&A | Teams]](https://teams.microsoft.com/l/message/19:bd624102235240c0956b930994553624@thread.v2/1778615641057?context=%7B%22contextType%22:%22chat%22%7D), [[VCC - Data/Calc Q&A | Teams]](https://teams.microsoft.com/l/message/19:bd624102235240c0956b930994553624@thread.v2/1778615345517?context=%7B%22contextType%22:%22chat%22%7D)

# Section 4: SG&A Methodology

## Reporting Scenarios

Companies may report:

### Scenario A

1

Selling & Marketing

2

General & Administrative

Separately.

### Scenario B

1

Combined SG&A

Only.

## Approved Hierarchy

1

1.

Combined SG&A (IQ_SGA)

2

1.

S&M + G&A

3

1.

NULL

Not acceptable:

1

SG&A = 0

Assumptions:

-

Reported SG&A is more reliable.

-

S&M values vary greatly across companies.

-

Derived plug values should be avoided. [[VCC - Data/Calc Q&A | Teams]](https://teams.microsoft.com/l/message/19:bd624102235240c0956b930994553624@thread.v2/1783447401346?context=%7B%22contextType%22:%22chat%22%7D), [[VCC - Data/Calc Q&A | Teams]](https://teams.microsoft.com/l/message/19:bd624102235240c0956b930994553624@thread.v2/1783526844713?context=%7B%22contextType%22:%22chat%22%7D), [[VCC - Data/Calc Q&A | Teams]](https://teams.microsoft.com/l/message/19:bd624102235240c0956b930994553624@thread.v2/1783352774895?context=%7B%22contextType%22:%22chat%22%7D)

# Section 5: EV / EBITDA Multiple Logic

## Multiple Calculation

Thomas Gerber clarified that target prices represent approximately a one-year forward valuation.

Calculation:

1

EV =

2

(Target Price × Shares)

3

+ Future Net Debt

4

+ Other EV Components

Then:

1

EV/EBITDA =

2

Future Enterprise Value

3

÷ Future EBITDA

Assumptions:

-

EBITDA is future consensus EBITDA.

-

Net debt is future consensus net debt.

-

Target price represents approximately 12 months forward value. [[VCC - Data/Calc Q&A | Teams]](https://teams.microsoft.com/l/message/19:bd624102235240c0956b930994553624@thread.v2/1785741656776?context=%7B%22contextType%22:%22chat%22%7D), [[VCC - Data/Calc Q&A | Teams]](https://teams.microsoft.com/l/message/19:bd624102235240c0956b930994553624@thread.v2/1785741554557?context=%7B%22contextType%22:%22chat%22%7D)

## Multiple Assumption Scenarios

### Option 1

1

Multiple remains constant

### Option 2

1

Multiple expands/contracts

2

based on analyst target prices

Future enhancement:

User-selectable toggle between the two assumptions. [[VCC - Data/Calc Q&A | Teams]](https://teams.microsoft.com/l/message/19:bd624102235240c0956b930994553624@thread.v2/1785741708076?context=%7B%22contextType%22:%22chat%22%7D), [[VCC - Data/Calc Q&A | Teams]](https://teams.microsoft.com/l/message/19:bd624102235240c0956b930994553624@thread.v2/1785741725107?context=%7B%22contextType%22:%22chat%22%7D), [[VCC - Data/Calc Q&A | Teams]](https://teams.microsoft.com/l/message/19:bd624102235240c0956b930994553624@thread.v2/1785741702071?context=%7B%22contextType%22:%22chat%22%7D)

## EBIT vs EBITDA Consistency Rule

Concern identified:

Lever calculations use EBIT.

Final multiple was proposed using EBITDA.

Risk:

Mixing valuation bases.

Guidance:

1

Use one basis consistently.

No strong preference for EBIT or EBITDA, but consistency is required. [[VCC - Data/Calc Q&A | Teams]](https://teams.microsoft.com/l/message/19:bd624102235240c0956b930994553624@thread.v2/1785775805202?context=%7B%22contextType%22:%22chat%22%7D), [[VCC - Data/Calc Q&A | Teams]](https://teams.microsoft.com/l/message/19:bd624102235240c0956b930994553624@thread.v2/1785780346902?context=%7B%22contextType%22:%22chat%22%7D), [[VCC - Data/Calc Q&A | Teams]](https://teams.microsoft.com/l/message/19:bd624102235240c0956b930994553624@thread.v2/1785780321454?context=%7B%22contextType%22:%22chat%22%7D)

# Section 6: TSR Decomposition

## Components

1

Beginning Share Price

2

3

+ Revenue Change

4

+ Margin Change

5

+ Leverage Change

6

+ Multiple Change

7

8

= Target Share Price

9

10

+ Dividends

11

12

= Total Shareholder Return Value

Example shared:

1

39.85

2

+1.48 Revenue

3

+5.55 Margin

4

−2.97 Leverage

5

−2.37 Multiple

6

=41.54

7

8

+2.09 Dividends

9

10

=43.63 TSR

Assumptions:

-

Multiple movement is isolated into a separate factor.

-

Dividends contribute after operating and valuation drivers. [[VCC - Data/Calc Q&A | Teams]](https://teams.microsoft.com/l/message/19:bd624102235240c0956b930994553624@thread.v2/1785506968589?context=%7B%22contextType%22:%22chat%22%7D), [[VCC - Data/Calc Q&A | Teams]](https://teams.microsoft.com/l/message/19:bd624102235240c0956b930994553624@thread.v2/1785351993183?context=%7B%22contextType%22:%22chat%22%7D)

# Section 7: Economic Profit Logic

## Non-Financial Companies

1

Economic Profit =

2

NOPAT

3

− (Funds Employed × WACC)

[[VCC - Data/Calc Q&A | Teams]](https://teams.microsoft.com/l/message/19:bd624102235240c0956b930994553624@thread.v2/1779665387099?context=%7B%22contextType%22:%22chat%22%7D)

## Financial Companies

1

Economic Profit =

2

NPAT

3

− (Total Equity × Cost of Equity)

Forecast rule:

The same methodology used historically must also be used for forecast calculations.

An implementation defect was identified and corrected where forecast logic incorrectly applied non-financial methodology to financial institutions. [[VCC - Data/Calc Q&A | Teams]](https://teams.microsoft.com/l/message/19:bd624102235240c0956b930994553624@thread.v2/1778176327885?context=%7B%22contextType%22:%22chat%22%7D)

# Section 8: Working Capital Calculations

## DIO

1

Inventory ÷ COGS × Days

## DPO

1

Accounts Payable ÷ COGS × Days

## DSO

1

Accounts Receivable ÷ Revenue × Days

## CCC

1

DIO + DSO − DPO

Assumptions confirmed by OI methodology discussions. [[VCC - Data/Calc Q&A | Teams]](https://teams.microsoft.com/l/message/19:bd624102235240c0956b930994553624@thread.v2/1778178956316?context=%7B%22contextType%22:%22chat%22%7D), [[VCC - Data/Calc Q&A | Teams]](https://teams.microsoft.com/l/message/19:bd624102235240c0956b930994553624@thread.v2/1778183759829?context=%7B%22contextType%22:%22chat%22%7D)

# Section 9: LTM Balance Sheet Averaging Logic

Problem:

Balance sheet data is a point-in-time snapshot.

Flow metrics are full-period values.

## Preferred Method

1

Average Balance =

2

(Current Quarter Snapshot

3

+

4

Same Quarter Prior Year Snapshot)

5

÷ 2

Example:

1

Q1 2026

2

+

3

Q1 2025

Reason:

Produces a more representative working capital balance. [[VCC - Data/Calc Q&A | Teams]](https://teams.microsoft.com/l/message/19:bd624102235240c0956b930994553624@thread.v2/1778871191242?context=%7B%22contextType%22:%22chat%22%7D), [[VCC - Data/Calc Q&A | Teams]](https://teams.microsoft.com/l/message/19:bd624102235240c0956b930994553624@thread.v2/1778871280904?context=%7B%22contextType%22:%22chat%22%7D)

# Section 10: R&D Methodology

Two source fields are available:

1

IQ_RD_EXP

2

IQ_RD_EXP_FN

## Final Logic

1

RD_PCT =

2

COALESCE(

3

IQ_RD_EXP,

4

IQ_RD_EXP_FN

5

)

6

÷ Revenue

Priority:

1

1.

Line-item R&D

2

1.

Footnote R&D

Coverage analysis showed this maximizes company coverage while maintaining source precedence. [[VCC - Data/Calc Q&A | Teams]](https://teams.microsoft.com/l/message/19:bd624102235240c0956b930994553624@thread.v2/1777322010857?context=%7B%22contextType%22:%22chat%22%7D)

# Section 11: Peer Median Methodology

## Median Rules

Include:

-

Latest available company value.

-

Values within approximately one year of the latest reporting period.

Exclude:

-

Significantly older observations.

Important clarification:

Target company should be included in peer median calculations. [[VCC - Data/Calc Q&A | Teams]](https://teams.microsoft.com/l/message/19:bd624102235240c0956b930994553624@thread.v2/1777931159019?context=%7B%22contextType%22:%22chat%22%7D), [[VCC - Data/Calc Q&A | Teams]](https://teams.microsoft.com/l/message/19:bd624102235240c0956b930994553624@thread.v2/1778086081658?context=%7B%22contextType%22:%22chat%22%7D)

# Section 12: Industry Mapping & Taxonomy Design

## Architectural Decision

Industry mappings should support:

-

Bain taxonomy

-

PEG taxonomy

-

Client taxonomy

Implementation:

1

TAXONOMY_TYPE

column introduced to support multiple methodologies without schema changes. [[VCC - Data/Calc Q&A | Teams]](https://teams.microsoft.com/l/message/19:bd624102235240c0956b930994553624@thread.v2/1779292643059?context=%7B%22contextType%22:%22chat%22%7D), [[VCC - Data/Calc Q&A | Teams]](https://teams.microsoft.com/l/message/19:bd624102235240c0956b930994553624@thread.v2/1779176180245?context=%7B%22contextType%22:%22chat%22%7D)

# Data Quality Rules

## Rule 1: Impossible Gross Margins

Condition:

1

Gross Margin > 100%

Typically caused by negative revenue.

Action:

1

Blank / NULL

Do not display. [[VCC - Data/Calc Q&A | Teams]](https://teams.microsoft.com/l/message/19:bd624102235240c0956b930994553624@thread.v2/1781807975749?context=%7B%22contextType%22:%22chat%22%7D)

## Rule 2: Extreme DIO / DPO Values

Condition:

1

Adjusted COGS ≈ 0

Causing:

1

DIO

2

DPO

to become unrealistically large.

Action:

1

Blank / NULL

Threshold discussed:

-

Initial = 10 years

-

Recommended ≈ 1000 days

[[VCC - Data/Calc Q&A | Teams]](https://teams.microsoft.com/l/message/19:bd624102235240c0956b930994553624@thread.v2/1781807975749?context=%7B%22contextType%22:%22chat%22%7D), [[VCC - Data/Calc Q&A | Teams]](https://teams.microsoft.com/l/message/19:bd624102235240c0956b930994553624@thread.v2/1781810177592?context=%7B%22contextType%22:%22chat%22%7D)

## Rule 3: Missing SG&A

Condition:

No:

1

S&M + G&A

and no:

1

Combined SG&A

Action:

1

NULL

Never default to zero. [[VCC - Data/Calc Q&A | Teams]](https://teams.microsoft.com/l/message/19:bd624102235240c0956b930994553624@thread.v2/1783447401346?context=%7B%22contextType%22:%22chat%22%7D), [[VCC - Data/Calc Q&A | Teams]](https://teams.microsoft.com/l/message/19:bd624102235240c0956b930994553624@thread.v2/1783352774895?context=%7B%22contextType%22:%22chat%22%7D)

## Rule 4: Missing R&D

Use source fallback:

1

IQ_RD_EXP

2

→ IQ_RD_EXP_FN

before nulling the metric. [[VCC - Data/Calc Q&A | Teams]](https://teams.microsoft.com/l/message/19:bd624102235240c0956b930994553624@thread.v2/1777322010857?context=%7B%22contextType%22:%22chat%22%7D)

## Rule 5: Industry Classification Gaps

Companies lacking valid industry mappings:

1

Excluded

until mapping is resolved. [[VCC - Data/Calc Q&A | Teams]](https://teams.microsoft.com/l/message/19:bd624102235240c0956b930994553624@thread.v2/1779694521776?context=%7B%22contextType%22:%22chat%22%7D), [[VCC - Data/Calc Q&A | Teams]](https://teams.microsoft.com/l/message/19:bd624102235240c0956b930994553624@thread.v2/1779292843089?context=%7B%22contextType%22:%22chat%22%7D)

## Rule 6: Missing Source Data

Principle:

1

NULL > Incorrect Value

If financial components cannot be sourced reliably:

-

Leave metric blank.

-

Do not fabricate values.

-

Consider excluding company from benchmark calculations. [[VCC - Data/Calc Q&A | Teams]](https://teams.microsoft.com/l/message/19:bd624102235240c0956b930994553624@thread.v2/1783447401346?context=%7B%22contextType%22:%22chat%22%7D)

## Rule 7: Historical / Forecast Consistency

All methodologies should operate consistently across:

-

Historical data

-

Forecast data

Applied to:

-

Economic Profit

-

EV Multiples

-

TSR

-

NWC Metrics

This is one of the strongest recurring design rules across the discussion. [[VCC - Data/Calc Q&A | Teams]](https://teams.microsoft.com/l/message/19:bd624102235240c0956b930994553624@thread.v2/1778176327885?context=%7B%22contextType%22:%22chat%22%7D), [[VCC - Data/Calc Q&A | Teams]](https://teams.microsoft.com/l/message/19:bd624102235240c0956b930994553624@thread.v2/1785775805202?context=%7B%22contextType%22:%22chat%22%7D), [[VCC - Data/Calc Q&A | Teams]](https://teams.microsoft.com/l/message/19:bd624102235240c0956b930994553624@thread.v2/1785741554557?context=%7B%22contextType%22:%22chat%22%7D)

# Key Open Backlog / Enhancement Ideas

1.

Multiple assumption toggle (constant vs changing multiple). [[VCC - Data/Calc Q&A | Teams]](https://teams.microsoft.com/l/message/19:bd624102235240c0956b930994553624@thread.v2/1785741702071?context=%7B%22contextType%22:%22chat%22%7D)

1.

Same-date peer comparison capability. [[VCC - Data/Calc Q&A | Teams]](https://teams.microsoft.com/l/message/19:bd624102235240c0956b930994553624@thread.v2/1783975840451?context=%7B%22contextType%22:%22chat%22%7D), [[VCC - Data/Calc Q&A | Teams]](https://teams.microsoft.com/l/message/19:bd624102235240c0956b930994553624@thread.v2/1783974598537?context=%7B%22contextType%22:%22chat%22%7D)

1.

Local-currency storage model instead of USD-only storage. [[VCC - Data/Calc Q&A | Teams]](https://teams.microsoft.com/l/message/19:bd624102235240c0956b930994553624@thread.v2/1783611124589?context=%7B%22contextType%22:%22chat%22%7D), [[VCC - Data/Calc Q&A | Teams]](https://teams.microsoft.com/l/message/19:bd624102235240c0956b930994553624@thread.v2/1783612095440?context=%7B%22contextType%22:%22chat%22%7D)

1.

Company-level refresh timestamps. [[VCC - Data/Calc Q&A | Teams]](https://teams.microsoft.com/l/message/19:bd624102235240c0956b930994553624@thread.v2/1778106264799?context=%7B%22contextType%22:%22chat%22%7D), [[VCC - Data/Calc Q&A | Teams]](https://teams.microsoft.com/l/message/19:bd624102235240c0956b930994553624@thread.v2/1778105011350?context=%7B%22contextType%22:%22chat%22%7D)

1.

Improved metric lineage and source transparency. [[VCC - Data/Calc Q&A | Teams]](https://teams.microsoft.com/l/message/19:bd624102235240c0956b930994553624@thread.v2/1777322010857?context=%7B%22contextType%22:%22chat%22%7D), [[VCC - Data/Calc Q&A | Teams]](https://teams.microsoft.com/l/message/19:bd624102235240c0956b930994553624@thread.v2/1777322597503?context=%7B%22contextType%22:%22chat%22%7D)

1.

Multiple taxonomy support (Bain/PEG/client-specific). [[VCC - Data/Calc Q&A | Teams]](https://teams.microsoft.com/l/message/19:bd624102235240c0956b930994553624@thread.v2/1779176180245?context=%7B%22contextType%22:%22chat%22%7D), [[VCC - Data/Calc Q&A | Teams]](https://teams.microsoft.com/l/message/19:bd624102235240c0956b930994553624@thread.v2/1779292643059?context=%7B%22contextType%22:%22chat%22%7D)

**Overall conclusion:** The VCC methodology consistently prioritizes source-reported data, explicit fallback hierarchies, reconciliation to financial statements, and conservative handling of incomplete data through NULLs rather than assumptions

I've prepared a comprehensive document-style analysis of the conversation, consolidating the calculation methodologies, business logic decisions, assumptions, formula definitions, implementation discussions, data quality considerations, and agreed outcomes discussed in VCC - Data/Calc Q&A. [[VCC - Data/Calc Q&A | Teams]](https://teams.microsoft.com/l/message/19:bd624102235240c0956b930994553624@thread.v2/1785785923519?context=%7B%22contextType%22:%22chat%22%7D)

# VCC Data & Calculation Logic Consolidated Reference

## Executive Summary

The conversation primarily focuses on the design, validation, implementation, and quality assurance of calculation methodologies within the Value Creation Center (VCC) platform. The discussions span:

-

TSR decomposition methodology

-

Revenue growth and Size of Prize calculations

-

EBIT and EBITDA calculations

-

EV / EBITDA multiple logic

-

Economic Profit calculations

-

Working Capital metrics (DIO, DPO, DSO, CCC)

-

R&D calculations

-

Industry mapping and adjustment methodologies

-

Capital IQ data sourcing decisions

-

Forecast versus historical metric treatment

-

Data quality validation rules

-

Stakeholder model calculations

-

Currency handling and enterprise value processing

The overall direction of the discussions consistently emphasizes:

1.

Alignment with Bain methodologies.

1.

Preference for sourced financial metrics over derived plug values where possible.

1.

Transparent handling of missing data.

1.

Preservation of analytical explainability.

1.

Future flexibility through configurable taxonomies and calculation frameworks.

[[VCC - Data/Calc Q&A | Teams]](https://teams.microsoft.com/l/message/19:bd624102235240c0956b930994553624@thread.v2/1785785923519?context=%7B%22contextType%22:%22chat%22%7D)

# 1. Revenue Growth Size of Prize Methodology

## Core Formula

The team discussed how projected revenue growth and size-of-prize metrics should be calculated.

Example shared:

1

Projected Revenue Growth Size of Prize =

2

(Current Revenue × (1 + Target Growth Rate)^Growth Period)

3

− Current Revenue

Example:

1

Current Revenue = 57B

2

Target Growth Rate = 4%

3

Growth Period = 5 years

4

5

Size of Prize =

6

57 × (1.04)^5 − 57

7

= 12.35B

[[VCC - Data/Calc Q&A | Teams]](https://teams.microsoft.com/l/message/19:bd624102235240c0956b930994553624@thread.v2/1781036436165?context=%7B%22contextType%22:%22chat%22%7D)

## Refined Forecast-Based Approach

A more detailed methodology was later clarified:

### Inputs

Current Revenue:

1

2,234.1M

Forecast Revenue:

1

2,035.5M

Forecast Period:

1

1.75 years

Projected CAGR:

1

(2035.5 / 2234.1)^(1/1.75) - 1

2

= -5.2%

[[VCC - Data/Calc Q&A | Teams]](https://teams.microsoft.com/l/message/19:bd624102235240c0956b930994553624@thread.v2/1781082634095?context=%7B%22contextType%22:%22chat%22%7D)

### Peer Median Scenario

1

Revenue @ Median Growth =

2

2234.1 × (1.02)^1.75

3

= 2298.0

Size of Prize:

1

2298.0 - 2035.5

2

= 262.5M

[[VCC - Data/Calc Q&A | Teams]](https://teams.microsoft.com/l/message/19:bd624102235240c0956b930994553624@thread.v2/1781082634095?context=%7B%22contextType%22:%22chat%22%7D)

### Top Quartile Scenario

1

Revenue @ Top Quartile Growth =

2

2234.1 × (1.0333)^1.75

3

= 2365.5

Size of Prize:

1

2365.5 - 2035.5

2

= 330M

3

`

Final clarification:

The incremental opportunity should be measured against current analyst forecasted revenue rather than today's revenue baseline.

[[VCC - Data/Calc Q&A | Teams]](https://teams.microsoft.com/l/message/19:bd624102235240c0956b930994553624@thread.v2/1781082634095?context=%7B%22contextType%22:%22chat%22%7D)

# 2. EBIT / EBITDA Margin Size of Prize

The accepted formula is:

1

Size of Prize =

2

(Target Margin − Client Margin)

3

× Revenue

Applicable to:

-

EBIT Margin

-

EBITDA Margin

[[VCC - Data/Calc Q&A | Teams]](https://teams.microsoft.com/l/message/19:bd624102235240c0956b930994553624@thread.v2/1778519770811?context=%7B%22contextType%22:%22chat%22%7D), [[VCC - Data/Calc Q&A | Teams]](https://teams.microsoft.com/l/message/19:bd624102235240c0956b930994553624@thread.v2/1778515676949?context=%7B%22contextType%22:%22chat%22%7D)

# 3. Revenue Stack Bar Logic

A major design discussion concerned the Adjusted EBIT component displayed in the Revenue Stack chart.

### Approved Logic

Adjusted EBIT should be calculated as a residual:

1

Adjusted EBIT =

2

Revenue

3

− COGS

4

− S&M

5

− G&A

6

− R&D

Where applicable:

1

Adjusted EBIT =

2

Revenue

3

− COGS

4

− SG&A

The goal is for stack totals to reconcile to total revenue.

Example given:

1

Revenue = 100

2

COGS = 20

3

SG&A = 25

4

5

Adjusted EBIT = 55

Total:

1

20 + 25 + 55 = 100

Using reported EBIT instead could break reconciliation after adjustments.

[[VCC - Data/Calc Q&A | Teams]](https://teams.microsoft.com/l/message/19:bd624102235240c0956b930994553624@thread.v2/1778615345517?context=%7B%22contextType%22:%22chat%22%7D), [[VCC - Data/Calc Q&A | Teams]](https://teams.microsoft.com/l/message/19:bd624102235240c0956b930994553624@thread.v2/1778615641057?context=%7B%22contextType%22:%22chat%22%7D)

# 4. SG&A Handling Methodology

## Original Problem

Some companies report:

1

Selling & Marketing

2

General & Administrative

Separately.

Others report:

1

Combined SG&A

only.

[[VCC - Data/Calc Q&A | Teams]](https://teams.microsoft.com/l/message/19:bd624102235240c0956b930994553624@thread.v2/1783352774895?context=%7B%22contextType%22:%22chat%22%7D), [[VCC - Data/Calc Q&A | Teams]](https://teams.microsoft.com/l/message/19:bd624102235240c0956b930994553624@thread.v2/1783447401346?context=%7B%22contextType%22:%22chat%22%7D)

## Approved Decision

Priority order:

1

If combined SG&A exists:

2

Use reported IQ_SGA

3

4

Else if split exists:

5

Use S&M + G&A

6

7

Else:

8

NULL

Do not force a zero.

Do not derive SG&A through EBIT plugs when a directly reported SG&A number exists.

Reason:

-

Reported SG&A is more reliable.

-

S&M definitions vary significantly across companies.

[[VCC - Data/Calc Q&A | Teams]](https://teams.microsoft.com/l/message/19:bd624102235240c0956b930994553624@thread.v2/1783447401346?context=%7B%22contextType%22:%22chat%22%7D), [[VCC - Data/Calc Q&A | Teams]](https://teams.microsoft.com/l/message/19:bd624102235240c0956b930994553624@thread.v2/1783526844713?context=%7B%22contextType%22:%22chat%22%7D)

# 5. EV / EBITDA Multiple Methodology

A detailed discussion occurred around enterprise value multiples.

### Thomas Gerber’s Clarification

Target prices represent approximately a 12-month future valuation.

Therefore:

1

EV / EBITDA =

2

(Target Price × Shares Outstanding

3

+ Future Net Debt

4

+ Other EV Contributors)

5

/ Future EBITDA

Where:

-

Target price = future value

-

Net debt = future consensus value

-

EBITDA = future consensus EBITDA

[[VCC - Data/Calc Q&A | Teams]](https://teams.microsoft.com/l/message/19:bd624102235240c0956b930994553624@thread.v2/1785741656776?context=%7B%22contextType%22:%22chat%22%7D), [[VCC - Data/Calc Q&A | Teams]](https://teams.microsoft.com/l/message/19:bd624102235240c0956b930994553624@thread.v2/1785741554557?context=%7B%22contextType%22:%22chat%22%7D)

## Multiple Assumption Options

Two conceptual approaches were discussed:

### Option A

Keep multiple constant.

### Option B

Allow multiple expansion/contraction based on analyst targets.

[[VCC - Data/Calc Q&A | Teams]](https://teams.microsoft.com/l/message/19:bd624102235240c0956b930994553624@thread.v2/1785741708076?context=%7B%22contextType%22:%22chat%22%7D), [[VCC - Data/Calc Q&A | Teams]](https://teams.microsoft.com/l/message/19:bd624102235240c0956b930994553624@thread.v2/1785741725107?context=%7B%22contextType%22:%22chat%22%7D)

A future toggle was proposed to allow users to select the assumption.

[[VCC - Data/Calc Q&A | Teams]](https://teams.microsoft.com/l/message/19:bd624102235240c0956b930994553624@thread.v2/1785741702071?context=%7B%22contextType%22:%22chat%22%7D)

## EBIT versus EBITDA Consistency

An implementation concern arose because:

-

Lever walk calculations used EBIT.

-

Final multiple was proposed using EBITDA.

Concern:

Mixed bases create inconsistency.

Final guidance:

Prefer one metric consistently.

Thomas stated he had no strong preference between EBIT and EBITDA but preferred consistency.

[[VCC - Data/Calc Q&A | Teams]](https://teams.microsoft.com/l/message/19:bd624102235240c0956b930994553624@thread.v2/1785775805202?context=%7B%22contextType%22:%22chat%22%7D), [[VCC - Data/Calc Q&A | Teams]](https://teams.microsoft.com/l/message/19:bd624102235240c0956b930994553624@thread.v2/1785780346902?context=%7B%22contextType%22:%22chat%22%7D), [[VCC - Data/Calc Q&A | Teams]](https://teams.microsoft.com/l/message/19:bd624102235240c0956b930994553624@thread.v2/1785780321454?context=%7B%22contextType%22:%22chat%22%7D), [[VCC - Data/Calc Q&A | Teams]](https://teams.microsoft.com/l/message/19:bd624102235240c0956b930994553624@thread.v2/1785783431971?context=%7B%22contextType%22:%22chat%22%7D)

# 6. TSR Decomposition Methodology

Example decomposition shown:

1

Current Share Price = 39.85

2

3

Revenue Change +1.48

4

Margin Change +5.55

5

Leverage Change -2.97

6

Multiple Change -2.37

7

8

Price Target = 41.54

9

10

Dividends +2.09

11

12

Total Shareholder Value = 43.63

[[VCC - Data/Calc Q&A | Teams]](https://teams.microsoft.com/l/message/19:bd624102235240c0956b930994553624@thread.v2/1785506968589?context=%7B%22contextType%22:%22chat%22%7D)

The multiple lever was subsequently introduced to explain residual valuation changes.

[[VCC - Data/Calc Q&A | Teams]](https://teams.microsoft.com/l/message/19:bd624102235240c0956b930994553624@thread.v2/1785351993183?context=%7B%22contextType%22:%22chat%22%7D)

# 7. Economic Profit Methodology

Special logic exists for financial companies.

## Non-Financial Companies

1

Economic Profit =

2

NOPAT − (Funds Employed × WACC)

[[VCC - Data/Calc Q&A | Teams]](https://teams.microsoft.com/l/message/19:bd624102235240c0956b930994553624@thread.v2/1779665387099?context=%7B%22contextType%22:%22chat%22%7D)

## Financial Companies

Use:

1

NPAT − (Total Equity × Cost of Equity)

instead.

A defect was discovered where projected values used non-financial logic.

Fix:

Historical and forecast calculations should use identical sector-specific formulas.

[[VCC - Data/Calc Q&A | Teams]](https://teams.microsoft.com/l/message/19:bd624102235240c0956b930994553624@thread.v2/1778176327885?context=%7B%22contextType%22:%22chat%22%7D)

# 8. Working Capital Metrics

## DIO

1

Average Inventory / COGS × Days

## DPO

1

Average AP / COGS × Days

## DSO

1

Average AR / Revenue × Days

Confirmed by the Operations Improvement team.

[[VCC - Data/Calc Q&A | Teams]](https://teams.microsoft.com/l/message/19:bd624102235240c0956b930994553624@thread.v2/1778178956316?context=%7B%22contextType%22:%22chat%22%7D), [[VCC - Data/Calc Q&A | Teams]](https://teams.microsoft.com/l/message/19:bd624102235240c0956b930994553624@thread.v2/1778183759829?context=%7B%22contextType%22:%22chat%22%7D)

## LTM Balance Sheet Treatment

Problem:

LTM balance sheet values are quarterly snapshots.

Three options discussed.

### Option 1

Average:

1

LTM Snapshot

2

+

3

Prior Year End

### Option 2

Use snapshot only.

### Option 3

Average four quarterly snapshots.

[[VCC - Data/Calc Q&A | Teams]](https://teams.microsoft.com/l/message/19:bd624102235240c0956b930994553624@thread.v2/1778868599212?context=%7B%22contextType%22:%22chat%22%7D)

### Final Preferred Approach

Add same-quarter prior-year snapshot:

1

(Current Quarter Snapshot

2

+

3

Same Quarter Prior Year Snapshot)

4

/ 2

5

``

Example:

1

Q1 2026

2

+

3

Q1 2025

Average.

[[VCC - Data/Calc Q&A | Teams]](https://teams.microsoft.com/l/message/19:bd624102235240c0956b930994553624@thread.v2/1778871191242?context=%7B%22contextType%22:%22chat%22%7D), [[VCC - Data/Calc Q&A | Teams]](https://teams.microsoft.com/l/message/19:bd624102235240c0956b930994553624@thread.v2/1778871280904?context=%7B%22contextType%22:%22chat%22%7D)

# 9. Gross Margin Data Quality Rules

Issue:

Negative revenue companies produced impossible margins.

Resolution:

1

Gross Margin > 100%

2

→ Blank

3

[[VCC - Data/Calc Q&A | Teams]](https://teams.microsoft.com/l/message/19:bd624102235240c0956b930994553624@thread.v2/1781807975749?context=%7B%22contextType%22:%22chat%22%7D)

# 10. DIO/DPO Outlier Control

Issue:

Near-zero adjusted COGS created extreme values.

Examples:

Hundreds of thousands of days.

Resolution:

Initial threshold:

1

10 years

Later recommendation:

1

~1000 days

Values above threshold become:

1

NULL

[[VCC - Data/Calc Q&A | Teams]](https://teams.microsoft.com/l/message/19:bd624102235240c0956b930994553624@thread.v2/1781807975749?context=%7B%22contextType%22:%22chat%22%7D), [[VCC - Data/Calc Q&A | Teams]](https://teams.microsoft.com/l/message/19:bd624102235240c0956b930994553624@thread.v2/1781810177592?context=%7B%22contextType%22:%22chat%22%7D)

# 11. R&D Methodology

Two CapIQ fields were evaluated:

1

IQ_RD_EXP

2

IQ_RD_EXP_FN

Coverage study:

-

Line item only: ~33%

-

Footnote only: ~30%

-

Both: ~37%

[[VCC - Data/Calc Q&A | Teams]](https://teams.microsoft.com/l/message/19:bd624102235240c0956b930994553624@thread.v2/1777322010857?context=%7B%22contextType%22:%22chat%22%7D)

## Approved Logic

1

RD_PCT =

2

COALESCE(

3

IQ_RD_EXP,

4

IQ_RD_EXP_FN

5

)

6

÷ Revenue

Priority:

1.

Line item

1.

Footnote

[[VCC - Data/Calc Q&A | Teams]](https://teams.microsoft.com/l/message/19:bd624102235240c0956b930994553624@thread.v2/1777322010857?context=%7B%22contextType%22:%22chat%22%7D), [[VCC - Data/Calc Q&A | Teams]](https://teams.microsoft.com/l/message/19:bd624102235240c0956b930994553624@thread.v2/1777322597503?context=%7B%22contextType%22:%22chat%22%7D)

# 12. Peer Median Calculation Rules

Clarified by Noah Wells.

Latest available value is used.

Example:

1

Company A = FY25

2

Company B = FY24

3

Company C = FY26 LTM

4

All included.

However:

If company data is too old:

1

>1 year difference

Exclude from median.

Still display on charts.

[[VCC - Data/Calc Q&A | Teams]](https://teams.microsoft.com/l/message/19:bd624102235240c0956b930994553624@thread.v2/1777931159019?context=%7B%22contextType%22:%22chat%22%7D), [[VCC - Data/Calc Q&A | Teams]](https://teams.microsoft.com/l/message/19:bd624102235240c0956b930994553624@thread.v2/1778084771686?context=%7B%22contextType%22:%22chat%22%7D)

# 13. Industry Adjustment Framework

A long-term architecture decision was agreed.

Requirement:

Support multiple classifications.

Examples:

-

Bain taxonomy

-

PEG taxonomy

-

Client-specific taxonomy

Implementation:

Industry mapping table supports:

1

TAXONOMY_TYPE

2

allowing flexible switching.

[[VCC - Data/Calc Q&A | Teams]](https://teams.microsoft.com/l/message/19:bd624102235240c0956b930994553624@thread.v2/1779176180245?context=%7B%22contextType%22:%22chat%22%7D), [[VCC - Data/Calc Q&A | Teams]](https://teams.microsoft.com/l/message/19:bd624102235240c0956b930994553624@thread.v2/1779292643059?context=%7B%22contextType%22:%22chat%22%7D)

# 14. Currency Handling

Current VCC behavior:

1

Store in USD

even when source data arrives in local currency.

Potential future enhancement:

1

Store local currency natively

and avoid repeated conversion.

No final migration decision was made.

[[VCC - Data/Calc Q&A | Teams]](https://teams.microsoft.com/l/message/19:bd624102235240c0956b930994553624@thread.v2/1783611124589?context=%7B%22contextType%22:%22chat%22%7D), [[VCC - Data/Calc Q&A | Teams]](https://teams.microsoft.com/l/message/19:bd624102235240c0956b930994553624@thread.v2/1783611202748?context=%7B%22contextType%22:%22chat%22%7D)

# 15. Stakeholder Model Logic

Confirmed hierarchy:

### Customer

-

Do #1

-

Do #2

### Employee

Contains third-level metrics:

-

Engagement

-

CEO Approval

-

Culture & Values

-

Pay & Policies

-

Career Opportunities

-

Community

-

Environmental

-

Social

-

Governance

etc.

### Investor

-

EVA Return

-

EVA Growth

-

EVA Return Delta

### Supplier

### Stewardship

### Track Record

Preferred terminology:

1

Stakeholder Groups

rather than "Levers".

[[VCC - Data/Calc Q&A | Teams]](https://teams.microsoft.com/l/message/19:bd624102235240c0956b930994553624@thread.v2/1784317742795?context=%7B%22contextType%22:%22chat%22%7D), [[VCC - Data/Calc Q&A | Teams]](https://teams.microsoft.com/l/message/19:bd624102235240c0956b930994553624@thread.v2/1784317818730?context=%7B%22contextType%22:%22chat%22%7D), [[VCC - Data/Calc Q&A | Teams]](https://teams.microsoft.com/l/message/19:bd624102235240c0956b930994553624@thread.v2/1784319178440?context=%7B%22contextType%22:%22chat%22%7D), [[VCC - Data/Calc Q&A | Teams]](https://teams.microsoft.com/l/message/19:bd624102235240c0956b930994553624@thread.v2/1784318076626?context=%7B%22contextType%22:%22chat%22%7D)

# Final Outcomes Across the Conversation

### Approved / Implemented

✅ Revenue Size-of-Prize framework
✅ EBIT/EBITDA margin opportunity formula
✅ Residual Adjusted EBIT calculation
✅ Future EV/EBITDA multiple methodology
✅ Financial vs non-financial Economic Profit separation
✅ R&D fallback hierarchy
✅ Peer median inclusion rules
✅ Multi-taxonomy architecture design
✅ Same-quarter averaging for LTM working capital calculations
✅ Data quality thresholds for margin and NWC metrics
✅ Stakeholder hierarchy definition

### Future Backlog Items

-

Multiple-assumption toggle.

-

Same-date peer comparison capability.

-

Local-currency storage evaluation.

-

Company-level refresh timestamps.

-

Improved transparency around metric lineage and assumptions.

All conclusions above are derived from discussions contained within VCC - Data/Calc Q&A. [[VCC - Data/Calc Q&A | Teams]](https://teams.microsoft.com/l/message/19:bd624102235240c0956b930994553624@thread.v2/1785785923519?context=%7B%22contextType%22:%22chat%22%7D)

## Key Calculation Assumptions

### 1. Revenue Growth & Size of Prize

**Projected Revenue Growth**

-

Revenue growth is calculated using CAGR between current revenue and forecast revenue over the forecast period.

-

Future opportunity is measured relative to analyst forecast revenue, not current revenue. [[VCC - Data/Calc Q&A | Teams]](https://teams.microsoft.com/l/message/19:bd624102235240c0956b930994553624@thread.v2/1781082634095?context=%7B%22contextType%22:%22chat%22%7D)

**Size of Prize Formula**

1

Expected Revenue at Target Growth

2

− Analyst Forecast Revenue

3

Where target growth may be:

-

Peer Median Growth

-

Top Quartile Growth [[VCC - Data/Calc Q&A | Teams]](https://teams.microsoft.com/l/message/19:bd624102235240c0956b930994553624@thread.v2/1781082634095?context=%7B%22contextType%22:%22chat%22%7D), [[VCC - Data/Calc Q&A | Teams]](https://teams.microsoft.com/l/message/19:bd624102235240c0956b930994553624@thread.v2/1781036436165?context=%7B%22contextType%22:%22chat%22%7D)

### 2. EBIT / EBITDA Margin Opportunity

**Size of Prize**

1

(Target Margin − Client Margin) × Revenue

Applied to both:

-

EBIT Margin

-

EBITDA Margin [[VCC - Data/Calc Q&A | Teams]](https://teams.microsoft.com/l/message/19:bd624102235240c0956b930994553624@thread.v2/1778519770811?context=%7B%22contextType%22:%22chat%22%7D), [[VCC - Data/Calc Q&A | Teams]](https://teams.microsoft.com/l/message/19:bd624102235240c0956b930994553624@thread.v2/1778515676949?context=%7B%22contextType%22:%22chat%22%7D)

### 3. Revenue Stack Bar

**Adjusted EBIT is not a reported value.** It is calculated as the residual needed to reconcile Revenue:

1

Adjusted EBIT =

2

Revenue − COGS − SG&A − R&D

or

1

Revenue − COGS − S&M − G&A − R&D

This ensures all bars sum to total revenue. [[VCC - Data/Calc Q&A | Teams]](https://teams.microsoft.com/l/message/19:bd624102235240c0956b930994553624@thread.v2/1778615641057?context=%7B%22contextType%22:%22chat%22%7D), [[VCC - Data/Calc Q&A | Teams]](https://teams.microsoft.com/l/message/19:bd624102235240c0956b930994553624@thread.v2/1783526844713?context=%7B%22contextType%22:%22chat%22%7D)

### 4. SG&A Treatment

Preferred hierarchy:

1

1.

Reported Combined SG&A (IQ_SGA)

2

1.

S&M + G&A

3

1.

NULL

Key assumption:

-

Never treat missing SG&A as zero.

-

Prefer reported SG&A over derived plugs.

-

S&M definitions are inconsistent across companies. [[VCC - Data/Calc Q&A | Teams]](https://teams.microsoft.com/l/message/19:bd624102235240c0956b930994553624@thread.v2/1783447401346?context=%7B%22contextType%22:%22chat%22%7D), [[VCC - Data/Calc Q&A | Teams]](https://teams.microsoft.com/l/message/19:bd624102235240c0956b930994553624@thread.v2/1783526844713?context=%7B%22contextType%22:%22chat%22%7D), [[VCC - Data/Calc Q&A | Teams]](https://teams.microsoft.com/l/message/19:bd624102235240c0956b930994553624@thread.v2/1783352774895?context=%7B%22contextType%22:%22chat%22%7D)

### 5. EV / EBITDA Multiple

Target price calculations assume a **12-month forward valuation horizon**.

Formula discussed:

1

EV/EBITDA =

2

(Future Market Cap + Future Net Debt + Other EV Components)

3

÷ Future EBITDA

Key assumptions:

-

Use future consensus EBITDA.

-

Use future consensus net debt.

-

Multiple expansion/contraction should be captured separately.

-

Avoid mixing EBIT-based and EBITDA-based methodologies in the same calculation chain. [[VCC - Data/Calc Q&A | Teams]](https://teams.microsoft.com/l/message/19:bd624102235240c0956b930994553624@thread.v2/1785741656776?context=%7B%22contextType%22:%22chat%22%7D), [[VCC - Data/Calc Q&A | Teams]](https://teams.microsoft.com/l/message/19:bd624102235240c0956b930994553624@thread.v2/1785741554557?context=%7B%22contextType%22:%22chat%22%7D), [[VCC - Data/Calc Q&A | Teams]](https://teams.microsoft.com/l/message/19:bd624102235240c0956b930994553624@thread.v2/1785775805202?context=%7B%22contextType%22:%22chat%22%7D), [[VCC - Data/Calc Q&A | Teams]](https://teams.microsoft.com/l/message/19:bd624102235240c0956b930994553624@thread.v2/1785780346902?context=%7B%22contextType%22:%22chat%22%7D)

### 6. TSR Decomposition

TSR decomposition includes these drivers:

1

Starting Share Price

2

+ Revenue Change

3

+ Margin Change

4

+ Leverage Change

5

+ Multiple Change

6

= Target Price

7

8

+ Dividends

9

= Total Shareholder Return Value

A separate Multiple lever is used to explain valuation effects. [[VCC - Data/Calc Q&A | Teams]](https://teams.microsoft.com/l/message/19:bd624102235240c0956b930994553624@thread.v2/1785506968589?context=%7B%22contextType%22:%22chat%22%7D), [[VCC - Data/Calc Q&A | Teams]](https://teams.microsoft.com/l/message/19:bd624102235240c0956b930994553624@thread.v2/1785351993183?context=%7B%22contextType%22:%22chat%22%7D)

### 7. Economic Profit

#### Non-Financial Companies

1

NOPAT − (Funds Employed × WACC)

#### Financial Companies

1

NPAT − (Total Equity × Cost of Equity)

Forecast calculations must use the same logic as historical calculations. [[VCC - Data/Calc Q&A | Teams]](https://teams.microsoft.com/l/message/19:bd624102235240c0956b930994553624@thread.v2/1778176327885?context=%7B%22contextType%22:%22chat%22%7D), [[VCC - Data/Calc Q&A | Teams]](https://teams.microsoft.com/l/message/19:bd624102235240c0956b930994553624@thread.v2/1779665387099?context=%7B%22contextType%22:%22chat%22%7D)

### 8. Working Capital Metrics

**DIO**

1

Inventory ÷ COGS

2

``

**DPO**

1

Accounts Payable ÷ COGS

**DSO**

1

Accounts Receivable ÷ Revenue

**CCC** Calculated from DIO, DSO, and DPO. [[VCC - Data/Calc Q&A | Teams]](https://teams.microsoft.com/l/message/19:bd624102235240c0956b930994553624@thread.v2/1778178956316?context=%7B%22contextType%22:%22chat%22%7D), [[VCC - Data/Calc Q&A | Teams]](https://teams.microsoft.com/l/message/19:bd624102235240c0956b930994553624@thread.v2/1778183759829?context=%7B%22contextType%22:%22chat%22%7D)

### 9. LTM Balance-Sheet Averaging

For LTM calculations, the preferred approach is:

1

(Current Quarter Snapshot

2

+ Same Quarter Prior Year Snapshot)

3

÷ 2

Example:

1

Q1 2026 + Q1 2025

This provides a more representative average balance for NWC metrics. [[VCC - Data/Calc Q&A | Teams]](https://teams.microsoft.com/l/message/19:bd624102235240c0956b930994553624@thread.v2/1778871191242?context=%7B%22contextType%22:%22chat%22%7D), [[VCC - Data/Calc Q&A | Teams]](https://teams.microsoft.com/l/message/19:bd624102235240c0956b930994553624@thread.v2/1778871280904?context=%7B%22contextType%22:%22chat%22%7D)

### 10. R&D Methodology

R&D percentage uses:

1

COALESCE(

2

IQ_RD_EXP,

3

IQ_RD_EXP_FN

4

) ÷ Revenue

Priority:

1.

R&D line item

1.

R&D footnote report

[[VCC - Data/Calc Q&A | Teams]](https://teams.microsoft.com/l/message/19:bd624102235240c0956b930994553624@thread.v2/1777322010857?context=%7B%22contextType%22:%22chat%22%7D)

### 11. Peer Median Logic

Key assumptions:

-

Use each peer's latest available value.

-

Include values up to roughly one year different from the latest peer set period.

-

Include target company in median calculations.

-

Exclude stale values significantly older than the rest of the peer set. [[VCC - Data/Calc Q&A | Teams]](https://teams.microsoft.com/l/message/19:bd624102235240c0956b930994553624@thread.v2/1777931159019?context=%7B%22contextType%22:%22chat%22%7D), [[VCC - Data/Calc Q&A | Teams]](https://teams.microsoft.com/l/message/19:bd624102235240c0956b930994553624@thread.v2/1778086081658?context=%7B%22contextType%22:%22chat%22%7D), [[VCC - Data/Calc Q&A | Teams]](https://teams.microsoft.com/l/message/19:bd624102235240c0956b930994553624@thread.v2/1778084771686?context=%7B%22contextType%22:%22chat%22%7D)

# Data Quality Rules Applied

### Revenue / Margin Quality Rules

#### Invalid Gross Margins

If negative revenue produces:

1

Gross Margin > 100%

2

``

Result:

1

NULL / Blank

2

``

instead of displaying unrealistic values. [[VCC - Data/Calc Q&A | Teams]](https://teams.microsoft.com/l/message/19:bd624102235240c0956b930994553624@thread.v2/1781807975749?context=%7B%22contextType%22:%22chat%22%7D)

### Extreme NWC Metrics

#### DIO / DPO Outlier Protection

When adjusted COGS is close to zero:

1

DIO

2

DPO

can become hundreds of thousands of days.

Rule:

-

Blank extreme values above threshold.

-

Initial threshold: 10 years.

-

Recommendation: reduce toward ~1000 days. [[VCC - Data/Calc Q&A | Teams]](https://teams.microsoft.com/l/message/19:bd624102235240c0956b930994553624@thread.v2/1781807975749?context=%7B%22contextType%22:%22chat%22%7D), [[VCC - Data/Calc Q&A | Teams]](https://teams.microsoft.com/l/message/19:bd624102235240c0956b930994553624@thread.v2/1781810177592?context=%7B%22contextType%22:%22chat%22%7D)

### Missing SG&A Handling

If neither:

1

S&M + G&A

nor:

1

Combined SG&A

exists:

Result:

1

NULL

Do not default to zero. [[VCC - Data/Calc Q&A | Teams]](https://teams.microsoft.com/l/message/19:bd624102235240c0956b930994553624@thread.v2/1783447401346?context=%7B%22contextType%22:%22chat%22%7D), [[VCC - Data/Calc Q&A | Teams]](https://teams.microsoft.com/l/message/19:bd624102235240c0956b930994553624@thread.v2/1783352774895?context=%7B%22contextType%22:%22chat%22%7D)

### Company Inclusion Quality Checks

When key financial components are unavailable:

-

Leave metric blank.

-

Consider excluding company from comparative analysis if supporting financial data is unreliable. [[VCC - Data/Calc Q&A | Teams]](https://teams.microsoft.com/l/message/19:bd624102235240c0956b930994553624@thread.v2/1783447401346?context=%7B%22contextType%22:%22chat%22%7D)

### R&D Quality Rule

Use fallback sourcing:

1

Line Item → Footnote

to maximize coverage while retaining source hierarchy. [[VCC - Data/Calc Q&A | Teams]](https://teams.microsoft.com/l/message/19:bd624102235240c0956b930994553624@thread.v2/1777322010857?context=%7B%22contextType%22:%22chat%22%7D)

### Industry Mapping Quality Controls

-

Companies with missing industry classifications are excluded until mappings are available.

-

Unmapped industries require explicit classification before inclusion. [[VCC - Data/Calc Q&A | Teams]](https://teams.microsoft.com/l/message/19:bd624102235240c0956b930994553624@thread.v2/1779694521776?context=%7B%22contextType%22:%22chat%22%7D), [[VCC - Data/Calc Q&A | Teams]](https://teams.microsoft.com/l/message/19:bd624102235240c0956b930994553624@thread.v2/1779292843089?context=%7B%22contextType%22:%22chat%22%7D)

### Forecast / Historical Consistency

A recurring design principle throughout the conversation:

**Historical and forecast calculations should follow the same methodology wherever possible.**

Examples:

-

Economic Profit

-

EV/EBITDA Multiples

-

TSR decomposition

-

Working Capital calculations

This was repeatedly raised to avoid calculation distortions between historical and projected views. [[VCC - Data/Calc Q&A | Teams]](https://teams.microsoft.com/l/message/19:bd624102235240c0956b930994553624@thread.v2/1778176327885?context=%7B%22contextType%22:%22chat%22%7D), [[VCC - Data/Calc Q&A | Teams]](https://teams.microsoft.com/l/message/19:bd624102235240c0956b930994553624@thread.v2/1785775805202?context=%7B%22contextType%22:%22chat%22%7D), [[VCC - Data/Calc Q&A | Teams]](https://teams.microsoft.com/l/message/19:bd624102235240c0956b930994553624@thread.v2/1785741554557?context=%7B%22contextType%22:%22chat%22%7D)

### Overall Guiding Principle

The strongest recurring rule across the discussion was:

>

Prefer directly reported/source financial data, use controlled fallbacks when necessary, and return NULL rather than displaying potentially misleading values
