---
title: "Non-negotiable adjustments in OI"
confluence_id: 19751993421
confluence_url: https://bainco.atlassian.net/wiki/spaces/OI30/pages/19751993421
version: 2
updated: 2026-08-21T08:46:58.757Z
---

# Non-negotiable adjustments in OI

[View in Confluence](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19751993421)

August 21 meeting: Michelle, Akhil, Niko

Zoom link: [https://bain.zoom.us/rec/share/k2GgZLpUKo93f3kZiI3GZdaOjAKTIx2pZA_WtTDcVkP7a9lRIXiofdGid1w3q_zp.-AtbRvqZuHZB4BNK](https://urldefense.com/v3/__https:/bain.zoom.us/rec/share/k2GgZLpUKo93f3kZiI3GZdaOjAKTIx2pZA_WtTDcVkP7a9lRIXiofdGid1w3q_zp.-AtbRvqZuHZB4BNK__;!!AbgBjg!2-zF_m5WtsqL7NjDjRz1nsOFHr2cB7NdLvj3nmeA5aeLaSlsyFu7QhYw9MtfTFsT_yckWCYosmHySZ6wkMZq$)

Passcode: Uf^g#7FM

**Meeting summary**

## Quick recap

Michelle led a meeting with Sharma and Nikolozi to identify non-negotiable adjustments and processes for creating an OI report version that would be accurate and stand out from other financial tools. Sharma explained that the key differentiators for OI reports include removing non-recurring items (5-25% of total), excluding other operating income/expenses that aren't core operations, and standardizing cost line items like freight and SBC across peer companies. Sharma identified healthcare and software companies in North America as the easiest sectors to analyze due to their clean non-GAAP reporting, while sectors like oil and gas require more detailed manual work. The discussion also covered how to handle recurring expenses that may be extraordinary in nature, with Sharma explaining that judgment calls are made based on whether the expense is part of the company's normal operating model and how peers handle similar costs.

## Next steps

### Michelle

-

Schedule a follow-up session with Sharma, to discuss peer benchmarking versus Bain experience, focusing on streamlining that process and identifying the minimum viable steps required.

### Sharma,

-

Share the Claude skill (LLM tool for pulling non-GAAP adjustments) on the Teams channel for Michelle and the team to review its prompting and background code.

-

Loop in the colleague who built the Claude skill so he can receive guidance on improvements and share which sectors the skill handles most effectively.

-

Ask the colleague who built the Claude skill to identify and share which sectors (beyond healthcare and software) are most easily analyzed by the tool.

## Summary

### GLS OI Report Version Development

Michelle and Sharma discussed identifying non-negotiable adjustments and processes for creating an OI report version specific to GLS. The goal is to develop a version that will be accurate and widely accepted, distinguishing it from other tools. They mentioned considering different versions, including GLS, MVP, and post-MVP, with a focus on ensuring the GLS version meets specific standards.

### OI Financial Analysis Approach Differentiators

Sharma explained the key differentiators of OI's financial analysis approach, which involves making specific adjustments to create more actionable and accurate recommendations for clients. The process includes removing non-recurring items (ranging from 5-25%), standardizing COGS and SG&A categories across companies, and excluding transaction-related expenses. Sharma emphasized that these adjustments help provide a more refined and achievable target number for transformation potential rather than overestimating with generalized financial comparisons.

### Non-GAAP Reporting Sector Analysis

Sharma identified healthcare companies in North America and software companies as the easiest sectors for non-GAAP financial reporting due to their standardized and detailed disclosure practices in press releases and 10-K filings. Sharma noted that these sectors provide non-GAAP numbers at lower levels (S&M, SG&A, R&D) more consistently than other industries, with Claude, an LLM tool, being particularly effective at extracting these adjustments from standardized companies.

### Claude Skill Performance Review

Sharma explained that their current Claude skill works well with companies that report clean data, particularly in the healthcare and software sectors in America, but becomes slower and less effective when too many sector-specific conditions are included in the prompt. The team has not actively deployed the skill yet, as they are still testing it, and it currently achieves about 70-80% accuracy with good quality reports. Sharma agreed to share the current skill details and seek guidance from their colleague to improve sector-specific analysis, particularly for consumer goods and retail sectors in America where non-GAAP reporting is more standardized. Nikolozi raised a question about how to handle ongoing material costs, such as long-term litigation or safety violations, which are not part of normal operating activities but continue for extended periods, though this discussion was not fully resolved in the transcript.

### Recurring Expenses in Financial Analysis

Sharma explained the approach for handling recurring expenses in financial analysis, particularly when determining whether to include litigation costs in P&L calculations. He outlined that expenses should be included if they are core to the business model and industry standard, while non-recurring or extraordinary items should be excluded. Sharma also emphasized the importance of comparing current expenses to historical trends to identify abnormalities or spikes that may require further investigation. The conversation ended with Michelle indicating they would need another session to discuss peer benchmarking versus Bain experience in more detail.
