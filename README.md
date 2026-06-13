# Examen Final de Computación Visual 2026-I

**Universidad Nacional de Colombia**  
**Curso:** Computación Visual  
**Estudiante:** Carlos Arturo Murcia Andrade  
**Componente:** Entrega práctica (Repositorio individual)  

Este repositorio contiene las soluciones para el examen final de la asignatura Computación Visual. De acuerdo con las instrucciones, esta entrega se centra en el **Ejercicio 1: Procesamiento visual e IA**.

---

## 🚀 Estructura del Repositorio

La organización del proyecto sigue la estructura especificada en la guía de entrega:

```text
examen-final-computacion-visual-carlos-arturo-murcia-andrade/
├── Instrucciones.pdf                        # Guía de requisitos del examen
├── README.md                                # Documentación principal (este archivo)
└── ejercicio_1_procesamiento_visual/        # Carpeta del Ejercicio 1
    ├── README.md                            # Documentación detallada del Ejercicio 1
    ├── data/
    │   └── input.png                        # Imagen de entrada de prueba
    ├── resultados/                          # Salidas intermedias y finales del pipeline
    │   ├── original.png
    │   ├── grises.png
    │   ├── hsv_o_lab.png
    │   ├── suavizado.png
    │   ├── bordes.png
    │   └── deteccion_o_segmentacion.png
    └── src/
        └── main.py                          # Código fuente en Python del pipeline
```

---

## 🛠️ Requisitos y Dependencias

Para poder ejecutar el código fuente reproducible de este proyecto, se requiere tener instalado:

- **Python**: Versión `3.12.x` o superior.
- **OpenCV (opencv-python)**: Versión `4.13.0` o superior.
- **NumPy**: Versión `2.4.4` o superior.

---

## 📦 Instalación y Configuración

1. **Clonar el repositorio**:
   ```bash
   git clone https://github.com/carlos-murcia/examen-final-computacion-visual-carlos-arturo-murcia-andrade.git
   cd examen-final-computacion-visual-carlos-arturo-murcia-andrade
   ```

2. **Instalar dependencias necesarias**:
   Puedes instalar los requerimientos utilizando `pip`:
   ```bash
   pip install opencv-python numpy
   ```

---

## ⚙️ Ejecución del Ejercicio 1

El pipeline de procesamiento visual está programado en Python y se encuentra en `ejercicio_1_procesamiento_visual/src/main.py`.

Para ejecutarlo con los parámetros por defecto, corre el siguiente comando desde la raíz del repositorio:

```bash
python ejercicio_1_procesamiento_visual/src/main.py
```

### Parámetros Configurables
El script admite argumentos por línea de comandos para facilitar su trazabilidad y experimentación con otros valores de umbrales y kernels:

```bash
python ejercicio_1_procesamiento_visual/src/main.py \
  --input ejercicio_1_procesamiento_visual/data/input.png \
  --output_dir ejercicio_1_procesamiento_visual/resultados \
  --blur_kernel 5 \
  --canny_low 50 \
  --canny_high 150 \
  --min_area 1000
```

---

## 📊 Resumen del Ejercicio 1

El **Ejercicio 1** consiste en un pipeline secuencial de procesamiento digital de imágenes que realiza las siguientes operaciones obligatorias:

1. **Cargar entrada visual**: Carga una imagen de alta calidad (`input.png`) usando OpenCV.
2. **Escala de grises**: Conversión BGR a Grises para simplificar los cálculos de intensidad.
3. **Segundo espacio de color**: Conversión a espacio **HSV** para analizar la escena separando la luminancia de los tonos cromáticos.
4. **Suavizado**: Aplicación de un **filtro Gaussiano** para reducir ruidos locales.
5. **Detección de bordes**: Algoritmo de **Canny** con histéresis para resaltar contornos estructurales.
6. **Segmentación y Detección**: Umbralización automática con **Otsu**, filtrado morfológico de ruido, y detección de contornos externos para delimitar y etiquetar objetos, calculando métricas geométricas (Área, Perímetro, Centroide y Circularidad).
7. **Guardar resultados**: Almacena cada una de las salidas intermedias y finales en la carpeta `resultados/` para permitir una comparación visual directa.

Para ver el análisis técnico detallado, los parámetros elegidos, las justificaciones científicas, dificultades encontradas y evidencias visuales adicionales, por favor consulta el **[README del Ejercicio 1](file:///e:/Backup/computer_science/Unal/VisualComputing/computacion-visual-camurcioa/examen-final-computacion-visual-carlos-arturo-murcia-andrade/ejercicio_1_procesamiento_visual/README.md)**.
