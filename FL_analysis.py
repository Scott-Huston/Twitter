import seaborn as sns

df = pd.read('master_data.csv')

ax1 = sns.lineplot(x='Day', y='Gains/Follow', data = df, ci=95)

ax2 = sns.lineplot(x='Day', y = 'Follower', data = df, ci=95)

ax3 = sns.lineplot(x='Day', y = 'Gains', data = df)

ax4 = sns.regplot(x='Follows', y = 'Gains', data=df, ci=95)

# Getting average gain
total_gain = df.Follower.iloc[-1] - df.Follower.iloc[0]
days = len(df)
avg_gain = total_gain/days
