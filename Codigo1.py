
#%% Codigo 1 - ANOVA de MEDIDAS REPETIDAS 

# Projeto acadêmico criado para o Curso de Análise de Dados Avançada da USP/EACH.

#%% Importando pacotes

import pingouin as pg
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats


#%% Importar arquivo

df_original = pd.read_excel('C:/Users/sandy/OneDrive/Documentos/GitHub/ProjetoEACH/ProjetoEACH/Codigo1.xlsx')

#%% Analisando o dataframe importado 

df = df_original.reset_index()
df = df.drop(columns = ['index'])

#%% Analisando o boxplot D0(inicio) e D120 (fim) dos dois grupos

sns.boxplot(x = "Grupo", y = "HBA1C D0", data = df)
sns.boxplot(x = "Grupo", y = "HBA1C D120", data = df)

#%% Analisando comportamento Hemoglobina Glicada somente do Grupo Controle

a = df.loc[df['Grupo']== 'Controle','HBA1C D0'].dropna()
b = df.loc[df['Grupo']== 'Controle','HBA1C D60'].dropna()
c = df.loc[df['Grupo']== 'Controle','HBA1C D120'].dropna()
       
hemo_controle = [a, b, c]

plt.figure(figsize=(15,5))
plt.axhline(y = 5.6, color = 'blue', linestyle = '--')
plt.boxplot(hemo_controle, labels=['D0', 'D60', 'D120'])
plt.yaxis.grid(True)
plt.ylabel('Hemoglobina Glicada')
plt.xlabel('Tempo')
plt.title('Hemoglobina Glicada')
plt.show()

#%% Analisar comportamento Hemoglobina Glicada somente do Grupo Estudo

d = df.loc[df['Grupo']== 'Estudo','HBA1C D0'].dropna()
e = df.loc[df['Grupo']== 'Estudo','HBA1C D60'].dropna()
f = df.loc[df['Grupo']== 'Estudo','HBA1C D120'].dropna()
       
hemo_estudo = [d, e, f]

plt.figure(figsize=(15,5))
plt.axhline(y = 5.6, color = 'blue', linestyle = '--')
plt.boxplot(hemo_estudo, labels=['D0', 'D60', 'D120'])
plt.yaxis.grid(True)
plt.ylabel('Hemoglobina Glicada')
plt.xlabel('Tempo')
plt.title('Hemoglobina Glicada')
plt.show()

# Hemo do Grupo Controle ficou estável, enquanto do grupo estudo caiu de D0 para D60, e de D60 para D120

#%% Deixar somente colunas de estudo de HBA1C

hemo_controle_antes = (df[(df['Grupo'] == 'Controle')].loc[:,'HBA1C D0']).dropna()
hemo_controle_depois = (df[(df['Grupo'] == 'Controle')].loc[:,'HBA1C D120']).dropna()
hemo_estudo_antes = (df[(df['Grupo'] == 'Estudo')].loc[:,'HBA1C D0']).dropna()
hemo_estudo_depois = (df[(df['Grupo'] == 'Estudo')].loc[:,'HBA1C D120']).dropna()

#%% Teste Shapiro Wilk para verificação da normalidade da distribuição

n1 = stats.shapiro(hemo_controle_antes)
n2 = stats.shapiro(hemo_controle_depois)
n3 = stats.shapiro(hemo_estudo_antes)
n4 = stats.shapiro(hemo_estudo_depois)

print('P-value Controle Antes:', n1.pvalue)
print('P-value Controle Depois:', n2.pvalue)
print('P-value Estudo Antes:', n3.pvalue)
print('P-value Estudo Depois:', n4.pvalue)

#Não houve violação da distribuição normal

#%% Teste Levene para verificação da homocedasticidade das variâncias

h1 = stats.levene(hemo_controle_antes,hemo_estudo_antes)
h2 = stats.levene(hemo_controle_depois,hemo_estudo_depois)

print('P-value Controle Antes:', h1.pvalue)
print('P-value Controle Depois:', h2.pvalue)

# Não houve violação da homogeneidade das variâncias.
# Todos os momentos possuem p > 0,05 no teste Levene. 

#%% ANOVA DE MEDIDA REPETIDA

Hemo = pd.read_excel('C:/Users/sandy/OneDrive/Documentos/GitHub/ProjetoEACH/ProjetoEACH/Codigo1b.xlsx')

ANOVA = pg.rm_anova(data=Hemo, dv='Hemo', within='Tempo', subject='Name', 
                  correction='auto', detailed=False, effsize='ng2')

print('Degrees of freedom (numerator)', ANOVA['ddof1'])
print('Degrees of freedom (denominator)', ANOVA['ddof2'])
print('F-value', ANOVA['F'])
print('Uncorrected p-value', ANOVA['p-unc'])
print('Generalized eta-square effect size', ANOVA['ng2']) 
print('Greenhouse-Geisser epsilon factor (= index of sphericity)', ANOVA['eps'])
print('Greenhouse-Geisser corrected p-value',ANOVA['p-GG-corr'])
print('Sphericity test statistic',ANOVA['W-spher'])
print('p-value of the sphericity test',ANOVA['p-spher'])
print('sphericity of the data (boolean)',ANOVA['sphericity'])

# Como não há esfericidade nas variâncias é preciso analisar o p-value da ANOVA com correção
# de Greenhouse-Geisser que é 0.000015. 
# Ou seja, existe diferença entre as médias de hemoglobina em relação ao tempo.

#%% Post Hoc para entender as interações entre os grupos no tempo

posthoc = pg.pairwise_tests(dv='Hemo', between=['Grupo', 'Tempo'], data=Hemo, 
                            alpha=0.05, padjust='bonf', correction='auto')


print((posthoc[posthoc['Contrast'] == 'Grupo * Tempo']))
                  
# Post hoc mostra que p-values do grupo Estudo nos tempos D0 e D120 é menor que 0,05 
# Já os p-values do grupo controle são todos acima de 0,05.
# O que indica que a substituição do estudo reduziu a hemoglobina glicada. 
# Com tamanho de efeito de 1,51 de D de Cohen (muito grande).

#%% Fim da análise da Hemoglobina glicada


