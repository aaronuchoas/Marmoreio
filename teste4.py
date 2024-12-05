import cv2
from tkinter import Tk, Label, Button, Radiobutton, StringVar, filedialog
from PIL import Image, ImageTk
from matplotlib import pyplot as plt
import numpy as np

# Função para carregar imagem
def carregar_imagem():
    file_path = filedialog.askopenfilename(
        title="Selecione a imagem",
        filetypes=[("Imagens", "*.jpg *.jpeg *.png")]
    )
    return file_path

# Função para exibir uma imagem usando Matplotlib
def exibir_imagem(titulo, imagem, cmap=None):
    plt.figure()
    plt.imshow(imagem, cmap=cmap)
    plt.title(titulo)
    plt.axis('off')
    plt.show()

# Função principal de análise
def analisar_imagem():
    # Seleciona a imagem
    image_path = carregar_imagem()
    if not image_path:
        label_resultado.config(text="Nenhuma imagem foi selecionada.")
        return

    img = cv2.imread(image_path)
    if img is None:
        label_resultado.config(text="Erro ao carregar a imagem. Verifique o arquivo selecionado.")
        return

    try:
        # Etapa 1: Imagem original
        exibir_imagem("Imagem Original", cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

        # Etapa 2: Conversão para HSV e máscara para o contorno verde
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        lower_green = np.array([40, 40, 40])
        upper_green = np.array([80, 255, 255])
        mask_green = cv2.inRange(hsv, lower_green, upper_green)
        exibir_imagem("Máscara Verde", mask_green, cmap="gray")

        # Etapa 3: Identificação e preenchimento do maior contorno
        contours, _ = cv2.findContours(mask_green, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        mask_filled_roi = np.zeros(img.shape[:2], dtype=np.uint8)
        if contours:
            largest_contour = max(contours, key=cv2.contourArea)
            cv2.drawContours(mask_filled_roi, [largest_contour], -1, 255, thickness=cv2.FILLED)
        exibir_imagem("ROI com Máscara Preenchida", mask_filled_roi, cmap="gray")

        # Etapa 4: Isolamento da ROI sem o contorno verde
        roi_without_green_contour = cv2.bitwise_and(img, img, mask=mask_filled_roi)
        roi_without_green = cv2.bitwise_and(roi_without_green_contour, roi_without_green_contour, mask=~mask_green)
        exibir_imagem("ROI Isolada", cv2.cvtColor(roi_without_green, cv2.COLOR_BGR2RGB))

        # Etapa 5: Conversão da ROI para escala de cinza
        roi_gray = cv2.cvtColor(roi_without_green, cv2.COLOR_BGR2GRAY)
        exibir_imagem("ROI em Escala de Cinza", roi_gray, cmap="gray")

        # Etapa 6: Binarização para destacar a gordura
        _, binary_roi = cv2.threshold(roi_gray, 127, 255, cv2.THRESH_BINARY)
        exibir_imagem("ROI Binarizada", binary_roi, cmap="gray")

        # Etapa 7: Erosão para separar áreas de gordura
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        eroded_roi = cv2.erode(binary_roi, kernel, iterations=1)
        exibir_imagem("Erosão (Separação da Gordura)", eroded_roi, cmap="gray")

        # Cálculos dos pixels
        num_white_pixels = cv2.countNonZero(eroded_roi)
        total_roi_pixels = cv2.countNonZero(mask_filled_roi)
        marmoreio_percentage = (num_white_pixels / total_roi_pixels) * 100

        # Classificação
        if marmoreio_percentage <= 10:
            grau_marmoreio = "Grau 1"
        elif marmoreio_percentage <= 20:
            grau_marmoreio = "Grau 2"
        elif marmoreio_percentage <= 30:
            grau_marmoreio = "Grau 3"
        elif marmoreio_percentage <= 40:
            grau_marmoreio = "Grau 4"
        else:
            grau_marmoreio = "Grau 5"

        resultado = f"Porcentagem de marmoreio: {marmoreio_percentage:.2f}%\nClassificação: {grau_marmoreio}"
        label_resultado.config(text=resultado)
    except Exception as e:
        label_resultado.config(text=f"Erro durante a análise: {str(e)}")

# Configuração da interface gráfica
root = Tk()
root.title("Classificador de Marmoreio de Carnes")
root.geometry("500x400")
root.configure(bg="#f2f2f2")  # Cor de fundo

# Imagem de capa
try:
    img_boi = Image.open("boizinho.jpg")  # Certifique-se de ter o arquivo na mesma pasta
    img_boi = img_boi.resize((100, 100), Image.Resampling.LANCZOS)
    img_boi_tk = ImageTk.PhotoImage(img_boi)
    label_boi = Label(root, image=img_boi_tk, bg="#f2f2f2")
    label_boi.pack(pady=10)
except Exception as e:
    print("Erro ao carregar a imagem do boizinho:", e)

# Título
titulo = Label(root, text="Classificador de Marmoreio de Carnes", font=("Arial", 16, "bold"), bg="#f2f2f2", fg="#333")
titulo.pack()

# Opção de raça
raca_label = Label(root, text="Selecione a Raça:", bg="#f2f2f2", fg="#333", font=("Arial", 12))
raca_label.pack()
raca_var = StringVar(value="Wagyu")
raca_button = Radiobutton(root, text="Wagyu", variable=raca_var, value="Wagyu", bg="#f2f2f2", font=("Arial", 10))
raca_button.pack()

# Botão para carregar imagem
botao_carregar = Button(root, text="Carregar Imagem", command=analisar_imagem, bg="#4CAF50", fg="white", font=("Arial", 12, "bold"), padx=10, pady=5)
botao_carregar.pack(pady=10)

# Resultado da análise
label_resultado = Label(root, text="", wraplength=400, justify="center", bg="#f2f2f2", fg="#333", font=("Arial", 11))
label_resultado.pack(pady=20)

# Iniciar o loop principal
root.mainloop()
