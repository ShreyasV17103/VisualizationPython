import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta

# Set random seed for reproducibility
np.random.seed(42)

# Parameters
airlines = ['Delta', 'United', 'American', 'Southwest', 'JetBlue', 'Alaska']
airports = ['JFK', 'LAX', 'ORD', 'ATL', 'DFW', 'DEN', 'SFO', 'SEA']
delay_causes = ['Weather', 'Technical', 'Crew', 'Security', 'Other', 'None']
start_date = datetime(2023, 1, 1)
end_date = datetime(2023, 12, 31)
days = (end_date - start_date).days + 1

# Generate flight-level data
records = []
for day in range(days):
    date = start_date + timedelta(days=day)
    for airport in airports:
        for airline in airlines:
            # Simulate number of flights per airline per airport per day
            n_flights = np.random.randint(8, 20)
            for _ in range(n_flights):
                flight_num = f"{airline[:2].upper()}{np.random.randint(100, 9999)}"
                delay_cause = np.random.choice(delay_causes, p=[0.2, 0.15, 0.1, 0.05, 0.1, 0.4])
                delay = 0 if delay_cause == 'None' else np.random.randint(10, 180)
                records.append({
                    'date': date.strftime('%Y-%m-%d'),
                    'airport': airport,
                    'airline': airline,
                    'flight_number': flight_num,
                    'delay_minutes': delay,
                    'delay_cause': delay_cause
                })

flights_df = pd.DataFrame(records)

# Save flight-level data
os.makedirs('data', exist_ok=True)
flights_df.to_csv('data/flight_delays.csv', index=False)

# Generate airport-level summary
airport_summary = flights_df.groupby(['airport', 'date']).agg(
    total_flights=('flight_number', 'count'),
    delayed_flights=('delay_minutes', lambda x: (x > 0).sum()),
    avg_delay=('delay_minutes', lambda x: x[x > 0].mean() if (x > 0).any() else 0)
).reset_index()
airport_summary.to_csv('data/airport_summary.csv', index=False)

print('Data generation complete. Files saved to data/.') 