# Classificação de Marmoreio em Carnes

Este projeto utiliza processamento de imagens em Python para avaliar o grau de marmoreio de peças de carne bovina, nesse codigo iremos avaliar especificamente o Wagyu. Esse projeto foi desenvolvido como Trabalho de Conclusão de Curso (TCC) do curso de **Análise e Desenvolvimento de Sistemas**.

## Requisitos

Certifique-se de ter o Python instalado em sua máquina. Utilize um ambiente virtual para instalar as bibliotecas necessárias:

1. Crie um ambiente virtual:
   ```bash
   python -m venv venv

2. Baixe as seguintes bibliotecas no prompt do VScode:
   ```bash
   pip install numpy opencv-python matplotib

3. Na linha 6, informe o nome da imagem .jpg que queria rodar:
   ```bash
   image_path = "nome_da_imagem.jpg"
4. Para rodar uma imagem, devemos manualmente fazer um contorno na cor VERDE da área a ser avaliada;

5. Feito esse procedimento, aperte RUN CODE ou execute no terminal:
   ```bash
   python Classificacao.py

6. O código irá gerar uma imagem por etapa, concluindo com:
 ```bash
   A quantidade de pixels de marmoreio
   A porcentagem de marmoreio
   A classificação da carne em graus (de 1 a 5)
