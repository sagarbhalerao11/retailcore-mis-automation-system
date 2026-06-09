from ingestion import process_data
from analytics import run_analytics
from charts import generate_all_charts

sales, inventory, returns = process_data()

metrics = run_analytics(
    sales,
    inventory,
    returns
)

chart_paths = generate_all_charts(
    metrics
)

print(chart_paths)
