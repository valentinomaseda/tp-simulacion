import math
import random
import matplotlib.pyplot as plt

# ==========================================
# 1. FUNCIONES GENERADORAS
# ==========================================

def gen_uniforme_continua(a, b, n):
    return [a + (b - a) * random.random() for _ in range(n)]

def gen_exponencial_inversa(lam, n):
    numeros = []
    for _ in range(n):
        R = random.random()
        if R == 1.0: R = 0.999999 
        numeros.append((-1 / lam) * math.log(1 - R))
    return numeros

def gen_normal_rechazo(mu, sigma, n):
    numeros = []
    while len(numeros) < n:
        R1 = 2 * random.random() - 1
        R2 = 2 * random.random() - 1
        W = R1**2 + R2**2
        if W < 1 and W != 0:
            Y = math.sqrt((-2 * math.log(W)) / W)
            numeros.append(mu + sigma * (R1 * Y))
            if len(numeros) < n:
                numeros.append(mu + sigma * (R2 * Y))
    return numeros

def gen_binomial_rechazo(N_ensayos, p_exito, n):
    numeros = []
    for _ in range(n):
        exitos = sum(1 for _ in range(N_ensayos) if random.random() <= p_exito)
        numeros.append(exitos)
    return numeros

def gen_poisson_inversa(lam, n):
    numeros = []
    L = math.exp(-lam)
    for _ in range(n):
        k, p = 0, 1.0
        while p > L:
            k += 1
            p *= random.random()
        numeros.append(k - 1)
    return numeros

def gen_empirica_discreta(valores, probabilidades, n):
    numeros = []
    prob_acumulada = [sum(probabilidades[:i+1]) for i in range(len(probabilidades))]
    for _ in range(n):
        R = random.random()
        for i, p_acum in enumerate(prob_acumulada):
            if R <= p_acum:
                numeros.append(valores[i])
                break
    return numeros

# ==========================================
# 2. GENERACIÓN DE DATOS (TESTEO)
# ==========================================

if __name__ == "__main__":
    cantidad = 5000 # 5000 números para que la curva quede bien definida
    
    print("Generando datos...")
    datos_uni = gen_uniforme_continua(a=10, b=50, n=cantidad)
    datos_exp = gen_exponencial_inversa(lam=2.0, n=cantidad)
    datos_norm = gen_normal_rechazo(mu=100, sigma=15, n=cantidad)
    datos_bin = gen_binomial_rechazo(N_ensayos=20, p_exito=0.5, n=cantidad)
    datos_poi = gen_poisson_inversa(lam=5.0, n=cantidad)
    
    # Para la empírica, inventamos un caso: Venta de autos diarios y su probabilidad
    valores_emp = [0, 1, 2, 3, 4]
    probs_emp = [0.10, 0.40, 0.30, 0.15, 0.05]
    datos_emp = gen_empirica_discreta(valores_emp, probs_emp, n=cantidad)

    # ==========================================
    # 3. ARMADO DEL PANEL DE GRÁFICOS
    # ==========================================
    
    print("Armando gráficos...")
    # Creamos una figura grande con 2 filas y 3 columnas
    fig, axs = plt.subplots(2, 3, figsize=(16, 9))
    fig.suptitle('Testeo de Generadores por Distribución de Probabilidad', fontsize=18, fontweight='bold')

    # 1. Uniforme
    axs[0, 0].hist(datos_uni, bins=30, color='skyblue', edgecolor='black', density=True)
    axs[0, 0].set_title('Uniforme Continua [10, 50]')
    
    # 2. Exponencial
    axs[0, 1].hist(datos_exp, bins=40, color='lightgreen', edgecolor='black', density=True)
    axs[0, 1].set_title('Exponencial (λ=2.0)')
    
    # 3. Normal
    axs[0, 2].hist(datos_norm, bins=40, color='salmon', edgecolor='black', density=True)
    axs[0, 2].set_title('Normal (μ=100, σ=15)')
    
    # 4. Binomial (Gráfico de barras discretas)
    bins_bin = range(min(datos_bin), max(datos_bin) + 2)
    axs[1, 0].hist(datos_bin, bins=bins_bin, align='left', color='gold', edgecolor='black', density=True)
    axs[1, 0].set_title('Binomial (N=20, p=0.5)')
    axs[1, 0].set_xticks(range(min(datos_bin), max(datos_bin) + 1))
    
    # 5. Poisson (Gráfico de barras discretas)
    bins_poi = range(min(datos_poi), max(datos_poi) + 2)
    axs[1, 1].hist(datos_poi, bins=bins_poi, align='left', color='plum', edgecolor='black', density=True)
    axs[1, 1].set_title('Poisson (λ=5.0)')
    axs[1, 1].set_xticks(range(min(datos_poi), max(datos_poi) + 1))
    
    # 6. Empírica Discreta
    bins_emp = range(min(datos_emp), max(datos_emp) + 2)
    axs[1, 2].hist(datos_emp, bins=bins_emp, align='left', color='tan', edgecolor='black', density=True)
    axs[1, 2].set_title('Empírica Discreta')
    axs[1, 2].set_xticks(valores_emp)

    # Ajuste visual y guardado
    plt.tight_layout(rect=[0, 0.03, 1, 0.95]) # Deja espacio para el título principal
    plt.savefig('distribuciones_testeo.png', dpi=300) # Guardamos en alta calidad
    print("¡Listo! Imagen 'distribuciones_testeo.png' generada con éxito.")