---
title: "Workshop: Data calculations"
confluence_id: 19735543865
confluence_url: https://bainco.atlassian.net/wiki/spaces/OI30/pages/19735543865
version: 2
updated: 2026-08-21T05:39:47.588Z
---

# Workshop: Data calculations

[View in Confluence](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19735543865)

Meeting Date: Aug 18, 2026

Zoom link: [https://bain.zoom.us/rec/share/6xD-LxSjQ5N1e01Rm9t76LmQ359SwfaqGuvrThE_5xb3saKdxIY0JMXA0N6r166B.P3wwttzo8yXMVoT7](https://urldefense.com/v3/__https:/bain.zoom.us/rec/share/6xD-LxSjQ5N1e01Rm9t76LmQ359SwfaqGuvrThE_5xb3saKdxIY0JMXA0N6r166B.P3wwttzo8yXMVoT7__;!!AbgBjg!3OEjHjFh1AGJGqMNd6ayitZd0L2byzoebrDt_LN0l4i09UU7yt3cCK8peBN-QUdkCtC0pUyhR8EdZOjmySZs$)

Passcode: 3?fESe8#

Zoom-generated Notes:

**Meeting summary**

## Quick recap

The meeting focused on discussing the OI (Operating Income) calculation methodology and adjustment processes for benchmarking across peer companies. Noah and Akhil explained their four-step approach: peer selection, data collection and adjustment, identifying savings, and completing outputs. They detailed the two main types of adjustments: removing one-time non-recurring costs (like restructuring, impairments, and acquisition-related expenses) from company financials, and aligning different reporting structures across peer companies to make metrics comparable. Akhil demonstrated specific examples using Coca-Cola and other companies to show how they identify and adjust non-GAAP financial measures, handle different reporting standards between US and European companies, and manage cost bucket re-allocation when companies report expenses in different categories. The team discussed their approach to standardizing financial reporting across geographies and accounting standards, with a focus on creating comparable metrics while maintaining accuracy to the target company's reporting structure.

## Next steps

### Noah

- Collaborate with Sharma, to review the analysis repository and identify what has not yet been captured from VCC, and build out the same spreadsheet format of metric calculations to pass to the development team.
- Plan a future session to go into more depth on metric calculation methodology, size of prize calculations, and triangulation with cost bar breakdown.
- Confirm availability and timing for the next day's session, targeting a morning slot (around 10am Singapore time) for topics requiring his input.

### SNG

- Gather the development team (Giorgi, Nico, Sandeep, Michelle) to assess complexity estimates for the calculations discussed and report back to Noah.
- Obtain the VCC codebase and share it with the development team as a reference before they begin writing the calculation engine.
- Check with Fritz to quickly revalidate the designs during the afternoon session.
- Organize a session for the next day focusing on refining the MVP plan, laser-focusing on calculations (what is in vs. out), and adding an adjustments stream to the MVP plan.

### Sharma,

- Share the Aptiv and Coca-Cola adjustment summary Excel workbooks with the development team (ensuring no confidential data is included).
- Share additional adjustment summary Excel workbooks if the team can easily digest the initial ones shared.
- Share the Claude-based peer comparability skill file directly with the team.
- Set up a separate session to walk through the A1OI methodology and how CapIQ numbers are manipulated to create comparable COGS and SG&A.

### Collaboration

- Joanna and Ramba (referenced by SNG): Send the latest visuals/designs to the team ahead of the next day's session.

## Summary

### OI 3.0 Product Workshop Discussion

The team discussed the OI 3.0 product workshop, focusing on calculation methodologies and adjustment approaches. Noah explained the four-step process for their typical 48-hour workflow, including peer selection, data collection and adjustment, identifying savings, and completing outputs. The adjustment process involves removing one-time costs and non-recurring items from company financials to ensure comparability across peers. Akhil was brought in to provide detailed examples and address questions about the complexity of calculations and adjustments.

### Financial Cost Adjustment Standards

Noah explained two types of financial adjustments: aligning cost bucketing definitions between the target company and peer set, and standardizing reporting structures to match the target company's approach. The team discussed how they typically align peer companies to the target's reporting structure rather than creating hybrid approaches, though exceptions can occur when peers lack sufficient granularity. Noah and Sharma clarified that labor cost re-bucketing often relies on operational KPIs when available, industry-specific assumptions when data isn't available, or documented industry guidelines, with adjustments being carefully tracked through reconciliation tables when modifications are made to the target company's reporting structure.

### Financial Reporting Standardization Strategy

The team discussed their approach to standardizing financial reporting across different companies and regions by creating non-GAAP or non-IFRS adjusted financials. Noah explained they remove non-recurring items to create comparable performance metrics across geographies, while Sharma detailed their three-step process: removing non-recurring items, comparing financial line items across peers, and synchronizing financial structures. The discussion covered how they handle different reporting structures, particularly noting challenges with European companies that may not clearly label non-GAAP adjustments, requiring manual analysis of footnotes and 10-K reports to identify appropriate adjustments.

### Non-GAAP Adjustment Approach Discussion

Sharma explained the approach to non-GAAP adjustments, noting that stock-based compensation (SBC) should only be removed if the target company includes it in their non-GAAP adjustments, not based on peer company practices. He clarified that in rare cases where reporting structures differ significantly between the target and peers, adjustments may be made to the target's financials, but this is avoided whenever possible to maintain transparency for CXOs. Sharma also discussed challenges in comparing companies with different reporting structures, particularly when some separate out employee expenses and D&A expenses while others do not.

### Industry-Specific Financial Calculation Nuances

Sharma explained that different industries require specific nuances in financial calculations, particularly for healthcare where the cost base denominator includes all costs versus just cost of goods sold for other sectors. Nikolozi categorized adjustment approaches into three types: removals of non-recurring items (consistent across industries), reclassification within cost categories, and complex re-bucketing across multiple cost categories. The team clarified that while industry-specific adjustments exist, the core calculation methods remain similar across sectors, with complexity primarily arising from qualitative factors and peer-specific requirements rather than fundamental calculation differences.

### Income Statement Analysis Methodology

Sharma explained the methodology for analyzing income statements by focusing on trade receivables and trade payables from balance sheets. He demonstrated the process of adjusting net accounts receivable figures by removing allowances and provisions to isolate only the trade aspects of the business using examples from Coca-Cola and PepsiCo's financial reports. Sharma also addressed how to handle LTM numbers in 10Q filings, explaining the need to adjust for differences in detail between annual reports and quarterly filings.

### LTM Trade Receivables Calculation Methodology

Sharma explained the methodology for calculating trade receivables and payables in LTM reports when detailed granularity is not available. The team uses proportions from annual reports to adjust LTM numbers, applying the same approach across balance sheet and income statement items. Sharma demonstrated how they calculate trade receivables by taking the proportion of trade receivables to total receivables from the 10K and applying it to LTM figures, and described a similar proportional approach for payables and other income statement adjustments.

### Income Statement Analysis Methodology

Sharma explained the income statement analysis methodology, focusing on reconciliation checks between their calculated adjusted EBIT and the company-reported numbers. He demonstrated how they identify and adjust non-GAAP, non-recurring items while maintaining consistency with the client's reporting structure. The team discussed using GPT and Claude for peer selection, with Sharma showing how they refine the peer list based on business comparability and reporting structure consistency. The group also addressed the limitations of using Cap IQ data directly, noting that significant adjustments are needed to create comparable COGS and SG&A figures.
