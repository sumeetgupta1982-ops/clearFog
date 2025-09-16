import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Parameters
labels = ['Quality', 'Planning', 'Schedule', 'Resource', 'Risk',
          'Technical', 'Communication', 'Proactiveness', 'Responsiveness',
          'Escalation', 'Flexibility']
num_vars = len(labels)

st.title('Kellton Project Experience Ratings (Radar Chart)')
st.write('Enter ratings for each respondent (0-4, where 0=Missing, 1=Very Low, 2=Low, 3=Medium, 4=High)')

respondents = st.text_input('Respondent names (comma separated)', 'R1, R2, R3, R4')
respondent_list = [r.strip() for r in respondents.split(',') if r.strip()]

# Input fields for each respondent
ratings = {}
for respondent in respondent_list:
    st.subheader(f'Ratings for {respondent}')
    values = []
    cols = st.columns(4)
    for i, label in enumerate(labels):
        col = cols[i % 4]
        val = col.number_input(f'{label}', min_value=0, max_value=4, value=3, key=f'{respondent}_{label}')
        values.append(val)
    ratings[respondent] = values

# Compute averages
all_scores = np.array(list(ratings.values()))
averages = np.mean(all_scores, axis=0)

# Find low (<2) and high (>3) average scores
avg_with_labels = list(zip(labels, averages))
low_vars = [(label, avg) for label, avg in avg_with_labels if avg < 2]
high_vars = [(label, avg) for label, avg in avg_with_labels if avg > 3]

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

st.write('### Average score for each variable:')
for label, avg in avg_with_labels:
    st.write(f'{label}: {avg:.2f}')

if low_vars:
    st.write('### Low average scores (below 2):')
    for label, avg in low_vars:
        st.write(f'{label}: {avg:.2f} - {comments.get(label, "")}')
if high_vars:
    st.write('### High average scores (above 3):')
    for label, avg in high_vars:
        st.write(f'{label}: {avg:.2f} - {comments.get(label, "")}')

# Radar chart
angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
angles += angles[:1]

fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))

line_styles = ['-', '--', '-.', ':']
markers = ['o', 's', 'D', '^']
colors = ['b', 'g', 'r', 'm', 'c', 'y', 'k']
for idx, (respondent, values) in enumerate(ratings.items()):
    vals = values + [values[0]]
    ax.plot(
        angles,
        vals,
        label=respondent,
        linewidth=2,
        linestyle=line_styles[idx % len(line_styles)],
        marker=markers[idx % len(markers)],
        color=colors[idx % len(colors)]
    )
    ax.fill(angles, vals, alpha=0.10, color=colors[idx % len(colors)])

# Plot average line
avg_values = averages.tolist() + [averages[0]]
ax.plot(angles, avg_values, label='Average', color='orange', linewidth=3, linestyle='-', marker='*', markersize=10)

# Add average score as label at each variable's position
for idx, (label, avg) in enumerate(avg_with_labels):
    angle = angles[idx]
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

# Highlight low and high average points with comments
for label, avg in low_vars:
    idx = labels.index(label)
    angle = angles[idx]
    ax.scatter([angle], [avg], color='red', s=120, zorder=10, label=f'Low: {label}')
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

ax.set_xticks(angles[:-1])
ax.set_xticklabels(labels)
ax.set_yticks([0, 1, 2, 3, 4])
ax.set_yticklabels(['Very Low', 'Low', 'Medium', 'High', 'Very High'])

handles, legend_labels = ax.get_legend_handles_labels()
from collections import OrderedDict
by_label = OrderedDict(zip(legend_labels, handles))
ax.legend(by_label.values(), by_label.keys(), loc='upper left', bbox_to_anchor=(1.05, 1.05), fontsize=12, title="Respondents & Averages")
ax.set_title('Kellton Project Experience Ratings (Radar Chart)', size=14, y=1.08)

st.pyplot(fig)
