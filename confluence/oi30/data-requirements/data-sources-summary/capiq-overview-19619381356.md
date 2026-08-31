---
title: "CapIQ overview"
confluence_id: 19619381356
confluence_url: https://bainco.atlassian.net/wiki/spaces/OI30/pages/19619381356
version: 1
updated: 2026-07-12T21:31:14.621Z
---

# CapIQ overview

[View in Confluence](https://bainco.atlassian.net/wiki/spaces/OI30/pages/19619381356)

To add here data source overview, example (to be modified as this is VERY OLD):

-

Data Source Overview

-

Sources of Input

-

Accessing XpressFeed Loader

  -

Requirements

  -

Instructions

-

DB Endpoints

  -

Full List

-

ETL Process

  -

Ingestion Process

  -

Cleaning Process

-

Storage of Results

  -

Table 1 – raw companies

  -

Table 2 – raw financials

  -

Table 3 – clean companies

  -

Table 4 – time series financials full

  -

Table 5 – time series financials latest

-

Attachments

## **Data Source Overview**

CapIQ is the most important data source in the Company Data Platform. It contains the largest number of rows and columns. We update CapIQ daily for its company firmographics, company financials, and financial history.

The processed financials are all separate paths by currency.

## **Sources of Input**

|

**Data Source**

 |

**Type of Source**

 |

**Type of Data**

 |

**Magnitude of Total Rows**

 |

**Pull Frequency**

 |
|---|---|---|---|---|
|

CapIQ

 |

XpressFeed

 |

Company Information

 |

10s of millions

 |

Monthly

 |
|

CapIQ

 |

XpressFeed

 |

Company Financials

Company Financial History

 |

2 billion

 |

Daily

 |

## **Accessing XpressFeed Loader**

### Requirements

1.

Some sort of remote desktop tool (example uses Microsoft Remote Desktop)

### Instructions

1.

Navigate to the AWS EC2 page and locate the instance named `xpressfeed-client-ec2`

1.

In the remote desktop tool, add a connection (add a PC) with the following information:

  1.

PC Name: `{private IP of the EC2 Instance above}`

  1.

User account: `Administrator`

1.

Launch the connection and the application will be open.

## **DB Endpoints**

```
--Companies
ciqcompany
ciqcompanystatustype
ciqcompanytype
ciqcountrygeo
ciqcompanycrossref
ciqcompanyindustrytree
ciqsubtype
ciqCompanyIndustry
ciqSubTypeToGICS
ciqindustrytosic
ciqcompanyultimateparent
--Financials
ciqfininstance
ciqfininstancetocollection
ciqfincollectiondata
ciqprivatefindata
```

### **Full List**

## **ETL Process**

All scripts for the CapIQ ETL process are located in [this repo](https://github.com/Bain/ng-python-CDP-ETL-ELT/tree/dev/etl_layer/capiq). The scripts are run in this order for the two separate pipelines.

**Companies Pipeline (Run monthly)**

1.

`capiq_companies_unload.py`

1.

`capiq_cleaning.py`

**Financials Pipeline (Run daily)**

1.

`capiq_financials_unload.py`

1.

`capiq_timeseries_incremental.py`

### **Ingestion Process**

All XpressFeed data comes from an RDS instance that houses both financial and company information on capiq. Each `*_unload.py` script takes data from the RDS instance and moves it into S3 buckets.

Financial data ingestion needs to be chunked because the input is so large.

### **Cleaning Process**

In order to clean the **company information**, each company is heavily enriched with many different financial metrics, signals, and transactional data. Additionally, the companies need to be mapped to the proper country names, sector taxonomy, GICS and SIC statuses.

Cleaning the **financial information** requires each row be mapped to the proper data item name (revenue, ebitda, etc), and each value be converted to the proper units. Most rows are converted to a TARGET_CURRENCY, but some values are percentages, days, or a simple count.

## **Storage of Results**

For each of the tables that are created as a result of the ETL Process (including the raw table) describe the table (high level description or schema or a snippet or anything)

### **Table 1 – raw companies**

**Location: **`??`

Contains companies that are uniquely identified by a `companyid` or `duns_number`. This table contains basic firmographic information, hierarchical data, and raw, unmapped GICS information. The tables that build the raw companies table are also stored in ??.

### **Table 2 – raw financials**

**Locations:**

-

`??`

-

`??`

Contains financial line items that are uniquely identified by a `finperiodid`. Each row refers to a `companyid` and contains information for a specific metric (revenue, ebitda, etc.). Metrics are captured in many different time periods and currencies.

This table is essentially a copy of the data – no currency conversion occurs.

### **Table 3 – clean companies**

**Location:** `??`

In addition to the basic firmographics and hierarchical data, the clean companies table contains different financial metrics, signals, and transactional data. It also contains the properly mapped GICS, SIC, country, and sector taxonomy information.

Each row is now uniquely identified by a `id_ciq`.

### Table 4 – time series financials full

**Location:** `??`

Each row contains a `finperiodid`, a company id, a mapped data item (or metric), and a proper unit (TARGET_CURRENCY if money value).

### Table 5 – time series financials latest

**Location:** `??`

Each row contains a `finperiodid`, a year, a company id, a mapped data item (or metric), and a proper unit (TARGET_CURRENCY if money value).

This table contains only financial information of the most recent year of financial information for the company

## **Attachments**

This section contains helpful documents like Taxonomy mappings:
