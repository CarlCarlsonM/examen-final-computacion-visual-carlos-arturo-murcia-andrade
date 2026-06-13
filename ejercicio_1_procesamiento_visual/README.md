# Ejercicio 1 - Procesamiento Visual e IA

Este ejercicio implementa una aplicación en Python que procesa una imagen a través de una secuencia clara de operaciones de visión artificial, culminando en la detección y segmentación clásica de objetos.

## 1. Propósito y Problema Abordado

El objetivo es construir un pipeline de procesamiento digital de imágenes (PDI) para analizar una escena visual. El pipeline realiza tareas de preprocesamiento, realce, detección de bordes y segmentación de objetos sobre una imagen que contiene múltiples elementos sobre un fondo. Este proceso permite extraer información estructural (bordes) y semántica (objetos aislados con sus respectivas propiedades geométricas como área, perímetro, circularidad y centroide).

## 2. Herramientas y Librerías Utilizadas

- **Python (v3.12.1)**: Lenguaje de programación principal.
- **OpenCV (v4.13.0)**: Biblioteca líder para visión artificial, utilizada para carga, guardado, transformaciones de color, filtrado espacial, detección de bordes, umbralización y análisis de contornos.
- **NumPy (v2.4.4)**: Biblioteca para computación científica, utilizada para la manipulación eficiente de matrices de imágenes.

## 3. Instrucciones de Ejecución

Para ejecutar la solución, navega a la raíz del repositorio y ejecuta:

```bash
python ejercicio_1_procesamiento_visual/src/main.py
```

### Argumentos Opcionales
Puedes personalizar los parámetros de la ejecución utilizando los siguientes argumentos de línea de comandos:

```bash
python ejercicio_1_procesamiento_visual/src/main.py --blur_kernel 5 --canny_low 50 --canny_high 150 --min_area 1000
```

- `--input`: Ruta de la imagen de entrada (por defecto: `ejercicio_1_procesamiento_visual/data/input.png`).
- `--output_dir`: Directorio de salida de resultados (por defecto: `ejercicio_1_procesamiento_visual/resultados`).
- `--blur_kernel`: Tamaño del kernel del filtro Gaussiano (debe ser un número impar, por defecto: `5`).
- `--canny_low`: Umbral inferior de Canny (por defecto: `50`).
- `--canny_high`: Umbral superior de Canny (por defecto: `150`).
- `--min_area`: Área mínima en píxeles para detectar un objeto (por defecto: `1000`).

---

## 4. Parámetros Técnicos y Decisiones

A continuación se detallan las decisiones de diseño y los parámetros utilizados:

| Operación | Método / Parámetros | Justificación Técnica |
| :--- | :--- | :--- |
| **Carga de entrada** | `cv2.imread()` | Carga de la imagen de prueba en formato estándar BGR de OpenCV. |
| **Escala de Grises** | BGR a Grises (`cv2.COLOR_BGR2GRAY`) | Elimina la información de color redundante para simplificar los cálculos de detección de bordes y umbralización. |
| **Segundo Espacio de Color** | BGR a HSV (`cv2.COLOR_BGR2HSV`) | El espacio de color HSV (Matiz, Saturación, Valor) separa la información cromática de la luminancia. Esto lo hace muy robusto frente a variaciones de iluminación. |
| **Suavizado (Filtro)** | Filtro Gaussiano con Kernel de `5x5` | El filtro Gaussiano suaviza la imagen aplicando una campana de Gauss, reduciendo eficazmente el ruido de alta frecuencia (como ruido de sensor) antes de la detección de bordes, reduciendo así falsos positivos. |
| **Detección de Bordes** | Canny (Umbral Bajo: `50`, Umbral Alto: `150`) | Se utiliza una relación de umbrales `1:3` (recomendada por John Canny). El algoritmo usa histéresis para conectar bordes débiles con bordes fuertes, garantizando contornos continuos. |
| **Segmentación** | Umbralización de Otsu + Operaciones Morfológicas (`MORPH_OPEN`/`MORPH_CLOSE`) con kernel elíptico `5x5` | La umbralización de Otsu calcula automáticamente el umbral óptimo basado en el histograma bimodal. Las operaciones morfológicas de apertura (eliminan ruido pequeño) y cierre (rellenan pequeños huecos internos) garantizan máscaras limpias. |
| **Detección de Objetos** | Contornos Externos (`cv2.RETR_EXTERNAL`) + Filtro de Área (`> 1000 px`) | Extrae los límites de los objetos segmentados. El filtro por área descarta pequeños artefactos residuales no deseados. |

---

## 5. Resultados Obtenidos

El script genera 6 salidas que documentan el pipeline de manera secuencial:

### Comparativa Visual del Pipeline

````carousel
![Original](/ejercicio_1_procesamiento_visual/resultados/original.png)
<!-- slide -->
![Escala de Grises](/ejercicio_1_procesamiento_visual/resultados/grises.png)
<!-- slide -->
![Representación HSV](/ejercicio_1_procesamiento_visual/resultados/hsv_o_lab.png)
<!-- slide -->
![Suavizado Gaussiano](/ejercicio_1_procesamiento_visual/resultados/suavizado.png)
<!-- slide -->
![Detección de Bordes Canny](/ejercicio_1_procesamiento_visual/resultados/bordes.png)
<!-- slide -->
![Segmentación y Detección de Objetos](/ejercicio_1_procesamiento_visual/resultados/deteccion_o_segmentacion.png)
````

### Métricas de Objetos Detectados en la Consola
Al ejecutar el script con la imagen de prueba generada, se obtienen los siguientes resultados en la consola:

```text
[INFO] Se encontraron en total 23 contornos candidatos.
  [Objeto 1] Centroide: (244, 785) | Área: 2407.5 px | Perímetro: 241.4 px | Circularidad: 0.52
  [Objeto 2] Centroide: (318, 780) | Área: 4227.5 px | Perímetro: 321.6 px | Circularidad: 0.51
  [Objeto 3] Centroide: (721, 659) | Área: 38591.0 px | Perímetro: 1685.5 px | Circularidad: 0.17
  [Objeto 4] Centroide: (278, 658) | Área: 35845.5 px | Perímetro: 1205.3 px | Circularidad: 0.31
  [Objeto 5] Centroide: (721, 296) | Área: 46767.0 px | Perímetro: 1120.8 px | Circularidad: 0.47
  [Objeto 6] Centroide: (286, 253) | Área: 30757.5 px | Perímetro: 844.2 px | Circularidad: 0.54
[INFO] Segmentación finalizada. Objetos detectados con área > 1000 px: 6
```

### Análisis Técnico de Resultados
1. **Representación HSV**: La imagen `hsv_o_lab.png` muestra colores distorsionados o psicodélicos cuando es visualizada con un visor de imágenes tradicional BGR. Esto es normal debido a que los valores de Matiz ($H \in [0, 179]$), Saturación ($S \in [0, 255]$) y Valor ($V \in [0, 255]$) son interpretados directamente como componentes Azul, Verde y Rojo.
2. **Suavizado**: Al comparar `grises.png` y `suavizado.png` se observa una reducción en la aspereza de las texturas de la mesa y la superficie de los objetos, lo cual facilita la detección de bordes limpios en el paso de Canny.
3. **Bordes Canny**: `bordes.png` captura con alta fidelidad las siluetas de las frutas y la taza generadas en la imagen, aislando las transiciones bruscas de intensidad.
4. **Segmentación y Detección**: La imagen `deteccion_o_segmentacion.png` muestra los contornos dibujados en verde y las cajas delimitadoras (Bounding Boxes) en azul. La segmentación clásica mediante Otsu y morfología logró separar con éxito los objetos principales (frutas y taza) del fondo oscuro, etiquetando individualmente los 6 objetos más grandes y calculando sus centroides y circularidades (donde valores cercanos a $1.0$ representan formas muy circulares, y valores más bajos representan formas irregulares o alargadas).

---

## 6. Dificultades y Soluciones

1. **Inversión de la Máscara de Umbralización**:
   - *Dificultad*: Dependiendo de la imagen de entrada, el fondo puede ser más claro que los objetos o viceversa. Si se usa un método fijo de umbralización inversa (`THRESH_BINARY_INV`), en imágenes de fondo claro se segmentaría el fondo en lugar de los objetos.
   - *Solución*: Se implementó un algoritmo dinámico que inspecciona los bordes externos de la máscara binaria resultante. Si los bordes contienen una alta densidad de píxeles activos (blancos), se deduce que el fondo se segmentó erróneamente. El script invierte automáticamente la máscara en este caso (`cv2.bitwise_not`), logrando un comportamiento adaptativo.

2. **Ruido en los Contornos**:
   - *Dificultad*: Se detectaban pequeños puntos de luz u sombras menores como objetos (falsos positivos).
   - *Solución*: Se aplicaron operaciones morfológicas de apertura (`MORPH_OPEN`) y cierre (`MORPH_CLOSE`) con un elemento estructurante elíptico, seguidas de un filtro estricto de área mínima (`min_area = 1000` píxeles) para descartar contornos despreciables.

---

## 7. Uso de IA (Prompts)

Para la generación de la imagen de prueba de alta calidad, se utilizó la herramienta de generación de imágenes con el siguiente prompt:
> *"A top-down photograph of distinct colorful items on a dark surface: a red apple, a yellow lemon, a green bell pepper, and a blue ceramic cup. Sharp focus, studio lighting, clean background, high contrast, perfect for computer vision and object segmentation."*

Este prompt garantizó un fondo homogéneo oscuro y objetos con alto contraste cromático, ideales para probar y validar algoritmos de segmentación y detección basados en color y contornos.

---

## 8. Verificación Manual

El pipeline se verificó manualmente realizando las siguientes comprobaciones:
- Ejecución completa del script `main.py` mediante la consola y verificación de logs correctos.
- Inspección visual de cada una de las imágenes guardadas en el directorio de `resultados/` para confirmar la calidad de la transformación de escala de grises, representación HSV, suavizado Gaussiano, bordes Canny y la correcta superposición geométrica de los contornos (verdes) y cajas delimitadoras (azules).
- Modificación de los parámetros por línea de comandos (ej. variando el kernel de suavizado Gaussiano a `9` y los umbrales de Canny) para observar su impacto directo en los bordes detectados.
