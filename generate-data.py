import csv
import random
import json
from datetime import date, timedelta
import math

random.seed(2025)

# NorthStyle Co. -- fictional Canadian fashion retailer
# 12 months of order and return data
# January 2024 to December 2024

CATEGORIES = {
    "Denim":       {"avg_price": 89, "avg_cost": 32, "return_rate_base": 0.38, "processing_cost": 14},
    "Outerwear":   {"avg_price": 195, "avg_cost": 78, "return_rate_base": 0.22, "processing_cost": 18},
    "Tops":        {"avg_price": 49, "avg_cost": 16, "return_rate_base": 0.28, "processing_cost": 10},
    "Footwear":    {"avg_price": 135, "avg_cost": 52, "return_rate_base": 0.31, "processing_cost": 16},
    "Accessories": {"avg_price": 65, "avg_cost": 22, "return_rate_base": 0.12, "processing_cost": 8},
}

RETURN_REASONS = ["Wrong size", "Did not match description", "Changed mind", "Ordered multiple sizes", "Quality issue", "Arrived too late", "Found better price"]
RETURN_REASON_WEIGHTS = [35, 18, 14, 20, 7, 4, 2]

SEGMENT_PROFILES = {
    "Loyal Buyer":          {"weight": 30, "orders_mean": 8,  "orders_std": 2, "return_rate": 0.08, "avg_order_items": 1.4},
    "Occasional Returner":  {"weight": 35, "orders_mean": 5,  "orders_std": 2, "return_rate": 0.28, "avg_order_items": 1.8},
    "Serial Returner":      {"weight": 20, "orders_mean": 7,  "orders_std": 2, "return_rate": 0.58, "avg_order_items": 2.1},
    "Bracket Buyer":        {"weight": 15, "orders_mean": 6,  "orders_std": 2, "return_rate": 0.72, "avg_order_items": 3.2},
}

SHIPPING_COST = 8.50
FREE_RETURN_SHIPPING = 9.50

start_date = date(2024, 1, 1)
end_date   = date(2024, 12, 31)

customers = []
orders    = []
customer_id = 10001
order_id    = 20001

total_customers = 1800
segment_list = []
for seg, prof in SEGMENT_PROFILES.items():
    count = int(total_customers * prof["weight"] / 100)
    segment_list.extend([seg] * count)
random.shuffle(segment_list)

for segment in segment_list:
    prof = SEGMENT_PROFILES[segment]
    num_orders = max(1, int(random.gauss(prof["orders_mean"], prof["orders_std"])))
    total_revenue = 0
    total_returns = 0
    total_items   = 0
    total_return_cost = 0
    total_shipping_cost = 0
    customer_orders = []

    for _ in range(num_orders):
        day_offset = random.randint(0, 364)
        order_date = start_date + timedelta(days=day_offset)
        category = random.choices(list(CATEGORIES.keys()), weights=[20,15,30,20,15])[0]
        cat = CATEGORIES[category]

        num_items = max(1, int(random.gauss(prof["avg_order_items"], 0.5)))
        item_price = round(random.gauss(cat["avg_price"], cat["avg_price"] * 0.15), 2)
        item_price = max(20, item_price)
        order_value = round(item_price * num_items, 2)
        cogs = round(cat["avg_cost"] * num_items, 2)

        returned = random.random() < prof["return_rate"]
        return_reason = random.choices(RETURN_REASONS, weights=RETURN_REASON_WEIGHTS)[0] if returned else "Not returned"

        if segment == "Bracket Buyer":
            return_reason = "Ordered multiple sizes" if returned else "Not returned"

        items_returned = num_items - 1 if returned and num_items > 1 else (num_items if returned else 0)
        return_value = round(item_price * items_returned, 2) if returned else 0
        return_processing = round(cat["processing_cost"] * items_returned, 2) if returned else 0
        return_shipping   = FREE_RETURN_SHIPPING if returned else 0

        gross_profit = round(order_value - cogs - SHIPPING_COST, 2)
        net_profit   = round(gross_profit - return_value - return_processing - return_shipping, 2)

        total_revenue     += order_value
        total_returns     += return_value
        total_items       += num_items
        total_return_cost += return_processing + return_shipping
        total_shipping_cost += SHIPPING_COST

        orders.append({
            "Order ID":              f"ORD{order_id}",
            "Customer ID":           f"CUST{customer_id}",
            "Customer Segment":      segment,
            "Order Date":            order_date.strftime("%Y-%m-%d"),
            "Month":                 order_date.strftime("%Y-%m"),
            "Category":              category,
            "Items Ordered":         num_items,
            "Order Value CAD":       order_value,
            "COGS CAD":              cogs,
            "Shipping Cost CAD":     SHIPPING_COST,
            "Returned":              "Yes" if returned else "No",
            "Items Returned":        items_returned,
            "Return Value CAD":      return_value,
            "Return Processing Cost CAD": return_processing,
            "Return Shipping Cost CAD":   return_shipping,
            "Return Reason":         return_reason,
            "Gross Profit CAD":      gross_profit,
            "Net Profit CAD":        net_profit,
        })
        order_id += 1
        customer_orders.append(net_profit)

    actual_return_rate = round(total_returns / total_revenue * 100, 1) if total_revenue > 0 else 0
    total_net = round(sum(customer_orders), 2)

    customers.append({
        "Customer ID":         f"CUST{customer_id}",
        "Segment":             segment,
        "Total Orders":        num_orders,
        "Total Items Ordered": total_items,
        "Total Revenue CAD":   round(total_revenue, 2),
        "Total Returns CAD":   round(total_returns, 2),
        "Return Rate %":       actual_return_rate,
        "Total COGS CAD":      round(sum(cat["avg_cost"] for cat in CATEGORIES.values()) / len(CATEGORIES) * total_items, 2),
        "Total Return Processing Cost CAD": round(total_return_cost, 2),
        "Total Shipping Cost CAD":          round(total_shipping_cost, 2),
        "Total Net Profit CAD":             total_net,
        "Profitable":          "Yes" if total_net > 0 else "No",
    })
    customer_id += 1

orders.sort(key=lambda x: x["Order Date"])

with open('/home/claude/returns-analytics/order-data.csv','w',newline='') as f:
    w = csv.DictWriter(f, fieldnames=orders[0].keys())
    w.writeheader(); w.writerows(orders)

with open('/home/claude/returns-analytics/customer-data.csv','w',newline='') as f:
    w = csv.DictWriter(f, fieldnames=customers[0].keys())
    w.writeheader(); w.writerows(customers)

print(f"Orders: {len(orders)}")
print(f"Customers: {len(customers)}")

from collections import defaultdict
seg_agg = defaultdict(lambda:{"customers":0,"revenue":0,"returns":0,"net":0,"orders":0,"profitable":0})
for c in customers:
    s = c["Segment"]
    seg_agg[s]["customers"] += 1
    seg_agg[s]["revenue"]   += c["Total Revenue CAD"]
    seg_agg[s]["returns"]   += c["Total Returns CAD"]
    seg_agg[s]["net"]       += c["Total Net Profit CAD"]
    seg_agg[s]["orders"]    += c["Total Orders"]
    seg_agg[s]["profitable"] += 1 if c["Profitable"] == "Yes" else 0

print("\nSegment summary:")
seg_rows = []
for seg, d in seg_agg.items():
    n = d["customers"]
    avg_rev  = round(d["revenue"] / n, 2)
    avg_net  = round(d["net"] / n, 2)
    avg_ret  = round(d["returns"] / d["revenue"] * 100, 1) if d["revenue"] > 0 else 0
    prof_pct = round(d["profitable"] / n * 100, 1)
    print(f"  {seg}: {n} customers, avg revenue ${avg_rev}, avg net profit ${avg_net}, return rate {avg_ret}%, profitable {prof_pct}%")
    seg_rows.append({
        "Segment":                   seg,
        "Customer Count":            n,
        "% of Customer Base":        round(n / len(customers) * 100, 1),
        "Avg Orders per Customer":   round(d["orders"] / n, 1),
        "Avg Revenue per Customer CAD":   avg_rev,
        "Avg Return Rate %":         avg_ret,
        "Avg Net Profit per Customer CAD": avg_net,
        "% Customers Profitable":    prof_pct,
        "Total Segment Revenue CAD": round(d["revenue"], 2),
        "Total Segment Net Profit CAD": round(d["net"], 2),
    })

with open('/home/claude/returns-analytics/segment-summary.csv','w',newline='') as f:
    w = csv.DictWriter(f, fieldnames=seg_rows[0].keys())
    w.writeheader(); w.writerows(seg_rows)

# Category return analysis
cat_agg = defaultdict(lambda:{"orders":0,"returned":0,"revenue":0,"return_val":0,"proc_cost":0})
for o in orders:
    c = o["Category"]
    cat_agg[c]["orders"]    += 1
    cat_agg[c]["revenue"]   += o["Order Value CAD"]
    cat_agg[c]["return_val"] += o["Return Value CAD"]
    cat_agg[c]["proc_cost"] += o["Return Processing Cost CAD"]
    if o["Returned"] == "Yes":
        cat_agg[c]["returned"] += 1

cat_rows = []
for cat, d in cat_agg.items():
    ret_rate = round(d["returned"] / d["orders"] * 100, 1)
    cat_rows.append({
        "Category":           cat,
        "Total Orders":       d["orders"],
        "Total Returned":     d["returned"],
        "Return Rate %":      ret_rate,
        "Total Revenue CAD":  round(d["revenue"], 2),
        "Total Return Value CAD": round(d["return_val"], 2),
        "Total Processing Cost CAD": round(d["proc_cost"], 2),
        "Return Cost as % of Revenue": round((d["return_val"] + d["proc_cost"]) / d["revenue"] * 100, 1) if d["revenue"] > 0 else 0,
    })

with open('/home/claude/returns-analytics/category-analysis.csv','w',newline='') as f:
    w = csv.DictWriter(f, fieldnames=cat_rows[0].keys())
    w.writeheader(); w.writerows(cat_rows)

# Scenario modelling
total_rev  = sum(d["revenue"] for d in seg_agg.values())
total_net  = sum(d["net"] for d in seg_agg.values())
serial_customers = seg_agg["Serial Returner"]["customers"]
bracket_customers = seg_agg["Bracket Buyer"]["customers"]
serial_net   = seg_agg["Serial Returner"]["net"]
bracket_net  = seg_agg["Bracket Buyer"]["net"]
serial_rev   = seg_agg["Serial Returner"]["revenue"]
bracket_rev  = seg_agg["Bracket Buyer"]["revenue"]

return_fee = 12.00
fit_guarantee_cost_saving = 0.35

scenario_a_net = total_net
scenario_b_revenue_impact = serial_rev * (-0.18)
scenario_b_cost_saving    = serial_customers * 52
scenario_b_net = total_net + scenario_b_cost_saving + scenario_b_revenue_impact
scenario_c_revenue_impact = bracket_rev * 0.08
scenario_c_cost_saving    = bracket_customers * 38
scenario_c_net = total_net + scenario_c_cost_saving + scenario_c_revenue_impact

scenarios = [
    {"Scenario":"A — Keep free returns for everyone","Description":"No change to current policy","Revenue Impact CAD":0,"Cost Saving CAD":0,"Net Profit CAD":round(scenario_a_net,2),"vs Current":0,"Recommended":"Baseline"},
    {"Scenario":"B — Charge Serial Returners $12 return fee","Description":"Apply $12 return fee to any customer with return rate above 50%","Revenue Impact CAD":round(scenario_b_revenue_impact,2),"Cost Saving CAD":round(scenario_b_cost_saving,2),"Net Profit CAD":round(scenario_b_net,2),"vs Current":round(scenario_b_net-scenario_a_net,2),"Recommended":"Yes"},
    {"Scenario":"C — Offer Bracket Buyers a Fit Guarantee","Description":"Bracket Buyers get one free exchange per order instead of free returns — reduces serial ordering","Revenue Impact CAD":round(scenario_c_revenue_impact,2),"Cost Saving CAD":round(scenario_c_cost_saving,2),"Net Profit CAD":round(scenario_c_net,2),"vs Current":round(scenario_c_net-scenario_a_net,2),"Recommended":"Yes"},
]

with open('/home/claude/returns-analytics/scenario-model.csv','w',newline='') as f:
    w = csv.DictWriter(f, fieldnames=scenarios[0].keys())
    w.writeheader(); w.writerows(scenarios)

findings = {
    "total_customers": len(customers),
    "total_orders": len(orders),
    "total_revenue": round(total_rev, 2),
    "total_net_profit": round(total_net, 2),
    "overall_return_rate": round(sum(o["Return Value CAD"] for o in orders) / sum(o["Order Value CAD"] for o in orders) * 100, 1),
    "most_profitable_segment": max(seg_rows, key=lambda x: x["Avg Net Profit per Customer CAD"])["Segment"],
    "least_profitable_segment": min(seg_rows, key=lambda x: x["Avg Net Profit per Customer CAD"])["Segment"],
    "pct_customers_unprofitable": round(sum(1 for c in customers if c["Profitable"]=="No") / len(customers) * 100, 1),
    "scenario_b_improvement": round(scenario_b_net - scenario_a_net, 2),
    "scenario_c_improvement": round(scenario_c_net - scenario_a_net, 2),
    "highest_return_category": max(cat_rows, key=lambda x: x["Return Rate %"])["Category"],
}

with open('/home/claude/returns-analytics/key-findings.json','w') as f:
    json.dump(findings, f, indent=2)

print(f"\nKey findings:")
print(f"  Overall return rate: {findings['overall_return_rate']}%")
print(f"  Most profitable segment: {findings['most_profitable_segment']}")
print(f"  Least profitable segment: {findings['least_profitable_segment']}")
print(f"  % customers unprofitable: {findings['pct_customers_unprofitable']}%")
print(f"  Scenario B improvement: ${findings['scenario_b_improvement']:,.0f}")
print(f"  Scenario C improvement: ${findings['scenario_c_improvement']:,.0f}")
print("All files written.")
