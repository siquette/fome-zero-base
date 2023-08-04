import folium
import pandas as pd
import streamlit as st
from folium.plugins import MarkerCluster
from PIL import Image
from streamlit_folium import folium_static

from utils import general_data as gd
from utils.process_data import process_data

RAW_DATA_PATH = f"./data/raw/data.csv"


def create_sidebar(df):
    image_path = "./img/"
    image = Image.open(image_path + "logo.png")

    col1, col2 = st.sidebar.columns([1, 4], gap="small")
    col1.image(image, width=35)
    col2.markdown("# Fome Zero")

    st.sidebar.markdown("## Filtros")

    countries = st.sidebar.multiselect(
        "Escolha os Paises que Deseja visualizar os Restaurantes",
        df.loc[:, "country"].unique().tolist(),
        default=["Brazil", "England", "Qatar", "South Africa", "Canada", "Australia"],
    )

    st.sidebar.markdown("### Dados Tratados")

    processed_data = pd.read_csv("./data/processed/data.csv")

    st.sidebar.download_button(
        label="Download",
        data=processed_data.to_csv(index=False, sep=";"),
        file_name="data.csv",
        mime="text/csv",
    )

    return list(countries)


def create_map(dataframe):
    f = folium.Figure(width=1920, height=1080)

    m = folium.Map(max_bounds=True).add_to(f)

    marker_cluster = MarkerCluster().add_to(m)

    for _, line in dataframe.iterrows():

        name = line["restaurant_name"]
        price_for_two = line["average_cost_for_two"]
        cuisine = line["cuisines"]
        currency = line["currency"]
        rating = line["aggregate_rating"]
        color = f'{line["color_name"]}'

        html = "<p><strong>{}</strong></p>"
        html += "<p>Price: {},00 ({}) para dois"
        html += "<br />Type: {}"
        html += "<br />Aggragate Rating: {}/5.0"
        html = html.format(name, price_for_two, currency, cuisine, rating)

        popup = folium.Popup(
            folium.Html(html, script=True),
            max_width=500,
        )

        folium.Marker(
            [line["latitude"], line["longitude"]],
            popup=popup,
            icon=folium.Icon(color=color, icon="home", prefix="fa"),
        ).add_to(marker_cluster)

    folium_static(m, width=1024, height=768)


def main():

    df = process_data(RAW_DATA_PATH)

    st.set_page_config(page_title="Home", page_icon="📊", layout="wide")

    selected_countries = create_sidebar(df)

    st.markdown("# Fome Zero!")

    st.markdown("## O Melhor lugar para encontrar seu mais novo restaurante favorito!")

    st.markdown("### Temos as seguintes marcas dentro da nossa plataforma:")

    restaurants, countries, cities, ratings, cuisines = st.columns(5)

    restaurants.metric(
        "Restaurantes Cadastrados",
        gd.qty_restaurants(df),
    )

    countries.metric(
        "Países Cadastrados",
        gd.qty_countries(df),
    )

    cities.metric(
        "Cidades Cadastrados",
        gd.qty_cities(df),
    )

    ratings.metric(
        "Avaliações Feitas na Plataforma",
        f"{gd.qty_ratings(df):,}".replace(",", "."),
    )

    cuisines.metric(
        f"Tipos de Culinárias\nOferecidas",
        f"{gd.qty_cuisines(df):,}",
    )

    map_df = df.loc[df["country"].isin(selected_countries), :]

    create_map(map_df)

    return None


if __name__ == "__main__":
    main()

st.markdown(
    """
 A Cury Company é uma empresa ficticia de tecnologia que criou um aplicativo
que conecta restaurantes, entregadores e pessoas.
Através desse aplicativo, é possível realizar o pedido de uma refeição, em
qualquer restaurante cadastrado, e recebê-lo no conforto da sua casa por
um entregador também cadastrado no aplicativo da Cury Company.
A empresa realiza negócios entre restaurantes, entregadores e pessoas,
e gera muitos dados sobre entregas, tipos de pedidos, condições
climáticas, avaliação dos entregadores e etc. Apesar da entrega estar
crescento, em termos de entregas, o CEO não tem visibilidade completa
dos KPIs de crescimento da empresa.
Eu foi contratado como um Cientista de Dados para criar soluções de
dados para entrega, mas antes de treinar algoritmos, a necessidade da
empresa é ter um os principais KPIs estratégicos organizados em uma
única ferramenta, para que o CEO possa consultar e conseguir tomar
decisões simples, porém importantes.
A Cury Company possui um modelo de negócio chamado Marketplace,
que fazer o intermédio do negócio entre três clientes principais:
Restaurantes, entregadores e pessoas compradoras. Para acompanhar o
crescimento desses negócios, o CEO gostaria de ver as seguintes
métricas de crescimento:

### Do lado da empresa:
1. Quantidade de pedidos por dia.
2. Quantidade de pedidos por semana.
3. Distribuição dos pedidos por tipo de tráfego.
4. Comparação do volume de pedidos por cidade e tipo de tráfego.
4. A quantidade de pedidos por entregador por semana.
5. A localização central de cada cidade por tipo de tráfego

### Do lado do entregador:
1. A menor e maior idade dos entregadores.
2. A pior e a melhor condição de veículos.
3. A avaliação médida por entregador.
4. A avaliação média e o desvio padrão por tipo de tráfego.
5. A avaliação média e o desvio padrão por condições climáticas.
6. Os 10 entregadores mais rápidos por cidade.
7. Os 10 entregadores mais lentos por cidade

### Do lado do restaurantes:
1. A quantidade de entregadores únicos.
2. A distância média dos resturantes e dos locais de entrega.
3. O tempo médio e o desvio padrão de entrega por cidade.
4. O tempo médio e o desvio padrão de entrega por cidade e tipo de
pedido.
5. O tempo médio e o desvio padrão de entrega por cidade e tipo de
tráfego.
6. O tempo médio de entrega durantes os Festivais.

O objetivo desse projeto é criar um conjunto de gráficos e/ou tabelas que exibam essas métricas da melhor forma possível para o CEO.

### Premissas assumidas para a análise
1. A análise foi realizada com dados entre 11/02/2022 e 06/04/2022.
2. Marketplace foi o modelo de negócio assumido.
3. Os 3 principais visões do negócio foram: Visão transação de pedidos,
visão restaurante e visão entregadores.

### Estratégia da solução
O painel estratégico foi desenvolvido utilizando as métricas que refletem
as 3 principais visões do modelo de negócio da empresa:
1. Visão do crescimento da empresa
2. Visão do crescimento dos restaurantes
3. Visão do crescimento dos entregadores

Cada visão é representada pelo seguinte conjunto de métricas.

#### 1. Visão do crescimento da empresa
a. Pedidos por dia
b. Porcentagem de pedidos por condições de trânsito
c. Quantidade de pedidos por tipo e por cidade.
d. Pedidos por semana
e. Quantidade de pedidos por tipo de entrega
f. Quantidade de pedidos por condições de trânsito e tipo de cidade
#### 2. Visão do crescimento dos restaurantes
a. Quantidade de pedidos únicos.
b. Distância média percorrida.
c. Tempo médio de entrega durante festival e dias normais.
d. Desvio padrão do tempo de entrega durante festivais e dias
normais.
e. Tempo de entrega médio por cidade.
f. Distribuição do tempo médio de entrega por cidade.
g. Tempo médio de entrega por tipo de pedido.
#### 3. Visão do crescimento dos entregadores
a. Idade do entregador mais velho e do mais novo.
b. Avaliação do melhor e do pior veículo.
c. Avaliação média por entregador.
d. Avaliação média por condições de trânsito.
e. Avaliação média por condições climáticas.
f. Tempo médido do entregador mais rápido.
g. Tempo médio do entregador mais rápido por cidade

### Top 3 Insights de dados
1. A sazonalidade da quantidade de pedidos é diária. Há uma variação
de aproximadamente 10% do número de pedidos em dia sequenciais.
2. As cidades do tipo Semi-Urban não possuem condições baixas de
trânsito.
3. As maiores variações no tempo de entrega, acontecem durante o
clima ensoladao.
### 5. O produto final do projeto
Painel online, hospedado em um Cloud e disponível para acesso em
qualquer dispositivo conectado à internet


### 6. Conclusão
O objetivo desse projeto é criar um conjunto de gráficos e/ou tabelas que
exibam essas métricas da melhor forma possível para o CEO.
Da visão da Empresa, podemos concluir que o número de pedidos
cresceu entre a semana 06 e a semana 13 do ano de 2022


- Discord para contato : rodrigoaronisiquette
- Email para contato : rodrigo.siquette@usp.br
- Telefone para contato : 19995504223
""" )
