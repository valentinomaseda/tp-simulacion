import random
import matplotlib.pyplot as plt
import argparse

def simular_ruleta():
    # Configuración de argumentos por consola 
    parser = argparse.ArgumentParser(description='Simulación de Ruleta UTN-FRRO')
    parser.add_argument('-c', type=int, required=True, help='Cantidad de corridas')
    parser.add_argument('-n', type=int, required=True, help='Cantidad de tiradas por corrida')
    parser.add_argument('-e', type=int, required=True, help='Número elegido (0-36)')
    args = parser.parse_args()

    # Parámetros teóricos
    NUMEROS_TOTALES = 37
    FRECUENCIA_ESPERADA = 1 / NUMEROS_TOTALES
    VALOR_PROMEDIO_ESPERADO = 18.0
    VARIANZA_ESPERADA = 114.0
    DESVIO_ESPERADO = VARIANZA_ESPERADA ** 0.5

    # Listas para almacenar datos de múltiples corridas 
    todas_frecuencias = []
    todos_promedios = []
    todas_varianzas = []
    todos_desvios = []

    # Estructura FOR para iterar las corridas 
    for corrida in range(args.c):
        resultados = []
        frecuencias_acum = []
        promedios_acum = []
        varianzas_acum = []
        desvios_acum = []
        exitos = 0

        for i in range(1, args.n + 1):
            # Generación de valores aleatorios enteros 
            tiro = random.randint(0, 36)
            resultados.append(tiro)

            # Frecuencia relativa del número elegido
            if tiro == args.e:
                exitos += 1
            frecuencias_acum.append(exitos / i)

            # Funciones estadísticas básicas [cite: 32]
            promedio_actual = sum(resultados) / i
            promedios_acum.append(promedio_actual)

            if i > 1:
                suma_cuadrados = 0 
                for x in resultados: 
                    suma_cuadrados += (x - promedio_actual)**2  
                var = suma_cuadrados / i            
            else:
                var = 0
            varianzas_acum.append(var)
            desvios_acum.append(var**0.5)

        todas_frecuencias.append(frecuencias_acum)
        todos_promedios.append(promedios_acum)
        todas_varianzas.append(varianzas_acum)
        todos_desvios.append(desvios_acum)

    # Gráficos de los resultados mediante Matplotlib [cite: 33]
    tiradas_eje = list(range(1, args.n + 1))
    fig, axs = plt.subplots(2, 2, figsize=(12, 8))
    fig.suptitle(f'Resultados de {args.c} corridas - Número elegido: {args.e}')

    # Frecuencia Relativa
    for f in todas_frecuencias:
        axs[0, 0].plot(tiradas_eje, f, alpha=0.4)
    axs[0, 0].axhline(y=FRECUENCIA_ESPERADA, color='r', label='Esperada')
    axs[0, 0].set_title('Frecuencia Relativa')
    axs[0, 0].legend()

    # Valor Promedio
    for p in todos_promedios:
        axs[0, 1].plot(tiradas_eje, p, alpha=0.4)
    axs[0, 1].axhline(y=VALOR_PROMEDIO_ESPERADO, color='r', label='Esperado')
    axs[0, 1].set_title('Valor Promedio')

    # Desvío
    for d in todos_desvios:
        axs[1, 0].plot(tiradas_eje, d, alpha=0.4)
    axs[1, 0].axhline(y=DESVIO_ESPERADO, color='r', label='Esperado')
    axs[1, 0].set_title('Valor del Desvío')

    # Varianza
    for v in todas_varianzas:
        axs[1, 1].plot(tiradas_eje, v, alpha=0.4)
    axs[1, 1].axhline(y=VARIANZA_ESPERADA, color='r', label='Esperada')
    axs[1, 1].set_title('Valor de la Varianza')

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    simular_ruleta()