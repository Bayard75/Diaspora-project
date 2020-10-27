import pandas as pd

df = pd.DataFrame(columns=['Pays de residence', "Pays d'origine", "Age Minimum", "Age Maximum", "Nombre d'utilisateur Total", "Hommes", "Femmes"])
new_row = {"Pays de residence":"a", "Pays d'origine":"D", "Age Minimum":"f","Age Maximum":"F","Nombre d'utilisateur Total":"3", "Hommes":'5', "Femmes":"5"}
df = df.append(new_row, ignore_index=True)
print(df)