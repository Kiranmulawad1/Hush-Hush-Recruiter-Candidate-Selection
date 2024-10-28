import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import joblib

df1 = pd.read_csv('github_profiles.csv')
df2 = pd.read_csv('github_profiles2.csv')
df3 = pd.read_csv('github_profiles3.csv')

df_combined = pd.concat([df1, df2, df3], ignore_index=True)

df_selected = df_combined[['Followers', 'Following', 'No of Repos', 'Fork_avg']]

scaler = StandardScaler()
df_scaled = scaler.fit_transform(df_selected)

optimal_clusters = 2
kmeans = KMeans(n_clusters=optimal_clusters, init='k-means++', max_iter=300, n_init=10, random_state=0)
df_combined['kmeans'] = kmeans.fit_predict(df_scaled)
joblib.dump(kmeans, 'kmeans_model.pkl')