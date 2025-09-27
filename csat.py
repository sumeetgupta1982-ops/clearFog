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

# Compute averages for each variable
all_scores = np.array(list(data.values()))
averages = np.mean(all_scores, axis=0)

# Find low (<2) and high (>3) average scores
avg_with_labels = list(zip(labels, averages))
low_vars = [(label, avg) for label, avg in avg_with_labels if avg < 2]
high_vars = [(label, avg) for label, avg in avg_with_labels if avg > 3]

# Example comments for each variable (customize as needed)
comments = {
    'Quality': 'Quality of deliverables and outcomes.',
    'Planning': 'Effectiveness of project planning.',
    'Schedule': 'Adherence to project timelines.',
    'Resource': 'Resource allocation and management.',
    'Risk': 'Risk identification and mitigation.',
    'Technical': 'Technical expertise and solutions.',
    'Communication': 'Clarity and frequency of communication.',
    'Proactiveness': 'Initiative and forward-thinking.',
    'Responsiveness': 'Speed of response to issues.',
    'Escalation': 'Handling of escalations.',
    'Flexibility': 'Ability to adapt to changes.'
}

print("Average score for each variable:")
for label, avg in avg_with_labels:
    print(f"{label}: {avg:.2f}")
print("\nLow average scores (below 2):")
for label, avg in low_vars:
    print(f"{label}: {avg:.2f} - {comments.get(label, '')}")
print("\nHigh average scores (above 3):")
for label, avg in high_vars:
    print(f"{label}: {avg:.2f} - {comments.get(label, '')}")


fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))

# Plot each respondent
line_styles = ['-', '--', '-.', ':']
markers = ['o', 's', 'D', '^']
colors = ['b', 'g', 'r', 'm']
for idx, (respondent, values) in enumerate(data.items()):
    values += values[:1]  # Close the circle
    ax.plot(
        angles,
        values,
        label=respondent,
        linewidth=2,
        linestyle=line_styles[idx % len(line_styles)],
        marker=markers[idx % len(markers)],
        color=colors[idx % len(colors)]
    )
    ax.fill(angles, values, alpha=0.10, color=colors[idx % len(colors)])

# Plot average line
avg_values = averages.tolist() + [averages[0]]
ax.plot(angles, avg_values, label='Average', color='orange', linewidth=3, linestyle='-', marker='*', markersize=10)

# Add labels
ax.set_xticks(angles[:-1])
ax.set_xticklabels(labels)
ax.set_yticks([0, 1, 2, 3, 4])
ax.set_yticklabels(['Very Low', 'Low', 'Medium', 'High', 'Very High'])




# Highlight low (<2) and high (>3) average points and add comments as annotation
for label, avg in low_vars:
    idx = labels.index(label)
    angle = angles[idx]
    ax.scatter([angle], [avg], color='red', s=120, zorder=10, label=f'Low: {label}')
    # Add comment annotation
    ax.annotate(
        comments.get(label, ''),
        xy=(angle, avg),
        xytext=(10, -20),
        textcoords='offset points',
        ha='left',
        va='top',
        fontsize=10,
        color='red',
        bbox=dict(facecolor='white', edgecolor='red', boxstyle='round,pad=0.2', alpha=0.7)
    )
for label, avg in high_vars:
    idx = labels.index(label)
    angle = angles[idx]
    ax.scatter([angle], [avg], color='green', s=120, zorder=10, label=f'High: {label}')
    # Add comment annotation
    ax.annotate(
        comments.get(label, ''),
        xy=(angle, avg),
        xytext=(10, 10),
        textcoords='offset points',
        ha='left',
        va='bottom',
        fontsize=10,
        color='green',
        bbox=dict(facecolor='white', edgecolor='green', boxstyle='round,pad=0.2', alpha=0.7)
    )

# Add average score as label at each variable's position
for idx, (label, avg) in enumerate(avg_with_labels):
    angle = angles[idx]
    # Offset label slightly away from the point
    offset = 0.25
    ax.text(
        angle,
        avg + offset,
        f"{avg:.2f}",
        color='orange',
        fontsize=11,
        fontweight='bold',
        ha='center',
        va='center',
        bbox=dict(facecolor='white', edgecolor='orange', boxstyle='round,pad=0.2', alpha=0.7)
    )

# Add legend and title
handles, legend_labels = ax.get_legend_handles_labels()
# Remove duplicate labels
from collections import OrderedDict
by_label = OrderedDict(zip(legend_labels, handles))
ax.legend(by_label.values(), by_label.keys(), loc='upper left', bbox_to_anchor=(1.05, 1.05), fontsize=12, title="Respondents & Averages")
ax.set_title('Kellton Project Experience Ratings (Radar Chart)', size=14, y=1.08)

plt.show()

