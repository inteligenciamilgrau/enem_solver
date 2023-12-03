import os
import json
import re
import openai # pip install openai
import time
import datetime
import requests
import base64

openai.api_key = "SUA-API-KEY"

'''
questões de número 01 a 45, relativas à área de Linguagens, Códigos e suas Tecnologias;
questões de número 46 a 90, relativas à área de Ciências Humanas e suas Tecnologias. 
questões de número 91 a 135, relativas à área de Ciências da Natureza e suas Tecnologias;
questões de número 136 a 180, relativas à área de Matemática e suas Tecnologias;
Questões de 01 a 05 (opção inglês ou espanhol)
'''

questoes = 180

gabarito_filename = "gabaritos/gabarito_unificado_azul.json"

modelo = "gpt-3.5-turbo-1106"
modelo = "gpt-4-1106-preview"
modelo_visao = "gpt-4-vision-preview"

temperatura = 0.0

instrucoes = """
    Explique passo a passo a questão e depois diga a alternativa correta 
    da questão em formato json como no exemplo { "questao 03": "B" }:"""

comecou = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M')

# Record the start time
start_time = time.time()


def perguntar_ao_chat(messages, model, temperature):
    try:
        response = openai.chat.completions.create(
            model=model,
            messages=[{"role": "system", "content": instrucoes},
                      {"role": "user", "content": messages}],
            temperature=temperature,
        )

        return response.choices[0].message.content
    except Exception as e:
        print("Erro", e)
        return e


def encode_image(image_path):
    if image_path.startswith("http:"):
        return base64.b64encode(requests.get(image_path).content).decode('utf-8')
    else:
        image_path = image_path.replace("\\", "\\\\")

        directory, filename = os.path.split(image_path)
        file = rf"{directory}\{filename}"

        with open(file, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')


def perguntar_ao_chat_com_imagem(question_content, image_file, model_vision):

    # Getting the base64 string
    base64_image = encode_image(image_file)

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {openai.api_key}"
    }

    pergunta = """
        Com o auxilio da imagem explique passo a passo a questão e depois diga a alternativa correta 
        da questão em formato json como no exemplo {'questao 03': 'B'}.\n"""

    pergunta = pergunta + question_content

    payload = {
        "model": model_vision,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": pergunta
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 1_000
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    resposta = response.json()["choices"][0]['message']['content']

    return resposta


with open(gabarito_filename, 'r', encoding='utf-8') as file:
    gabarito = json.load(file)

acertos = 0
parciais = {}

assistente_intro = '# Assistente IMG para Resolução da Prova do ENEM 2023 com ChatGPT #'

print('#' * len(assistente_intro))
print(assistente_intro)
print('#' * len(assistente_intro))
print("Modelo de Linguagem:", modelo)
print("Modelo de Visão:", modelo_visao)

# Iterate through 45 questions
for question_number in range(1, questoes + 1):

    dia = "D1" if question_number <= 90 else "D2"

    # Generate the filename
    filename = f"questoes/{dia}_questao_{question_number:02d}.txt"

    # Check if a corresponding JPG file exists
    image_filename = f"questoes/questao_{question_number:02d}.PNG"
    image_exists = os.path.exists(image_filename)

    # Read and print the content of the file
    with open(filename, 'r', encoding='utf-8') as file:
        question_content = file.read()


        if image_exists:
            print("Enviando Questão", question_number, "Com Imagem")
            resp_chat = perguntar_ao_chat_com_imagem(question_content, image_filename, modelo_visao)
        else:
            print("Enviando Questão", question_number, "Sem Imagem")
            resp_chat = perguntar_ao_chat(question_content, modelo, temperatura)

        resp = resp_chat

        #print(f"Pergunta atual: {filename}:\n{question_content}")
        print(f"Pergunta atual: \n{question_content}")

        print("\n##########\n Resposta do Chat", resp)
        print(40 * "=")

        matches = re.findall(r'["\'](quest\S+ \d+)["\']: ["\'](.*?)["\']', resp, re.IGNORECASE | re.UNICODE)
        # Iterate over matches
        if matches:
            for match in matches:
                question_num = match[0]
                answer = match[1]
                print(f"A resposta para questão {question_num} é: {answer}")
        else:
            answer = "Sem resposta"
            print("Answer not found.")

        print('=' * 40)

    correta = gabarito[f"questao {question_number:02d}"]
    parcial = "Questao", question_number, "Gabarito:", correta, "Respondida:", answer

    print(parcial)
    if correta == answer:
        acertos += 1

    avaliacao = "Acertos: " + str(acertos) + " De: " + str(question_number) +\
                " questoes - Percentual de Acertos: " + str(int(acertos/question_number * 100)) + "%"
    print(avaliacao)

    save_txt = False
    if save_txt:
        # Append text to a text file
        output_text_file = f"resolucao_{comecou}_{modelo}.txt"
        with open(output_text_file, 'a', encoding='utf-8') as text_file:
            text_file.write(f"Questao: {question_content}\n")
            text_file.write(f"Resposta: {resp_chat}\n")
            text_file.write(f"Avaliacao: {avaliacao}\n")

    parciais[f"questao {question_number:02d}"] = [{"Pergunta": question_content},
                                                  {"Resposta": resp},
                                                  {"Gabarito": correta},
                                                  {"Respondida": answer},
                                                  {"Avaliacao Parcial": [{"acertos": acertos,
                                                                          "questoes": question_number,
                                                                          "percentual de acertos": int(acertos/question_number * 100)}]}]

    print("")


# Record the end time
end_time = time.time()
elapsed_time = end_time - start_time

# Calculate hours, minutes, and seconds
hours, remainder = divmod(elapsed_time, 3600)
minutes, seconds = divmod(remainder, 60)

output_text_file = f"resolucao_{modelo}_pts_{int(acertos/questoes * 100):03d}_{comecou}.json"

with open(output_text_file, 'a', encoding='utf-8') as text_file:
    json.dump({"prova": parciais,
               "avaliacao": [{"tempo decorrido": [{"horas": int(hours), "minutos": int(minutes), "segundos": int(seconds)}],
                              "acertos": acertos,
                              "erros": questoes - acertos,
                              "percentual de acertos": int(acertos/questoes * 100),
                              "modelo": modelo,
                              "modelo visao": modelo_visao,
                              "temperatura": temperatura}]},
    text_file, ensure_ascii=False, indent=4)

