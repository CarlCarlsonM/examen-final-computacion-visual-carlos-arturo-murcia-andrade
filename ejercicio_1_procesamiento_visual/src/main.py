import cv2
import numpy as np
import os
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="Pipeline de Procesamiento Visual - Ejercicio 1")
    parser.add_argument(
        "--input", 
        type=str, 
        default=os.path.join("ejercicio_1_procesamiento_visual", "data", "input.png"),
        help="Ruta de la imagen de entrada"
    )
    parser.add_argument(
        "--output_dir", 
        type=str, 
        default=os.path.join("ejercicio_1_procesamiento_visual", "resultados"),
        help="Directorio de salida para los resultados"
    )
    parser.add_argument(
        "--blur_kernel", 
        type=int, 
        default=5, 
        help="Tamaño del kernel para el suavizado Gaussiano (debe ser impar)"
    )
    parser.add_argument(
        "--canny_low", 
        type=int, 
        default=50, 
        help="Umbral inferior para el detector de bordes Canny"
    )
    parser.add_argument(
        "--canny_high", 
        type=int, 
        default=150, 
        help="Umbral superior para el detector de bordes Canny"
    )
    parser.add_argument(
        "--min_area", 
        type=int, 
        default=1000, 
        help="Área mínima (en píxeles) para considerar un contorno como objeto"
    )
    return parser.parse_args()

def main():
    args = parse_args()
    
    # Crear el directorio de salida si no existe
    os.makedirs(args.output_dir, exist_ok=True)
    print(f"[INFO] Directorio de salida verificado/creado: {args.output_dir}")

    # 1. Cargar una entrada visual
    print(f"[INFO] Cargando imagen de entrada desde: {args.input}")
    if not os.path.exists(args.input):
        print(f"[ERROR] No se encontró la imagen en {args.input}. Por favor verifica la ruta.")
        return

    original = cv2.imread(args.input)
    if original is None:
        print("[ERROR] No se pudo decodificar la imagen de entrada.")
        return
    
    h, w, c = original.shape
    print(f"[INFO] Imagen cargada con éxito. Dimensiones: {w}x{h} px, Canales: {c}")
    
    # Guardar original en resultados
    original_path = os.path.join(args.output_dir, "original.png")
    cv2.imwrite(original_path, original)
    print(f"[INFO] Imagen original guardada en: {original_path}")

    # 2. Generar una versión en escala de grises
    print("[INFO] Convirtiendo a escala de grises...")
    grises = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
    grises_path = os.path.join(args.output_dir, "grises.png")
    cv2.imwrite(grises_path, grises)
    print(f"[INFO] Imagen en escala de grises guardada en: {grises_path}")

    # 3. Generar una segunda representación de color (HSV)
    print("[INFO] Convirtiendo a espacio de color HSV...")
    hsv = cv2.cvtColor(original, cv2.COLOR_BGR2HSV)
    hsv_path = os.path.join(args.output_dir, "hsv_o_lab.png")
    cv2.imwrite(hsv_path, hsv)
    print(f"[INFO] Representación HSV guardada en: {hsv_path}")

    # 4. Aplicar suavizado (Filtro Gaussiano)
    print(f"[INFO] Aplicando filtro de suavizado Gaussiano con kernel {args.blur_kernel}x{args.blur_kernel}...")
    suavizado = cv2.GaussianBlur(grises, (args.blur_kernel, args.blur_kernel), 0)
    suavizado_path = os.path.join(args.output_dir, "suavizado.png")
    cv2.imwrite(suavizado_path, suavizado)
    print(f"[INFO] Imagen suavizada guardada en: {suavizado_path}")

    # 5. Aplicar detección de bordes (Canny)
    print(f"[INFO] Aplicando detección de bordes Canny (Umbrales: {args.canny_low}, {args.canny_high})...")
    bordes = cv2.Canny(suavizado, args.canny_low, args.canny_high)
    bordes_path = os.path.join(args.output_dir, "bordes.png")
    cv2.imwrite(bordes_path, bordes)
    print(f"[INFO] Detección de bordes guardada en: {bordes_path}")

    # 6. Realizar segmentación o detección (Técnica Clásica basada en Umbralización y Contornos)
    print("[INFO] Iniciando segmentación y detección de objetos...")
    
    # Aplicar umbralización adaptativa u Otsu para obtener una máscara binaria
    # Usamos Otsu sobre la versión suavizada para segmentar los objetos del fondo
    _, thresh = cv2.threshold(suavizado, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    
    # En caso de que el fondo sea claro y los objetos oscuros, o viceversa:
    # Contamos los píxeles blancos en los bordes para determinar si debemos invertir la máscara
    border_pixels = np.concatenate([thresh[0, :], thresh[-1, :], thresh[:, 0], thresh[:, -1]])
    if np.mean(border_pixels) > 127:
        print("[INFO] Detectado fondo claro en la máscara. Invirtiendo máscara para segmentar objetos del fondo.")
        thresh = cv2.bitwise_not(thresh)

    # Operaciones morfológicas para limpiar ruido (apertura para eliminar ruido blanco pequeño, clausura para rellenar huecos)
    kernel_morph = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    morph = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel_morph, iterations=1)
    morph = cv2.morphologyEx(morph, cv2.MORPH_CLOSE, kernel_morph, iterations=1)

    # Encontrar contornos
    contours, hierarchy = cv2.findContours(morph, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Crear una copia de la imagen original para dibujar los resultados
    deteccion_visual = original.copy()
    
    object_count = 0
    print(f"[INFO] Se encontraron en total {len(contours)} contornos candidatos.")
    
    for idx, c in enumerate(contours):
        area = cv2.contourArea(c)
        # Filtrar contornos pequeños que son ruido
        if area < args.min_area:
            continue
        
        object_count += 1
        
        # Calcular momentos para el centroide
        M = cv2.moments(c)
        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
        else:
            cX, cY = 0, 0
            
        # Calcular perímetro y circularidad
        perimeter = cv2.arcLength(c, True)
        circularity = 4 * np.pi * area / (perimeter ** 2) if perimeter > 0 else 0
        
        # Obtener caja delimitadora (Bounding Box)
        x, y, w_box, h_box = cv2.boundingRect(c)
        
        # Dibujar el contorno en verde
        cv2.drawContours(deteccion_visual, [c], -1, (0, 255, 0), 2)
        
        # Dibujar la caja en azul
        cv2.rectangle(deteccion_visual, (x, y), (x + w_box, y + h_box), (255, 0, 0), 2)
        
        # Dibujar una pequeña marca en el centroide
        cv2.circle(deteccion_visual, (cX, cY), 5, (0, 0, 255), -1)
        
        # Añadir etiqueta sobre el objeto
        label = f"Obj {object_count}"
        cv2.putText(deteccion_visual, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
        
        print(f"  [Objeto {object_count}] Centroide: ({cX}, {cY}) | Área: {area:.1f} px | Perímetro: {perimeter:.1f} px | Circularidad: {circularity:.2f}")

    print(f"[INFO] Segmentación finalizada. Objetos detectados con área > {args.min_area} px: {object_count}")

    # Guardar imagen con detecciones/segmentación
    segmentacion_path = os.path.join(args.output_dir, "deteccion_o_segmentacion.png")
    cv2.imwrite(segmentacion_path, deteccion_visual)
    print(f"[INFO] Imagen de detección/segmentación guardada en: {segmentacion_path}")
    print("[INFO] Pipeline completado con éxito.")

if __name__ == "__main__":
    main()
