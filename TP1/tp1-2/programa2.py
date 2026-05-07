import random
import matplotlib.pyplot as plt
import argparse
import numpy as np

def generar_fibonacci(n):
    fib = [1, 1]
    for i in range(2, n):
        fib.append(fib[i-1] + fib[i-2])
    return fib

def simular_ruleta():
    parser = argparse.ArgumentParser(description='Simulación de Apuestas UTN-FRRO')
    parser.add_argument('-c', type=int, required=True, help='Cantidad de corridas')
    parser.add_argument('-n', type=int, required=True, help='Cantidad de tiradas')
    parser.add_argument('-s', choices=['m', 'd', 'f', 'o'], required=True, help='Estrategia: m (Martingala), d (D\'Alembert), f (Fibonacci), o (Jacobo)')
    parser.add_argument('-a', choices=['f', 'i'], required=True, help='Capital: f (Finito), i (Infinito)')
    # parser.add_argument('-i', type=int, default=1000, help='Capital inicial (fci)')
    args = parser.parse_args()

    # FCI = args.i
    FCI = 1000
    UNIDAD_APUESTA = 10
    secuencia_fib = generar_fibonacci(args.n + 2)
    
    bancarrotas = 0
    resultados_capitales = []
    resultados_frsa = [] # Frecuencia relativa de apuesta favorable

    for corrida in range(args.c):
        capital = FCI
        historial_capital = [FCI]
        exitos_apuesta = 0
        frsa_acumulada = []
        
        # Variables de control de estrategia
        apuesta_actual = UNIDAD_APUESTA
        idx_fib = 0 # Para Fibonacci
        
        for t in range(1, args.n + 1):
            # Validar capital finito
            if args.a == 'f' and capital < apuesta_actual:
                bancarrotas += 1
                # Rellenar con ceros para que todas las listas tengan el mismo largo al graficar
                historial_capital.extend([0] * (args.n - len(historial_capital) + 1))
                frsa_acumulada.extend([exitos_apuesta / max(1, len(frsa_acumulada))] * (args.n - len(frsa_acumulada)))
                break

            tiro = random.randint(0, 36)
            gano = False
            pago = 0

            # --- Lógica de Estrategias ---
            if args.s in ['m', 'd', 'f']: # Apuestas a PAR (Dinero parejo)
                gano = (tiro % 2 == 0 and tiro != 0)
                if gano:
                    capital += apuesta_actual
                    exitos_apuesta += 1

                    # Ajuste de apuesta según estrategia
                    if args.s == 'm': apuesta_actual = UNIDAD_APUESTA
                    elif args.s == 'd': apuesta_actual = max(UNIDAD_APUESTA, apuesta_actual - UNIDAD_APUESTA)
                    elif args.s == 'f': 
                        idx_fib = max(0, idx_fib - 2)
                        apuesta_actual = secuencia_fib[idx_fib] * UNIDAD_APUESTA

                else: #si no gano
                    capital -= apuesta_actual
                    if args.s == 'm': apuesta_actual *= 2
                    elif args.s == 'd': apuesta_actual += UNIDAD_APUESTA
                    elif args.s == 'f':
                        idx_fib += 1
                        apuesta_actual = secuencia_fib[idx_fib] * UNIDAD_APUESTA

            # Metodo de Jacobo - Cobertura
            elif args.s == 'o': 
                if 19 <= tiro <= 36: # Números altos
                    capital += (apuesta_actual * 0.7) # Ganancia neta simplificada
                    gano = True
                elif 13 <= tiro <= 18: # Seisena
                    capital += (apuesta_actual * 1.0)
                    gano = True
                elif tiro == 0: # Seguro al cero
                    capital += (apuesta_actual * 1.6)
                    gano = True
                else: # 1 al 12 pierde
                    capital -= apuesta_actual
                
                if gano: exitos_apuesta += 1

            historial_capital.append(capital)
            frsa_acumulada.append(exitos_apuesta / t)

        resultados_capitales.append(historial_capital)
        resultados_frsa.append(frsa_acumulada)

    # --- Gráficos ---
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 10))
    t_eje = range(len(resultados_capitales[0]))

    # Gráfico de Flujo de Caja (fc)
    for cap in resultados_capitales:
        ax1.plot(cap, alpha=0.5)
    ax1.axhline(y=FCI, color='black', linestyle='--', label='Capital Inicial')
    ax1.set_title(f'Flujo de Caja - Estrategia: {args.s.upper()} - Capital: {"Finito" if args.a == "f" else "Infinito"}')
    ax1.set_ylabel('CC (Cantidad de Capital)')

    # Gráfico de Frecuencia Relativa de Éxitos (frsa)
    for fr in resultados_frsa:
        ax2.plot(range(1, len(fr)+1), fr, alpha=0.5)
    ax2.set_title('Frecuencia Relativa de Apuestas Favorables')
    ax2.set_xlabel('Número de tiradas (n)')
    ax2.set_ylabel('fr')

    print(f"Simulación finalizada.")
    if args.a == 'f':
        print(f"Bancarrotas: {bancarrotas} de {args.c} corridas ({(bancarrotas/args.c)*100}%).")

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    simular_ruleta()