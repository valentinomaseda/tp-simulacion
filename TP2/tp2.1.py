import random
import math
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt

# ==========================================
# 1. GENERADORES PSEUDOALEATORIOS
# ==========================================

def generador_gcl(seed, a, c, m, n):
    """Generador Congruencial Lineal"""
    numeros = []
    x = seed
    for _ in range(n):
        x = (a * x + c) % m
        numeros.append(x / m) # Normalizamos entre 0 y 1
    return numeros

def generador_cuadrados_medios(seed, n):
    """Método de los Cuadrados Medios"""
    numeros = []
    x = seed
    largo = len(str(seed))
    for _ in range(n):
        x_cuadrado = str(x ** 2).zfill(largo * 2) # Rellenamos con ceros a la izq
        mitad_inicio = (len(x_cuadrado) - largo) // 2
        x = int(x_cuadrado[mitad_inicio : mitad_inicio + largo])
        numeros.append(x / (10 ** largo)) # Normalizamos entre 0 y 1
        
        if x == 0: # Evitar estancamiento en 0
            x = seed + len(numeros)
    return numeros

def generador_python(n):
    """Generador nativo de Python (Mersenne Twister)"""
    return [random.random() for _ in range(n)]

# ==========================================
# 2. PRUEBAS ESTADÍSTICAS (TESTS) - estos los podemos elegir nosotros el q queremos si quieren cambiar alguno 
# ==========================================

def test_medias(datos, alpha=0.05):
    """Prueba de Medias (Z-test)"""
    n = len(datos)
    media = np.mean(datos)
    z_calc = (media - 0.5) / (math.sqrt(1/12) / math.sqrt(n))
    z_crit = stats.norm.ppf(1 - alpha/2)
    aprobado = abs(z_calc) < z_crit
    return aprobado, media, z_calc, z_crit

def test_varianza(datos, alpha=0.05):
    """Prueba de Varianza (Chi-Cuadrado)"""
    n = len(datos)
    varianza = np.var(datos, ddof=1)
    chi_calc = ((n - 1) * varianza) / (1/12)
    chi_crit_inf = stats.chi2.ppf(alpha/2, n - 1)
    chi_crit_sup = stats.chi2.ppf(1 - alpha/2, n - 1)
    aprobado = chi_crit_inf < chi_calc < chi_crit_sup
    return aprobado, varianza, chi_calc, (chi_crit_inf, chi_crit_sup)

def test_chi_cuadrado_uniformidad(datos, bins=10, alpha=0.05):
    """Prueba de Chi-Cuadrado para Uniformidad"""
    n = len(datos)
    frec_esperada = n / bins
    frec_observada, _ = np.histogram(datos, bins=bins, range=(0, 1))
    
    chi_calc = sum(((o - frec_esperada)**2) / frec_esperada for o in frec_observada)
    chi_crit = stats.chi2.ppf(1 - alpha, bins - 1)
    aprobado = chi_calc < chi_crit
    return aprobado, chi_calc, chi_crit

def test_rachas(datos, alpha=0.05):
    """Prueba de Rachas (arriba y abajo de la media)"""
    n = len(datos)
    media_teorica = 0.5
    secuencia = [1 if x >= media_teorica else 0 for x in datos]
    
    rachas = 1
    for i in range(1, n):
        if secuencia[i] != secuencia[i-1]:
            rachas += 1
            
    n1 = sum(secuencia)
    n2 = n - n1
    
    # Media y varianza esperada de las rachas
    mu_rachas = ((2 * n1 * n2) / n) + 1
    var_rachas = (2 * n1 * n2 * (2 * n1 * n2 - n)) / ((n ** 2) * (n - 1))
    
    z_calc = (rachas - mu_rachas) / math.sqrt(var_rachas)
    z_crit = stats.norm.ppf(1 - alpha/2)
    aprobado = abs(z_calc) < z_crit
    return aprobado, rachas, z_calc, z_crit

# ==========================================
# 3. EJECUCIÓN Y COMPARACIÓN
# ==========================================

if __name__ == "__main__":
    N = 10000 # Cantidad de números a generar
    
    # Parámetros del GCL (usamos los de un estándar conocido como el de POSIX/glibc)
    semilla = 12345
    a = 1103515245
    c = 12345
    m = 2**31
    
    # Generamos las secuencias
    print(f"Generando {N} números...")
    sec_gcl = generador_gcl(semilla, a, c, m, N)
    sec_cuadrados = generador_cuadrados_medios(8473, N) # Semilla de 4 dígitos
    sec_python = generador_python(N)

    # Evaluación del GCL (Requisito principal)
    print("\n--- RESULTADOS TESTS PARA GCL ---")
    
    ap_media, val_media, z_m, z_m_c = test_medias(sec_gcl)
    print(f"1. Medias: {'Aprobado' if ap_media else 'Rechazado'} (Media={val_media:.4f}, Z_calc={z_m:.4f})")
    
    ap_var, val_var, chi_v, chi_v_c = test_varianza(sec_gcl)
    print(f"2. Varianza: {'Aprobado' if ap_var else 'Rechazado'} (Var={val_var:.4f}, Chi_calc={chi_v:.4f})")
    
    ap_chi, chi_c, chi_c_c = test_chi_cuadrado_uniformidad(sec_gcl, bins=20)
    print(f"3. Chi-Cuadrado: {'Aprobado' if ap_chi else 'Rechazado'} (Chi_calc={chi_c:.4f}, Chi_crit={chi_c_c:.4f})")
    
    ap_rachas, rachas, z_r, z_r_c = test_rachas(sec_gcl)
    print(f"4. Rachas: {'Aprobado' if ap_rachas else 'Rechazado'} (Rachas={rachas}, Z_calc={z_r:.4f})")

    # Evaluación general para armar tabla en LaTeX
    print("\n--- COMPARACIÓN DE GENERADORES (Aprobación de Tests) ---")
    generadores = {
        "GCL": sec_gcl,
        "Cuadrados Medios": sec_cuadrados,
        "Python (M. Twister)": sec_python
    }
    
    print(f"{'Generador':<20} | {'Medias':<8} | {'Varianza':<8} | {'Chi-Cuad':<8} | {'Rachas':<8}")
    print("-" * 60)
    for nombre, sec in generadores.items():
        t1 = "OK" if test_medias(sec)[0] else "ERROR"
        t2 = "OK" if test_varianza(sec)[0] else "ERROR"
        t3 = "OK" if test_chi_cuadrado_uniformidad(sec)[0] else "ERROR"
        t4 = "OK" if test_rachas(sec)[0] else "ERROR"
        print(f"{nombre:<20} | {t1:<8} | {t2:<8} | {t3:<8} | {t4:<8}")

# ==========================================
    # 4. GRÁFICA COMPARATIVA (MAPAS DE BITS)
    # ==========================================
    # Para tener un buen gráfico cuadrado, calculamos el lado (ej: 100x100 = 10000)
    lado = int(math.sqrt(N))
    
    # Recortamos las secuencias para que encajen en una matriz cuadrada perfecta
    matriz_cuadrados = np.array(sec_cuadrados[:lado*lado]).reshape((lado, lado))
    matriz_gcl = np.array(sec_gcl[:lado*lado]).reshape((lado, lado))
    matriz_python = np.array(sec_python[:lado*lado]).reshape((lado, lado))

    plt.figure(figsize=(15, 5))
    
    # Gráfico 1: Cuadrados Medios
    plt.subplot(1, 3, 1)
    plt.imshow(matriz_cuadrados, cmap='gray', interpolation='nearest')
    plt.title('Cuadrados Medios')
    plt.axis('off') # Ocultamos los ejes para que se vea como imagen pura

    # Gráfico 2: GCL
    plt.subplot(1, 3, 2)
    plt.imshow(matriz_gcl, cmap='gray', interpolation='nearest')
    plt.title('Generador Congruencial Lineal (GCL)')
    plt.axis('off')
    
    # Gráfico 3: Python
    plt.subplot(1, 3, 3)
    plt.imshow(matriz_python, cmap='gray', interpolation='nearest')
    plt.title('Python Random')
    plt.axis('off')

    plt.tight_layout()
    plt.savefig('mapas_de_bits_generadores.png')
    print("\nGráfico 'mapas_de_bits_generadores.png' generado exitosamente.")
    plt.show()