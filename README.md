# Data Science em Produção
## Previsão de Vendas

### Questão de Negócio
Qual é o valor das vendas de cada loja para as próximas 6 semanas?

### Entendimento do Negócio
#### Qual a Motivação?
- A previsão de vendas foi requisiada pelo CFO em uma reunião mensal sobre os resultados das lojas;
 
#### Qual a causa raiz do problema?
- Dificuldade em determinar o valor de investimento para reformas de cada loja. 

### Quem é o usuário da solução?
- Diretor Financeiro (CFO) da Rossmann

### Qual o formato da solução?
- Granularidade: Previsão de vendas por dia para cada loja para os próximos 42 dias, 6 semanas.
- Tipo do problema: Previsão de vendas
- Potenciais métodos: Séries temporais e regressão
- Formato de entrega:
1) O valor total previsto das vendas de cada loja para as próximas seis semanas. 
Ex: 
Loja    Total previsto
01 	    100.000,00
02      130.000,00

2) Acesso via celular do valor previsto e o comportamento da previsão