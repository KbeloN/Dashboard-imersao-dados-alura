import streamlit as st
import pandas as pd
import plotly.express as px

# Define o título e o icone da página e que o layout ocupe a página inteira.
st.set_page_config(
    page_title="Dashboard Interativo",
    page_icon="📊",
    layout="wide",
)

# Carregar o DataFrame
df = pd.read_csv("dataframe-limpo")

# Barra lateral (Filtros)
st.sidebar.header("Filtros")

# Filtros
# Filtro (Ano)
anos_disponiveis = sorted(df['ano'].unique())
ano_selecionado = st.sidebar.multiselect("Ano(s)", anos_disponiveis, default=anos_disponiveis)

# Filtro (Experiência)
experiencias_disponiveis = sorted(df['experiencia'].unique())
experiencias_selecionadas = st.sidebar.multiselect("Experiência(s)", experiencias_disponiveis, default=experiencias_disponiveis)

# Filtro (Tipo de Trabalho)
tipos_trabalho_disponiveis = sorted(df['tipo_trabalho'].unique())
tipos_trabalho_selecionados = st.sidebar.multiselect("Tipo de Trabalho(s)", tipos_trabalho_disponiveis, default=tipos_trabalho_disponiveis)

# Filtro (Taxa Remoto)
taxas_remoto_disponiveis = sorted(df['taxa_remoto'].unique())
taxas_remoto_selecionadas = st.sidebar.multiselect("Taxa Remoto(s)", taxas_remoto_disponiveis, default=taxas_remoto_disponiveis)

# Filtro (Tamanho da empresa)
tam_empresa_disponiveis = sorted(df['tamanho_empresa'].unique())
tam_empresa_selecionados = st.sidebar.multiselect("Tamanho da Empresa(s)", tam_empresa_disponiveis, default=tam_empresa_disponiveis)

# Variável que armazena os filtros selecionados
df_filtrado = df[
    df['ano'].isin(ano_selecionado) &
    df['experiencia'].isin(experiencias_selecionadas) &
    df['tipo_trabalho'].isin(tipos_trabalho_selecionados) &
    df['taxa_remoto'].isin(taxas_remoto_selecionadas) &
    df['tamanho_empresa'].isin(tam_empresa_selecionados)             
    ]

# Conteúdo principal
st.title("Dashboard Interativo do mundo da Tecnologia")
st.markdown("Dados salariais de profissionais da tecnologia dos últimos anos (Selecione os filtros à esquerda).")

# Subtítulo das métricas
st.subheader("Métricas gerais (Salário anual em USD)")

# Métricas gerais
if not df_filtrado.empty:
    salario_media = df_filtrado['usd'].mean()
    salario_max = df_filtrado['usd'].max()
    quant_registros = df_filtrado.shape[0]
    cargo_mais_frequente = df_filtrado['cargo'].mode()[0]
else:
    salario_media, salario_max, quant_registros, cargo_mais_frequente = 0, 0, 0, "N/A"

# Exibição das métricas
col1, col2, col3, col4 = st.columns(4)
col1.metric("Salário Médio", f"${salario_media:,.0f}")
col2.metric("Salário Máximo", f"${salario_max:,.0f}")
col3.metric("Quantidade de Registros", f"${quant_registros:,}")
col4.metric("Cargo Mais Frequente", cargo_mais_frequente)

st.markdown("---")

# Gráficos

#Linha com os gráficos 1 e 2
col_graf1, col_graf2 = st.columns(2)

# Gráfico 1: Distribuição salarial por cargo
with col_graf1:
    if not df_filtrado.empty:
        media_cargo = df_filtrado.groupby('cargo')['usd'].mean().nlargest(10).reset_index() # Obtendo os 10 cargos com as maiores médias salariais
        grafico_cargo = px.bar(
            media_cargo,
            x='usd',
            y='cargo',
            orientation='h',
            title="Distribuição salarial por cargo",
            labels={'cargo' : 'Cargo(s)', 'usd' : 'Média Salarial Anual (USD)'})
        grafico_cargo.update_layout(title_x=0.1,yaxis={'categoryorder':'total ascending'},yaxis_title_text=None)
        st.plotly_chart(grafico_cargo, use_container_width=True)
    else:
        st.warning("Nenhum dado disponível para exibir.")

# Gráfico 2: Distribuição salarial anual
with col_graf2:
    if not df_filtrado.empty:
        grafico_anual = px.histogram(
            df_filtrado,
            x='usd',
            nbins=30,
            title="Distribuição Salarial Anual",
            labels={'usd': 'Salário anual (USD)'})
        grafico_anual.update_layout(title_x=0.1, yaxis_title_text=None)
        st.plotly_chart(grafico_anual, use_container_width=True)
    else:
        st.warning("Nenhum dado disponível para exibir.")


# Linha com os gráficos 3 e 4
col_graf3, col_graf4 = st.columns(2)

# Gráfico 3: Distribuição de tipos de trabalho 
remoto_est = df_filtrado['taxa_remoto'].value_counts().reset_index() # Pegando a distribuição dos tipos de trabalho
remoto_est.columns = ['taxa_remoto', 'quantidade'] # Renomeando as colunas

with col_graf3:
    if not df_filtrado.empty:
        grafico_rosca = px.pie(
            remoto_est,
            names='taxa_remoto',
            values='quantidade',
            title='Distribuição dos tipos de trabalho',
            hole=0.5)
        grafico_rosca.update_layout(title_x=0.1)
        st.plotly_chart(grafico_rosca, use_container_width=True)
    else:
        st.warning("Nenhum dado disponível para exibir.")

# Gráfico 4: Média salarial de Data Scientist por país
with col_graf4:
    if not df_filtrado.empty:
        df_ds = df_filtrado[df_filtrado['cargo'] == 'Data Scientist']
        media_ds_pais = df_ds.groupby('residencia_iso3')['usd'].mean().reset_index()

        grafico_ds_pais = px.choropleth(
            media_ds_pais,
            locations='residencia_iso3',
            color='usd',
            color_continuous_scale='rdylgn',
            title='Média salarial data scientist por país',
            labels={'usd': 'Média salárial (USD)', 'residencia_iso3': 'País'})
        grafico_ds_pais.update_layout(title_x=0.1)
        st.plotly_chart(grafico_ds_pais, use_container_width=True)
    else:
        st.warning("Nenhum dado disponível para exibir.")

# Dados detalhados
st.subheader("Dados detalhados")
st.dataframe(df_filtrado)