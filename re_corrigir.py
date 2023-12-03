import json

filename = 'resolucao_2023_11_29_17_03.json'

# Leitura do arquivo JSON
with open(filename, 'r', encoding='utf-8') as file:
    data = json.load(file)

# Inicialização das variáveis
total_questoes = 180
total_acertos = 0

# Iteração sobre as questões
for questao, dados_questao in data['prova'].items():
    # Verifica se há resposta e gabarito para a questão
    if 'Respondida' in dados_questao[-2] and 'Gabarito' in dados_questao[-3]:
        resposta = dados_questao[-2]['Respondida']
        gabarito = dados_questao[-3]['Gabarito']

        # Verifica se a resposta é igual ao gabarito
        if resposta == gabarito:
            total_acertos += 1

# Calcula o percentual de acerto
percentual_acerto = (total_acertos / total_questoes) * 100

# Exibe o resultado
print(f'Total de acertos: {total_acertos}')
print(f'Percentual de acerto: {percentual_acerto:.2f}%')


def calcular_acertos_por_categoria(json_data):
    # Inicialização das variáveis
    acertos_por_categoria = {'linguagens': 0, 'humanas': 0, 'natureza': 0, 'matematica': 0}

    # Iteração sobre as questões
    for questao, dados_questao in json_data['prova'].items():
        # Verifica se há resposta e gabarito para a questão
        if 'Respondida' in dados_questao[-2] and 'Gabarito' in dados_questao[-3]:
            resposta = dados_questao[-2]['Respondida']
            gabarito = dados_questao[-3]['Gabarito']

            # Obtém o número da questão como inteiro
            num_questao = int(questao.split()[-1])

            # Determina a categoria com base no número da questão
            if 1 <= num_questao <= 45:
                categoria = 'linguagens'
            elif 46 <= num_questao <= 90:
                categoria = 'humanas'
            elif 91 <= num_questao <= 135:
                categoria = 'natureza'
            elif 136 <= num_questao <= 180:
                categoria = 'matematica'

            # Verifica se a resposta é igual ao gabarito
            if resposta == gabarito:
                acertos_por_categoria[categoria] += 1

    return acertos_por_categoria

# Chamada da função
resultado_por_categoria = calcular_acertos_por_categoria(data)

# Exibe o resultado
for categoria, acertos in resultado_por_categoria.items():
    print(f'Total de acertos em {categoria}: {acertos} que corresponde a {int((acertos/45)*100)}%')
