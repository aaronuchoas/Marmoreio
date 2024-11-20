# Este codigo realiza a análise do marmoreio em steaks de carne.
# Etapas:
# 1. Carrega a imagem ja com um contorno VERDE para isolar.
# 2. Isola a região de interesse (ROI) com base em contornos verdes.
# 3. Processa a ROI para destacar o marmoreio (gordura).
# 4. Calcula a porcentagem de marmoreio e classifica em graus de 1 a 5.



import cv2
from matplotlib import pyplot as plt
import numpy as np

# Carrega a imagem .jpg presente na mesma pasta 
image_path = "c1.jpg"
img = cv2.imread(image_path)

# Verificar se a imagem foi carregada corretamente
if img is None:
    print("Erro ao carregar a imagem.")
else:
    # Etapa 1: Carrega imagem original com o cotorno verde feito manualmente
    plt.figure()
    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    plt.title('Imagem original com a area de análise circulada em Verde')
    plt.axis('off')
    plt.show()

    # Converte a imagem para HSV para detectar o contorno verde
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    # Define limites para a cor verde
    lower_green = np.array([40, 40, 40])
    upper_green = np.array([80, 255, 255])
    
    # Cria uma máscara para a o contorno  verde
    mask_green = cv2.inRange(hsv, lower_green, upper_green)

    # Etapa 2: Apresenta o cortono verde feito 
    plt.figure()
    plt.imshow(mask_green, cmap='gray')
    plt.title('Máscara Verde')
    plt.axis('off')
    plt.show()
    
    # Identifica o contorno na máscara verde
    contours, _ = cv2.findContours(mask_green, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Criar uma máscara vazia do mesmo tamanho da imagem original
    mask_filled_roi = np.zeros(img.shape[:2], dtype=np.uint8)
    
    # Preencher o interior da máscara (sem as bordas)
    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        cv2.drawContours(mask_filled_roi, [largest_contour], -1, 255, thickness=cv2.FILLED)
    
    # Etapa 3: Máscara Preenchida da Region of Interest (ROI)
    plt.figure()
    plt.imshow(mask_filled_roi, cmap='gray')
    plt.title('ROI com a Máscara Preenchida')
    plt.axis('off')
    plt.show()

    # Aplica a máscara preenchida na imagem original para isolar a ROI 
    roi_without_green_contour = cv2.bitwise_and(img, img, mask=mask_filled_roi)

    # Remover o contorno verde, aplicando a máscara apenas nas regiões que não têm contorno verde
    roi_without_green = cv2.bitwise_and(roi_without_green_contour, roi_without_green_contour, mask=~mask_green)

    # Etapa 4: ROI Isolada, regiao contornada com o fundo original
    plt.figure()
    plt.imshow(cv2.cvtColor(roi_without_green, cv2.COLOR_BGR2RGB))
    plt.title('ROI Isolada com o fundo original')
    plt.axis('off')
    plt.show()

    # Converter a ROI isolada para escala de cinza para facilitar a aplicação do proximo filtro
    roi_gray = cv2.cvtColor(roi_without_green, cv2.COLOR_BGR2GRAY)

    # Etapa 5: ROI Isolada em Escala de Cinza
    plt.figure()
    plt.imshow(roi_gray, cmap='gray')
    plt.title('ROI Isolada em Escala de Cinza')
    plt.axis('off')
    plt.show()

    # Binarizar a ROI em escala de cinza para destacar as áreas de gordura
    _, binary_roi = cv2.threshold(roi_gray, 127, 255, cv2.THRESH_BINARY)

    # Aplicar erosão para separar áreas de gordura próximas
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    eroded_roi = cv2.erode(binary_roi, kernel, iterations=1)
    

    # Etapa 6: Erosão (Separação da Gordura)
    plt.figure()
    plt.imshow(eroded_roi, cmap='gray')
    plt.title('Erosão (Separação da Gordura)')
    plt.axis('off')
    plt.show()

# Contar os pixels brancos (representando gordura) na imagem erodida
num_white_pixels = cv2.countNonZero(eroded_roi)

# Exibir o resultado
print(f"Numero de pixels de marmoreio: {num_white_pixels}")

# Área total da ROI (número total de pixels na máscara preenchida)
total_roi_pixels = cv2.countNonZero(mask_filled_roi)

# Porcentagem de gordura (marmoreio) em relação à ROI
marmoreio_percentage = (num_white_pixels / total_roi_pixels) * 100

# Exibir a porcentagem
print(f"Porcentagem de marmoreio: {marmoreio_percentage:.2f}%")

# Classificação de acordo com a porcentagem de marmoreio
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
    
# Retorna os dados
print(f"Classificacao: {grau_marmoreio} de marmoreio")