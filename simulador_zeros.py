# Simulador de Zeros de Funções - Cálculo Numérico (UNIVASF)
# Métodos: Bissecção, Falsa Posição, Newton-Raphson e Secante
#
# Como executar:  python simulador_zeros.py
# Para os gráficos é preciso ter o matplotlib:  pip install matplotlib

import time
from math import *
import matplotlib.pyplot as plt


sen = sin   # para poder digitar sen(x)
ln = log    # para poder digitar ln(x)
historico = {}  # guarda |f(x)| em cada iteração para cada método

# ---------------------------------------------------------------
# MÉTODOS
# Todos param quando |f(x)| < eps ou quando chegam em max_iter.
# Todos devolvem: raiz, número de iterações e uma observação.
# Se o método falhar, a raiz devolvida é None.
# ---------------------------------------------------------------


#X = (a + b) / 2
def bisseccao(f, a, b, eps, max_iter):
    historico["Bissecção"] = [] 
    if f(a) * f(b) > 0:
        return None, 0, "Falha: não há mudança de sinal no intervalo"
    for k in range(1, max_iter + 1):
        x = (a + b) / 2                 # ponto médio
        historico["Bissecção"].append(abs(f(x)))
        if abs(f(x)) < eps:
            return x, k, "OK"
        if f(a) * f(x) < 0:             #a raiz está entre a e x
            b = x
        else:                           #a raiz está entre x e b
            a = x
    return x, max_iter, "Não convergiu"


#X = (a * f(b) - b * f(a)) / (f(b) - f(a))
def falsa_posicao(f, a, b, eps, max_iter):
    historico["Falsa Posição"] = []
    if f(a) * f(b) > 0:
        return None, 0, "Falha: não há mudança de sinal no intervalo"

    for k in range(1, max_iter + 1):
        if f(b) - f(a) == 0:
            return None, k, "Falha: divisão por zero"
        x = (a * f(b) - b * f(a)) / (f(b) - f(a))   # onde a reta corta o eixo x
        historico["Falsa Posição"].append(abs(f(x)))
        if abs(f(x)) < eps:
            return x, k, "OK"
        if f(a) * f(x) < 0:
            b = x
        else:
            a = x
    return x, max_iter, "Não convergiu"


#X1 = X0 - f(X0) / f'(X0)
def newton(f, df, x0, a, b, eps, max_iter):
    historico["Newton-Raphson"] = []
    x = x0
    obs = "OK"
    for k in range(1, max_iter + 1):
        if df(x) == 0:
            return None, k, "Falha: derivada nula"
        x = x - f(x) / df(x)
        historico["Newton-Raphson"].append(abs(f(x)))
        if x < a or x > b:              # só avisa, o método continua
            obs = "OK (saiu do intervalo)"
        if abs(f(x)) < eps:
            return x, k, obs
    return x, max_iter, "Não convergiu"



#X2 = X1 - [f(X1) * (X1 - X0) / (f(X1) - f(X0))]
def secante(f, x0, x1, a, b, eps, max_iter):
    historico["Secante"] = []
    obs = "OK"
    for k in range(1, max_iter + 1):
        if f(x1) - f(x0) == 0:
            return None, k, "Falha: divisão por zero"
        x2 = x1 - f(x1) * (x1 - x0) / (f(x1) - f(x0))
        historico["Secante"].append(abs(f(x2)))
        if x2 < a or x2 > b:
            obs = "OK (saiu do intervalo)"
        if abs(f(x2)) < eps:
            return x2, k, obs
        x0 = x1
        x1 = x2
    return x2, max_iter, "Não convergiu"


# ---------------------------------------------------------------
# FUNÇÕES AUXILIARES
# ---------------------------------------------------------------

def ler_numero(texto):
    # aceita vírgula ou ponto, e também coisas como 1e-6
    return float(input(texto).replace(",", "."))



def medir(metodo, *argumentos):
    # roda o método e mede o tempo em mili  ssegundos
    inicio = time.perf_counter()
    raiz, iteracoes, obs = metodo(*argumentos)
    fim = time.perf_counter()
    tempo = (fim - inicio) * 1000
    return raiz, iteracoes, tempo, obs



def mostrar_grafico(f, a, b, nomes, resultados):
    marcadores = ["o", "s", "^", "x"]
    plt.figure(figsize=(12, 5))

    # ---- gráfico 1: a função e os zeros encontrados ----
    plt.subplot(1, 2, 1)

    # 200 pontos entre a e b para desenhar a curva
    xs = []
    ys = []
    for i in range(201):
        x = a + i * (b - a) / 200
        xs.append(x)
        ys.append(f(x))

    plt.plot(xs, ys, label="f(x)")
    plt.axhline(0, color="black", linewidth=0.8)
    for i in range(4):
        raiz = resultados[i][0]
        if raiz is not None:
            plt.plot(raiz, 0, marcadores[i], markersize=10, fillstyle="none",
                     label=nomes[i] + ": " + format(raiz, ".10f"))
    plt.title("Função e zeros encontrados")
    plt.xlabel("x")
    plt.ylabel("f(x)")
    plt.grid(True)
    plt.legend()

    # ---- gráfico 2: velocidade de convergência ----
    # mostra |f(x)| em cada iteração; quanto mais rápido a curva desce,
    # mais rápido o método converge
    plt.subplot(1, 2, 2)
    for i in range(4):
        residuos = historico[nomes[i]]
        iteracoes = range(1, len(residuos) + 1)
        plt.plot(iteracoes, residuos, marker=marcadores[i], label=nomes[i])
    plt.yscale("log")       # escala logarítmica, porque |f(x)| cai muito rápido
    plt.title("Velocidade de convergência")
    plt.xlabel("Iteração")
    plt.ylabel("|f(x)|")
    plt.grid(True)
    plt.legend()

    plt.tight_layout()
    plt.show()





if __name__ == "__main__":

    print("=" * 60)
    print(" SIMULADOR DE ZEROS DE FUNÇÕES")
    print("=" * 60)
    print("Escreva a função usando x. Exemplos: cos(x) - x   x**3 - 2*x - 5")
    print("Pode usar: sin/sen, cos, tan, exp, log/ln, sqrt, pi, e")

    continuar = "s"
    while continuar == "s":
        try:

            print()
            texto_f = input("f(x)  = ").replace("^", "**")
            texto_df = input("f'(x) = ").replace("^", "**")

            #transforma o texto em função que é reconhcida pelo Python. Exemplo: "cos(x) - x" para x = 0,5 faz cos(0,5) - 0,5, retornando 0,37758
            def f(x):
                return eval(texto_f) 

            def df(x):
                return eval(texto_df)

            print("\nIntervalo para Bissecção e Falsa Posição:")
            a = ler_numero("  a = ")
            b = ler_numero("  b = ")
            print("Newton-Raphson:")
            x0_newton = ler_numero("  x0 = ")
            print("Secante:")
            
            x0_sec = ler_numero("  x0 = ")
            x1_sec = ler_numero("  x1 = ")
            eps = ler_numero("\nPrecisão (ex: 1e-6) = ")
            max_iter = int(input("Máximo de iterações = "))

            # ---- cálculo ----
            nomes = ["Bissecção", "Falsa Posição", "Newton-Raphson", "Secante"]
            resultados = [
                medir(bisseccao, f, a, b, eps, max_iter),
                medir(falsa_posicao, f, a, b, eps, max_iter),
                medir(newton, f, df, x0_newton, a, b, eps, max_iter),
                medir(secante, f, x0_sec, x1_sec, a, b, eps, max_iter),
            ]

            # ---- tabela comparativa ----
            print()
            print("-" * 92)
            print(f"{'Método':<16}{'Raiz':>14}{'Iterações':>11}{'Tempo (ms)':>13}{'|f(raiz)|':>13}   Observação")
            print("-" * 92)
            for i in range(4):
                raiz, iteracoes, tempo, obs = resultados[i]
                if raiz is None:
                    print(f"{nomes[i]:<16}{'---':>14}{iteracoes:>11}{tempo:>13.2f}{'---':>13}   {obs}")
                else:
                    print(f"{nomes[i]:<16}{raiz:>14.10f}{iteracoes:>11}{tempo:>13.2f}{abs(f(raiz)):>13.2e}   {obs}")
            print("-" * 92)

            # ---- gráfico ----
            if input("\nMostrar o gráfico? (s/n): ").lower() == "s": 
                mostrar_grafico(f, a, b, nomes, resultados)

        except Exception as erro:
            print("\nErro:", erro)
            print("Confira a função e os valores digitados.")

        continuar = input("\nFazer um novo cálculo? (s/n): ").lower()

    print("Programa encerrado.")
