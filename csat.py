import matplotlib.pyplot as plt
import numpy as np

# Parameters
labels = ['Quality', 'Planning', 'Schedule', 'Resource', 'Risk', 
          'Technical', 'Communication', 'Proactiveness', 'Responsiveness', 
'Escalation', 'Flexibility']
num_vars = len(labels)

# Data for each respondent
data = {
    'R1': [3, 3, 3, 3, 3, 4, 3, 3, 3, 3, 3],
    'R2': [2, 3, 3, 1, 1, 2, 3, 1, 3, 1, 4],
    'R3': [3, 3, 3, 2, 3, 3, 3, 3, 0, 0, 0],  # Missing values as 0
    'R4': [3, 3, 3, 2, 3, 4, 4, 3, 3, 3, 3]
}

# Compute angle for each axis
angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
angles += angles[:1]  # Close the circle

fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))

# Plot each respondent
for respondent, values in data.items():
    values += values[:1]  # Close the circle
    ax.plot(angles, values, label=respondent)
    ax.fill(angles, values, alpha=0.3)  # Slight shading for 3D effect

# Add labels
ax.set_xticks(angles[:-1])
ax.set_xticklabels(labels)
ax.set_yticks([1, 2, 3, 4])
ax.set_yticklabels(['Very Low', 'Low', 'High', 'Very High'])

# Add legend and title
ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
ax.set_title('Kellton Project Experience Ratings (Radar Chart)', size=14, y=1.08)

plt.show()

