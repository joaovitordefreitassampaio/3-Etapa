import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("Tabela4.csv", sep=";", decimal=",", encoding="latin1", skiprows=1)
df = df.dropna(axis=1, how="all").dropna(subset=["Sigla"])

anos = [c for c in df.columns if c.isdigit()]
variaveis = [c for c in df.columns if c not in anos]

df_longo = df.melt(id_vars=variaveis, value_vars=anos, var_name="Ano", value_name="IDH")
df_longo["Ano"] = df_longo["Ano"].astype(int)

fig, ax = plt.subplots(figsize=(12, 7))
for sigla, grupo in df_longo.groupby("Sigla"):
    ax.plot(grupo["Ano"], grupo["IDH"], marker="o", markersize=3, linewidth=1.5, label=sigla)

ax.set_title("Evolução do IDH por estado (1991–2024)")
ax.set_xlabel("Ano")
ax.set_ylabel("IDH")
ax.set_ylim(0.3, 0.9)
ax.legend(ncol=3, bbox_to_anchor=(1.02, 1), loc="upper left", title="UF")
fig.tight_layout()
fig.savefig("idh_todos_estados.png", dpi=150)

mg = df_longo[df_longo["Sigla"] == "MG"]

fig, ax = plt.subplots(figsize=(10, 5.5))
ax.plot(mg["Ano"], mg["IDH"], marker="o", linewidth=2, color="steelblue")
ax.set_title("Evolução do IDH de Minas Gerais (1991–2024)")
ax.set_xlabel("Ano")
ax.set_ylabel("IDH")
fig.tight_layout()
fig.savefig("idh_minas_gerais.png", dpi=150)

plt.show()
