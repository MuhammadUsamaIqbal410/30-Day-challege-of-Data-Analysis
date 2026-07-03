import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.patches as mpatches
import numpy as np

df = pd.read_csv(r"C:\Users\Hp\Desktop\Project\Project 30\Day 01\Sample - Superstore.csv", encoding='latin-1')

print(df.shape)             # kitni rows, kitne columns
print(df.columns.tolist())  # column names 
df.head()                   # first five rows of the dataset

df.info()        # data types aur nulls ka overview
df.describe()    # numeric columns ki stats (min, max, mean)

print("Nulls:\n", df.isnull().sum())
print("\nDuplicates:", df.duplicated().sum())

df = df.drop_duplicates()   #duplicates drop karna

# Sub-Category ke hisaab se avg discount aur avg profit
subcat = df.groupby('Sub-Category').agg(
    Avg_Discount=('Discount', 'mean'),
    Avg_Profit=('Profit', 'mean'),
    Total_Sales=('Sales', 'sum')
).round(2).sort_values('Avg_Profit')

print(subcat)


# #Chart 1: Sub-Category vs Avg Profit (bar chart)
# plt.figure(figsize=(12,5))
# colors = ['#d9534f' if x < 0 else '#5cb85c' for x in subcat['Avg_Profit']]
# plt.bar(subcat.index, subcat['Avg_Profit'], color=colors)
# plt.xticks(rotation=45, ha='right')
# plt.axhline(0, color='black', linewidth=0.8, linestyle='--')
# plt.title('Avg Profit by Sub-Category (Red = Loss)')
# plt.tight_layout()
# plt.savefig('chart1_profit.png', dpi=150)
# plt.show()

# #Chart 2: Discount vs Profit scatter
# plt.figure(figsize=(8,5))
# sns.scatterplot(data=df, x='Discount', y='Profit', alpha=0.4, color='steelblue')
# plt.axhline(0, color='red', linewidth=0.8, linestyle='--')
# plt.title('Discount vs Profit (jitna discount, utna loss?)')
# plt.tight_layout()
# plt.savefig('chart2_discount_profit.png', dpi=150)
# plt.show()

# #Chart 3: Top 5 loss-making sub-categories
# top5_loss = subcat[subcat['Avg_Profit'] < 0].head(5)
# plt.figure(figsize=(8,4))
# plt.barh(top5_loss.index, top5_loss['Avg_Profit'], color='#d9534f')
# plt.title('Top 5 Loss-Making Sub-Categories')
# plt.xlabel('Avg Profit')
# plt.tight_layout()
# plt.savefig('chart3_top5loss.png', dpi=150)
# plt.show()



plt.rcParams.update({
    'figure.facecolor': '#0a0a0a',
    'axes.facecolor': '#111111',
    'axes.edgecolor': '#333333',
    'axes.labelcolor': '#888780',
    'xtick.color': '#888780',
    'ytick.color': '#888780',
    'text.color': '#ffffff',
    'grid.color': '#222222',
    'grid.linewidth': 0.5,
    'font.family': 'sans-serif',
    'font.size': 12,
})

# --- Chart 1: Avg Profit by Sub-Category ---
fig, ax = plt.subplots(figsize=(14, 6))
colors = ['#E24B4A' if x < 0 else '#1D9E75' for x in subcat['Avg_Profit']]
bars = ax.bar(subcat.index, subcat['Avg_Profit'], color=colors, 
            width=0.6, zorder=3)
ax.axhline(0, color='#444441', linewidth=1, linestyle='--')
ax.set_title('Avg Profit by Sub-Category', fontsize=16, 
            fontweight='bold', color='#ffffff', pad=20)
ax.set_xlabel('')
ax.set_ylabel('Avg Profit ($)', color='#888780')
ax.tick_params(axis='x', rotation=45)
ax.yaxis.grid(True, zorder=0)
ax.set_axisbelow(True)

# Value labels on bars
for bar, val in zip(bars, subcat['Avg_Profit']):
    ax.text(bar.get_x() + bar.get_width()/2, 
            bar.get_height() + (15 if val >= 0 else -25),
            f'${val:.0f}', ha='center', va='bottom',
            fontsize=9, color='#888780')

loss_patch = mpatches.Patch(color='#E24B4A', label='Loss')
profit_patch = mpatches.Patch(color='#1D9E75', label='Profit')
ax.legend(handles=[loss_patch, profit_patch], 
        facecolor='#111111', edgecolor='#333333',
        labelcolor='#ffffff', loc='upper left')

plt.tight_layout()
plt.savefig('chart1_profit.png', dpi=150, 
            facecolor='#0a0a0a', bbox_inches='tight')
plt.show()

# --- Chart 2: Discount vs Profit Scatter ---
fig, ax = plt.subplots(figsize=(10, 6))
scatter = ax.scatter(df['Discount'], df['Profit'], 
                    alpha=0.4, 
                    c=df['Profit'].apply(
                        lambda x: '#E24B4A' if x < 0 else '#1D9E75'),
                    s=20, zorder=3)
ax.axhline(0, color='#E24B4A', linewidth=1.5, 
        linestyle='--', alpha=0.8, label='Break-even line')
ax.set_title('Discount vs Profit — Where Does It Break?', 
            fontsize=16, fontweight='bold', color='#ffffff', pad=20)
ax.set_xlabel('Discount Level', color='#888780')
ax.set_ylabel('Profit ($)', color='#888780')
ax.xaxis.set_major_formatter(
    plt.FuncFormatter(lambda x, _: f'{int(x*100)}%'))
ax.yaxis.grid(True, zorder=0)
ax.set_axisbelow(True)
ax.legend(facecolor='#111111', edgecolor='#333333', labelcolor='#ffffff')

# Annotation
ax.annotate('Loss zone', xy=(0.45, -3000), fontsize=11,
            color='#E24B4A', fontstyle='italic')
ax.annotate('Profit zone', xy=(0.01, 5000), fontsize=11,
            color='#1D9E75', fontstyle='italic')

plt.tight_layout()
plt.savefig('chart2_discount_profit.png', dpi=150,
            facecolor='#0a0a0a', bbox_inches='tight')
plt.show()

# --- Chart 3: Top Loss-Making Sub-Categories ---
fig, ax = plt.subplots(figsize=(10, 5))
top5_loss = subcat[subcat['Avg_Profit'] < 0].head(5)
bars = ax.barh(top5_loss.index, top5_loss['Avg_Profit'],
            color='#E24B4A', height=0.5, zorder=3)
ax.axvline(0, color='#444441', linewidth=1)
ax.set_title('Loss-Making Sub-Categories', fontsize=16,
            fontweight='bold', color='#ffffff', pad=20)
ax.set_xlabel('Avg Profit ($)', color='#888780')
ax.xaxis.grid(True, zorder=0)
ax.set_axisbelow(True)

for bar, val in zip(bars, top5_loss['Avg_Profit']):
    ax.text(2, bar.get_y() + bar.get_height()/2,
            f'${val:.1f}', ha='left', va='center',
            fontsize=11, color='#ffffff', fontweight='bold')

plt.tight_layout()
plt.savefig('chart3_top5loss.png', dpi=150,
            facecolor='#0a0a0a', bbox_inches='tight')
plt.show()