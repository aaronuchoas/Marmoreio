# Classificação de Marmoreio em Carnes

Este projeto utiliza processamento de imagens em Python para avaliar o grau de marmoreio de peças de carne bovina, nesse codigo iremos avaliar especificamente o Wagyu. Esse projeto foi desenvolvido como Trabalho de Conclusão de Curso (TCC) do curso de **Análise e Desenvolvimento de Sistemas**.

## Requisitos

Certifique-se de ter o Python instalado em sua máquina.

1. Dica: Salve a paste em um caminho curto:
    ```bash
    Ex: C:\Users\<seu_nome_de_usuário>

2. Baixe as seguintes bibliotecas no prompt do VScode:
   ```bash
   pip install opencv-python
   pip install matplotlib
   pip install numpy
   pip install pillow

4. Para rodar uma imagem, devemos manualmente fazer um contorno na cor VERDE da área a ser avaliada;

5. Feito esse procedimento, aperte RUN CODE:

6. Na tela inicial selecione a raça e aperte em CARREGAR IMAGEM.

7. Selecione a imagem para analise.

8. O código irá gerar um processamento por etapa, concluindo com:
 ```bash
   A quantidade de pixels de marmoreio
   A porcentagem de marmoreio
   A classificação da carne em graus (de 1 a 5)
