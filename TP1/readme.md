# Simulación de Ruleta y Estudio de Estrategias de Apuestas
### UTN FRRO - Cátedra de Simulación (2026)

Este repositorio contiene el desarrollo de los Trabajos Prácticos 1.1 y 1.2 para la materia **Simulación**[1, 29]. El proyecto consiste en un software desarrollado en Python que simula el funcionamiento del plato de una ruleta, realiza análisis estadísticos de los resultados y evalúa diferentes estrategias económicas de apuesta[2, 34].

## 📋 Descripción del Proyecto

El sistema está dividido en dos grandes objetivos:
1.  **TP 1.1 - Análisis Estadístico:** Verificación de la aleatoriedad de la ruleta mediante el estudio de frecuencias relativas, valores promedio, varianza y desvío estándar a lo largo de $n$ tiradas[2, 12].
2.  **TP 1.2 - Estudio Económico:** Simulación de flujos de caja aplicando estrategias clásicas de apuestas bajo condiciones de capital finito e infinito[29, 34, 40].

## 🚀 Requisitos Técnicos

* **Lenguaje:** Python 3.x[6, 34].
* **Librerías principales:** `Matplotlib` (para la generación de gráficos)[9, 37].
    * `NumPy` o `Statistics` (para el procesamiento de datos estadísticos)[9].

## 💻 Uso y Parámetros

El programa se ejecuta a través de la consola permitiendo configurar los parámetros de la simulación mediante flags[10, 41]:

```bash
python programa.py -c <corridas> -n <tiradas> -e <numero> -s <estrategia> -a <capital>
```

### Detalle de argumentos:
* `-c XXX`: Cantidad de corridas del experimento[11, 41].
* `-n YYY`: Cantidad de tiradas por cada corrida[11, 41].
* `-e ZZ`: Número elegido para la apuesta (0-36 o 00)[11, 41].
* `-s`: Estrategia utilizada[39]:
    * `m`: Martingala.
    * `d`: D'Alembert.
    * `f`: Fibonacci.
    * `o`: Otra estrategia.
* `-a`: Tipo de capital[40]:
    * `i`: Infinito.
    * `f`: Finito.

## 📊 Gráficos Generados

El sistema genera un mínimo de **8 gráficas** para el análisis[14]:
1.  **Frecuencia relativa** (frn) vs. esperada (fre)[12].
2.  **Valor promedio** de las tiradas (vpn) vs. esperado (vpe)[12].
3.  **Valor de la varianza** (vvn) vs. esperada (vve)[12].
4.  **Valor del desvío** (vdn) vs. esperado (vde)[12].
5.  **Flujo de caja** (fc) según la estrategia y capital[40].
6.  **Frecuencia relativa de obtener apuestas favorables** (frsa)[40].

## 📄 Informe en LaTeX

Siguiendo las pautas de la cátedra, el informe académico se encuentra desarrollado en **LaTeX** utilizando el template de la Cornell University[16, 26, 53]. 

**Secciones incluidas en el informe[23, 51]:**
* Abstract (Resumen).
* Introducción y Marco Teórico (Teorema Central del Límite, estadísticos)[15, 24].
* Metodología.
* Análisis de resultados y discusión.
* Conclusiones.
* Referencias bibliográficas[24].

## 👥 Autores
* **Juan I. Torres** (Docente/Autor original de la guía)[1, 29].
* *Insertar nombre de los integrantes del grupo aquí*

---
*Este proyecto fue realizado para la Universidad Tecnológica Nacional - Facultad Regional Rosario (UTN-FRRO)*[1, 29].

<!---## Referencias

Completar la lista de referencias numeradas usadas en el texto. Ejemplo:

1. Autor A. Título. Año.
2. Autor B. Título. Año.

(Sustituir por las referencias reales y ordenar por número).
--->