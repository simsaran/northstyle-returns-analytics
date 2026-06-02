# The Real Cost of Free Returns
### NorthStyle Co. Customer Returns and Profitability Analytics

I ordered three sizes of the same jeans online last month. Kept one. Returned two. Free shipping both ways. The whole thing cost me nothing extra. On the way to the post office I started thinking about what that transaction actually cost the retailer. Because it definitely was not free for them.

Most retailers offer free returns because it increases purchase confidence. More people buy when they know they can return. The question is whether the extra sales from offering free returns outweigh the cost of processing them. And the answer is different for different customers.

This project builds the analysis that shows exactly which customers are genuinely profitable and which ones only look profitable until you account for what their returns actually cost.

---

## What this is

A customer returns and profitability analytics project for a fictional Canadian fashion retailer called NorthStyle Co. 12 months of order data. 1,800 customers segmented into four groups based on their return behaviour. A true profitability model that subtracts return processing costs, return shipping, and returned item value from each customer's gross revenue. A scenario model comparing three different returns policy options. A business case document with findings and recommendations.

---

## Live app

[Launch the NorthStyle Returns Analytics Dashboard](https://northstyle-returns-analytics-2026.streamlit.app/)

---

## What the data showed

Not all customers are equally profitable. Some spend a lot but return even more. The four segments tell very different stories.

| Segment | Size | Avg Revenue | Avg Return Rate | Avg Net Profit | % Profitable |
|---------|------|------------|----------------|---------------|-------------|
| Loyal Buyer | 540 (30%) | $809 | 7.3% | $376 | 99.4% |
| Occasional Returner | 630 (35%) | $600 | 20.8% | $185 | 87.0% |
| Serial Returner | 360 (20%) | $1,043 | 36.4% | $137 | 70.6% |
| Bracket Buyer | 270 (15%) | $1,373 | 45.0% | $79 | 57.4% |

Bracket Buyers generate the highest average revenue per customer. But after return processing costs, return shipping, and returned item value are subtracted, their net profit is $79, the lowest of any segment. Loyal Buyers deliver 4.7 times more net profit per customer despite spending less.

17% of all customers are net unprofitable after return costs are fully accounted for.

---

## The scenario model

Three policy options were modelled against the current baseline.

Scenario A keeps free returns for everyone. 17% of customers remain unprofitable.

Scenario B applies a $12 return fee to Serial Returners with return rates above 50%. The cost saving is partially offset by reduced purchase frequency from that segment.

Scenario C replaces free returns for Bracket Buyers with a Fit Guarantee, one free exchange per order instead of a full return. This reduces the multi-item return behaviour while retaining the segment. It produces the strongest net profit improvement and is the recommended approach.

---

## What the four tabs cover

Customer Segments shows the four segment breakdown with return rates, customer counts, and the NPS-equivalent satisfaction comparison across segments.

True Profitability shows the revenue versus net profit gap by segment, the percentage of profitable customers in each group, and the full customer-level profit distribution so you can see exactly where the unprofitable customers sit.

Return Patterns shows return rates by product category, the monthly return volume trend overlaid against total orders, and the breakdown of return reasons.

Policy Scenarios shows the three-scenario comparison with net profit, revenue impact, and cost saving side by side so the trade-offs are immediately visible.

---

## Files in this repo

| File | What it is |
|------|-----------|
| app.py | Streamlit app with four interactive analytics tabs |
| order-data.csv | 10,592 order records with return status, costs, and net profit per order |
| customer-data.csv | 1,800 customer records with segment, total revenue, return rate, and net profit |
| segment-summary.csv | Aggregated metrics by segment |
| category-analysis.csv | Return rates and costs by product category |
| scenario-model.csv | Three policy scenarios with revenue impact, cost saving, and net profit |
| key-findings.json | Headline findings including return rate and profitability metrics |
| business-case.pdf | Full business analysis report with segment findings and recommendations |
| generate-data.py | Python script that built the synthetic dataset |
| requirements.txt | Package dependencies |

---

## Skills this project demonstrates

Customer segmentation based on behavioural data. Unit economics and true profitability modelling. Ecommerce return cost analysis. Scenario modelling and policy recommendation. Python for data generation and analysis with pandas. Plotly for interactive charts. Streamlit dashboard design and deployment. Business case writing for a non-technical audience.

---

## About this project

Part of a portfolio series built while job searching in Canada after graduating from the University of Waterloo.

Prepared by Simran Saran. Targeting business analyst, data analyst, and ecommerce analytics roles across Canada.

All data is synthetic. NorthStyle Co. is fictional. Return rates and cost structures are modelled on publicly available ecommerce industry benchmarks.
