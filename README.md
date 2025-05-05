<p align="center">
  <img src="food_logo.png" alt="food-logo" width="250"/>
</p>

## 1. Problema de negócio

>Este projeto foi elaborado durante a curso Analisando Dados com Python da Comunidade DS e tenta solucionar um problema de negócio apresentado durante o curso.

A Cury Company é uma empresa de tecnologia que criou um aplicativo que conecta restaurantes, entregadores e consumidores. Através desse aplicativo, o consumidor pode realizar o pedido de uma refeição em um dos restaurantes cadastrados que entrega por meio de um entregador também cadastrado no aplicativo da Cury Company.

Nesta operação são gerados muitos dados sobre entregas, tipos de pedidos, condições climáticas, avaliação dos entregadores etc. Apesar do número de entregas apresentar aumento(em números gerais), o CEO não tem visibilidade completa dos KPIs de crescimento da empresa.

Uma das necessidades atuais da empresa é ter os principais KPIs estratégicos organizados em uma única ferramenta, para que sejam consultados pelos interessados a qualquer momento e os ajudem a tomar decisões simples, porém importantes.

A Cury Company possui um modelo de negócio chamado **Marketplace**. Para acompanhar o crescimento desses negócios, o CEO gostaria de ver as seguintes métricas de crescimento:

***Métricas da EMPRESA:***

1. Quantidade de pedidos por dia.
2. Quantidade de pedidos por semana.
3. Distribuição dos pedidos por tipo de tráfego.
4. Comparação do volume de pedidos por cidade e tipo de tráfego.
5. A quantidade de pedidos por entregador por semana.
6. A localização central de cada cidade por tipo de tráfego.

***Métricas dos ENTREGADORES:***

1. A menor e maior idade dos entregadores.
2. A pior e a melhor condição de veículos.
3. A avaliação média por entregador.
4. A avaliação média e o desvio padrão por tipo de tráfego.
5. A avaliação média e o desvio padrão por condições climáticas.
6. Os 10 entregadores mais rápidos por cidade.
7. Os 10 entregadores mais lentos por cidade.

***Métrica dos RESTAURANTES:***

1. A quantidade de entregadores únicos.
2. A distância média dos restaurantes e dos locais de entrega.
3. O tempo médio e o desvio padrão de entrega por cidade.
4. O tempo médio e o desvio padrão de entrega por cidade e tipo de pedido.
5. O tempo médio e o desvio padrão de entrega por cidade e tipo de tráfego.
6. O tempo médio de entrega durantes os Festivais.

>O objetivo desse projeto, portanto, é criar um conjunto de gráficos e/ou tabelas que exibam essas métricas afim de auxiliar nas tomadas de decisão.

## 2. Premissas assumidas para análise

1. A análise foi realizada com dados coletados entre 11/02/2022 e 06/04/2022.
2. Marketplace foi o modelo de negócio assumido.
3. As 3 principais visões do negócio foram: *visão da Empresa, visão dos Restaurantes e visão dos Entregadores*.

## 3. Estratégia para a solução

O painel estratégico foi desenvolvido com base nas métricas que refletem as 3 principais visões do modelo de negócio da empresa:

1. Visão do crescimento da empresa.
2. Visão do crescimento dos restaurantes.
3. Visão do crescimento dos entregadores.

Cada visão é representada pelo seguinte conjunto de métricas.

1. ***Visão do crescimento da empresa***
    1. Pedidos por dia.
    2. Porcentagem de pedidos por condições de trânsito.
    3. Quantidade de pedidos por tipo e por cidade.
    4. Pedidos por semana.
    5. Quantidade de pedidos por tipo de entrega.
    6. Quantidade de pedidos por condições de trânsito e tipo de cidade.
    
2. ***Visão do crescimento dos restaurantes***
    1. Quantidade de pedidos únicos.
    2. Distância média percorrida.
    3. Tempo médio de entrega durante festival e dias normais.
    4. Desvio padrão do tempo de entrega durante festivais e dias normais.
    5. Tempo de entrega médio por cidade.
    6. Distribuição do tempo médio de entrega por cidade.
    7. Tempo médio de entrega por tipo de pedido.
    
3. ***Visão do crescimento dos entregadores***
    1. Idade do entregador mais velho e do mais novo.
    2. Avaliação do melhor e do pior veículo.
    3. Avaliação média por entregador .
    4. Avaliação média por condições de trânsito.
    5. Avaliação média por condições climáticas.
    6. Tempo médio do entregador mais rápido.
    7. Tempo médio do entregador mais rápido por cidade.

## 4. Top Insights de dados

>**1**. A sazonalidade da quantidade de pedidos é diária e há uma variação de aproximadamente 10% do número de pedidos em dia sequenciais.

>**2**. As cidades do tipo “Semi-Urban” não possuem condições baixas de trânsito.

>**3**. As maiores variações no tempo de entrega, acontecem durante o clima ensolarado.

>**4**. Durante o “Festival” foi observado um comportamento atípico.

## 5. O produto final do projeto

Foi elaborado um painel online que está hospedado em uma Cloud e disponível para acesso através de  qualquer dispositivo conectado à internet.

O painel pode ser acessado em [Curry Company App](https://marcelaprettoamorim-curry-company.streamlit.app/).

## 6. Próximos passos
Esta é a primeira versão do projeto, sendo possível diversas melhorias.

Algumas das melhorias possíveis seriam:
 - Solicitar feedback das áreas de negócio que utilizaram a análise para entender se as métricas apresentadas foram suficientes para a tomada de decisões e se modificações são necessárias;
- Criar novos filtros para melhor segmentar os resultados;
- Adicionar novas visões de negócio;
- Buscar mais informações sobre o “Festival” para explicar comportamento atípico observado;
- Melhoria no código para melhor eficiência.

## 📩 Contato

Caso tenha dúvidas, entre em contato pelo meu [LinkedIn](https://www.linkedin.com/in/marcela-de-pretto-amorim/).