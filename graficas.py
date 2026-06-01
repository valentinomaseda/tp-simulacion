import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats

# Configuramos el panel de 3 filas x 3 columnas
fig, axs = plt.subplots(3, 3, figsize=(15, 12))
fig.suptitle('Distribuciones de Probabilidad Teóricas', fontsize=18, fontweight='bold')

# ==========================================
# 1. CONTINUAS (Curvas)
# ==========================================

# 1. Uniforme Continua [10, 50]
x_uni = np.linspace(0, 60, 1000)
y_uni = stats.uniform.pdf(x_uni, loc=10, scale=40)
axs[0, 0].plot(x_uni, y_uni, 'b-', lw=2)
axs[0, 0].fill_between(x_uni, y_uni, alpha=0.3, color='blue')
axs[0, 0].set_title('Uniforme Continua (a=10, b=50)')

# 2. Exponencial (lambda=2)
x_exp = np.linspace(0, 3, 1000)
y_exp = stats.expon.pdf(x_exp, scale=1/2.0)
axs[0, 1].plot(x_exp, y_exp, 'g-', lw=2)
axs[0, 1].fill_between(x_exp, y_exp, alpha=0.3, color='green')
axs[0, 1].set_title('Exponencial (λ=2)')

# 3. Gamma (k=3, lambda=2)
x_gam = np.linspace(0, 5, 1000)
y_gam = stats.gamma.pdf(x_gam, a=3, scale=1/2.0)
axs[0, 2].plot(x_gam, y_gam, 'r-', lw=2)
axs[0, 2].fill_between(x_gam, y_gam, alpha=0.3, color='red')
axs[0, 2].set_title('Gamma (k=3, λ=2)')

# 4. Normal (mu=0, sigma=1)
x_norm = np.linspace(-4, 4, 1000)
y_norm = stats.norm.pdf(x_norm, 0, 1)
axs[1, 0].plot(x_norm, y_norm, 'm-', lw=2)
axs[1, 0].fill_between(x_norm, y_norm, alpha=0.3, color='magenta')
axs[1, 0].set_title('Normal Estándar (μ=0, σ=1)')

# ==========================================
# 2. DISCRETAS (Barras/Bastones)
# ==========================================

# 5. Pascal / Binomial Negativa (r=5 éxitos, p=0.5)
x_pascal = np.arange(0, 15)
y_pascal = stats.nbinom.pmf(x_pascal, 5, 0.5)
axs[1, 1].vlines(x_pascal, 0, y_pascal, colors='c', lw=4)
axs[1, 1].plot(x_pascal, y_pascal, 'co')
axs[1, 1].set_title('Pascal (r=5, p=0.5)')

# 6. Binomial (N=20, p=0.5)
x_bin = np.arange(0, 21)
y_bin = stats.binom.pmf(x_bin, 20, 0.5)
axs[1, 2].vlines(x_bin, 0, y_bin, colors='orange', lw=4)
axs[1, 2].plot(x_bin, y_bin, 'o', color='orange')
axs[1, 2].set_title('Binomial (N=20, p=0.5)')

# 7. Hipergeométrica (Población=50, Exitos=10, Muestra=15)
x_hyper = np.arange(0, 11)
y_hyper = stats.hypergeom.pmf(x_hyper, 50, 10, 15)
axs[2, 0].vlines(x_hyper, 0, y_hyper, colors='brown', lw=4)
axs[2, 0].plot(x_hyper, y_hyper, 'o', color='brown')
axs[2, 0].set_title('Hipergeométrica (N=50, K=10, n=15)')

# 8. Poisson (lambda=5)
x_poi = np.arange(0, 15)
y_poi = stats.poisson.pmf(x_poi, 5)
axs[2, 1].vlines(x_poi, 0, y_poi, colors='purple', lw=4)
axs[2, 1].plot(x_poi, y_poi, 'o', color='purple')
axs[2, 1].set_title('Poisson (λ=5)')

# 9. Empírica Discreta (Ejemplo propio)
x_emp = np.array([1, 2, 3, 4, 5])
y_emp = np.array([0.1, 0.3, 0.4, 0.15, 0.05])
axs[2, 2].bar(x_emp, y_emp, color='gray', alpha=0.7, edgecolor='black')
axs[2, 2].set_title('Empírica Discreta (Arbitraria)')

# Ajustes visuales finales
for ax in axs.flat:
    ax.set_ylabel('Probabilidad')
    ax.grid(True, linestyle='--', alpha=0.6)

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.savefig('graficas_teoricas.png', dpi=300)
print("¡Imagen 'graficas_teoricas.png' generada con éxito!")