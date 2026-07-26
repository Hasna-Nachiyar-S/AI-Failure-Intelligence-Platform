from backend.utils.data_loader import load_student
from backend.analytics.analytics import failure_count

df = load_student()

print(failure_count(df, "school"))