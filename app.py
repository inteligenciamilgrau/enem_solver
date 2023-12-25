from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)


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


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Check if a file was uploaded
        if "file" in request.files:
            file = request.files["file"]
            if file.filename != "":
                try:
                    # Read data from the uploaded JSON file
                    result_data = json.load(file)

                    # Chamada da função
                    resultado_por_categoria = calcular_acertos_por_categoria(result_data)
                    # Exibe o resultado
                    for categoria, acertos in resultado_por_categoria.items():
                        avaliacao_por_categoria = {
                            categoria: [{'acertos': acertos,'percentual': int((acertos / 45) * 100)}]
                        }
                        print(avaliacao_por_categoria)
                        result_data['avaliacao'].append(avaliacao_por_categoria)
                        print(
                            f'Total de acertos em {categoria}: {acertos} que corresponde a {int((acertos / 45) * 100)}%')
                    print(result_data['avaliacao'])
                    return render_template("index.html", data=result_data)
                except json.JSONDecodeError:
                    error_message = "Invalid JSON file. Please upload a valid JSON file."
                    return render_template("index.html", error_message=error_message)

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)


