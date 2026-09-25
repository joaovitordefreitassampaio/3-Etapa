import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

regioes = ["Norte", "Nordeste", "Sudeste", "Sul", "Centro-Oeste"]

bruto = pd.read_excel("Tabela 1.1.1.xls", engine="xlrd", header=None)
indicador_1 = bruto.iloc[8:41].copy()
indicador_1.columns = [
    "uf_regiao", "total", "total_branca", "total_preta_parda",
    "homem_branca", "homem_preta_parda", "mulher_branca", "mulher_preta_parda",
]
for col in indicador_1.columns[1:]:
    indicador_1[col] = pd.to_numeric(indicador_1[col], errors="coerce")

reg = indicador_1[indicador_1["uf_regiao"].isin(regioes)].copy()
reg["homens"] = (reg["homem_branca"] + reg["homem_preta_parda"]) / 2
reg["mulheres"] = (reg["mulher_branca"] + reg["mulher_preta_parda"]) / 2
reg_long = reg.melt(id_vars="uf_regiao", value_vars=["homens", "mulheres"], var_name="sexo", value_name="horas")

fig, ax = plt.subplots(figsize=(9, 5))
sns.barplot(data=reg_long, x="uf_regiao", y="horas", hue="sexo", ax=ax)
ax.set_title("Afazeres domésticos por região e sexo")
ax.set_xlabel("Região")
ax.set_ylabel("Horas / semana")
plt.tight_layout()
fig.savefig("atividade2_afazeres.png", dpi=150)
plt.show()

formacao_bruto = pd.read_excel("Tabela_3_Areas_gerais_de_formacao_na_graduacao.xlsx", header=None)
colunas = ["uf_regiao", "total", "total_homens", "total_mulheres"]

formacao_total = formacao_bruto.iloc[3:36, 0:4].copy()
formacao_stem = formacao_bruto.iloc[3:36, [0, 4, 5, 6]].copy()
formacao_saude = formacao_bruto.iloc[3:36, [0, 7, 8, 9]].copy()

for tabela in (formacao_total, formacao_stem, formacao_saude):
    tabela.columns = colunas
    for col in colunas[1:]:
        tabela[col] = pd.to_numeric(tabela[col])


def valor(tabela, coluna):
    return tabela.loc[tabela["uf_regiao"] == "Brasil", coluna].item()


brasil = pd.DataFrame({
    "area": ["Graduação (total)", "STEM", "Saúde / educação"],
    "homens": [valor(t, "total_homens") for t in (formacao_total, formacao_stem, formacao_saude)],
    "mulheres": [valor(t, "total_mulheres") for t in (formacao_total, formacao_stem, formacao_saude)],
})
brasil_long = brasil.melt(id_vars="area", var_name="sexo", value_name="pessoas")

fig, ax = plt.subplots(figsize=(9, 5))
sns.barplot(data=brasil_long, x="area", y="pessoas", hue="sexo", ax=ax)
ax.set_title("Brasil: pessoas com graduação, por área e sexo")
ax.set_xlabel("Área")
ax.set_ylabel("Pessoas")
plt.tight_layout()
fig.savefig("atividade3_formacao.png", dpi=150)
plt.show()

df = pd.read_excel("CD2022_Populacao_2010_Compatibilizada_20231222 (1).xlsx", header=2)
pop_estado = df.groupby(["COD. UF", "UF"], as_index=False).agg(
    populacao_2022=("População Censo 2022", "sum")
)
ordem = pop_estado.sort_values("populacao_2022", ascending=False)

fig, ax = plt.subplots(figsize=(9, 8))
sns.barplot(data=ordem, y="UF", x="populacao_2022", ax=ax, color="steelblue")
ax.set_title("População 2022 por UF")
ax.set_xlabel("Habitantes")
ax.set_ylabel("UF")
plt.tight_layout()
fig.savefig("atividade4_populacao.png", dpi=150)
plt.show()
