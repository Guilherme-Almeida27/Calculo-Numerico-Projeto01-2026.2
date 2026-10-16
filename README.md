# Simulador de Zeros de Funções

Programa em Python que encontra raízes de funções pelos métodos da **Bissecção**, **Falsa Posição**, **Newton-Raphson** e **Secante**, e compara o desempenho dos quatro.

Trabalho da disciplina de **Cálculo Numérico** da **UNIVASF**: Projeto Unidade 1 (Zeros), 2026.2.

---

## O que o programa faz

1. Recebe a função f(x), a derivada f'(x), o intervalo inicial e as estimativas iniciais.
2. Executa os quatro métodos com o mesmo critério de parada: **|f(x)| < ε**.
3. Mostra uma tabela comparativa com a raiz encontrada, o número de iterações, o tempo de execução, o resíduo |f(raiz)| e uma observação sobre falhas.
4. Opcionalmente, mostra dois gráficos:
   - **Função e zeros encontrados:** a curva de f(x) no intervalo [a, b], com a raiz de cada método marcada.
   - **Velocidade de convergência:** |f(x)| a cada iteração, em escala logarítmica, uma curva por método.
5. Pergunta se o usuário quer fazer um novo cálculo ou sair.

---

## Métodos implementados

| Método | Tipo | Precisa de | Fórmula |
|---|---|---|---|
| Bissecção | Intervalo | [a, b] com troca de sinal | `x = (a + b) / 2` |
| Falsa Posição | Intervalo | [a, b] com troca de sinal | `x = (a·f(b) − b·f(a)) / (f(b) − f(a))` |
| Newton-Raphson | Aberto | x0 e f'(x) | `x1 = x0 − f(x0) / f'(x0)` |
| Secante | Aberto | x0 e x1 | `x2 = x1 − f(x1)·(x1 − x0) / (f(x1) − f(x0))` |

Os métodos de intervalo mantêm a raiz sempre dentro de [a, b] e convergem sempre que há troca de sinal. Os métodos abertos convergem mais rápido perto da raiz, mas dependem da estimativa inicial e podem sair do intervalo.

---

## Requisitos

- Python 3.8 ou mais recente
- [matplotlib](https://matplotlib.org/), usado apenas nos gráficos

```bash
pip install matplotlib
```

As demais bibliotecas (`math` e `time`) já vêm com o Python.

---

## Como executar

```bash
git clone [link do repositório]
cd [nome do repositório]
python simulador_zeros.py
```

O programa pede os dados um por um no terminal.

---

## Como digitar a função

A função é lida como uma expressão em Python, então precisa seguir estas regras:

| O que você quer | Como digitar | Não funciona |
|---|---|---|
| Variável | `x` (sempre minúsculo) | `t`, `X` |
| Multiplicação | `2*x`, `5*(1 - exp(-x))` | `2x`, `5(1 - ...)` |
| Potência | `x**3` ou `x^3` | `x³` |
| Número decimal | `0.15` | `0,15` |
| Exponencial eˣ | `exp(x)` | `e^x` |
| Seno, cosseno, tangente | `sen(x)` ou `sin(x)`, `cos(x)`, `tan(x)` | `senx`, `cos x` |
| Logaritmo natural | `ln(x)` ou `log(x)` | |
| Raiz quadrada | `sqrt(x)` | `√x` |
| Constantes | `pi`, `e` | `π` |

Nos campos numéricos (a, b, x0, x1, precisão) também é aceita vírgula decimal: `0,5`. A precisão pode ser digitada como `1e-6`. O máximo de iterações deve ser um número inteiro.

> **Atenção:** a função digitada é executada com `eval()`. Isso é adequado para um programa usado localmente, mas não deve ser usado em sistemas abertos a outras pessoas, porque `eval()` executa qualquer código Python.

---

## Exemplo de uso

Exemplo de teste do enunciado: f(x) = cos(x) − x no intervalo [0, 1].

```text
f(x)  = cos(x) - x
f'(x) = -sen(x) - 1

Intervalo para Bissecção e Falsa Posição:
  a = 0
  b = 1
Newton-Raphson:
  x0 = 0.5
Secante:
  x0 = 0
  x1 = 1

Precisão (ex: 1e-6) = 1e-6
Máximo de iterações = 100

--------------------------------------------------------------------------------------------
Método                    Raiz  Iterações   Tempo (ms)    |f(raiz)|   Observação
--------------------------------------------------------------------------------------------
Bissecção         0.7390851974         20         1.33     1.08e-07   OK
Falsa Posição     0.7390847824          5         0.65     5.87e-07   OK
Newton-Raphson    0.7390851339          3         0.27     1.18e-09   OK
Secante           0.7390851121          4         0.39     3.53e-08   OK
--------------------------------------------------------------------------------------------
```

A raiz de referência é 0,7390851332. Os tempos variam a cada execução e de um computador para outro.

---

## Resultados

Todos os casos com ε = 10⁻⁶. O tempo de execução foi omitido porque varia entre execuções; a comparação se apoia nas iterações e no resíduo.

### Exemplo de teste: f(x) = cos(x) − x

Intervalo [0, 1] · Newton x0 = 0,5 · Secante x0 = 0 e x1 = 1

| Método | Raiz | Iterações | \|f(raiz)\| |
|---|---|---|---|
| Bissecção | 0,7390851974 | 20 | 1,08·10⁻⁷ |
| Falsa Posição | 0,7390847824 | 5 | 5,87·10⁻⁷ |
| Newton-Raphson | 0,7390851339 | 3 | 1,18·10⁻⁹ |
| Secante | 0,7390851121 | 4 | 3,53·10⁻⁸ |

### Problema 1: resfriamento de um componente eletrônico

f(t) = 20 + 90·e^(−0,15t) − 50 · intervalo [0, 15] min · Newton t0 = 0 · Secante t0 = 0 e t1 = 15

Entrada no programa: `20 + 90*exp(-0.15*x) - 50` e `-13.5*exp(-0.15*x)`

| Método | Raiz (min) | Iterações | \|f(raiz)\| |
|---|---|---|---|
| Bissecção | 7,3240819573 | 24 | 1,48·10⁻⁷ |
| Falsa Posição | 7,3240820293 | 23 | 4,72·10⁻⁷ |
| Newton-Raphson | 7,3240819244 | 5 | 3,97·10⁻¹⁰ |
| Secante | 7,3240820811 | 7 | 7,05·10⁻⁷ |

Solução analítica: t = ln(3) / 0,15 ≈ 7,3241 min.

### Problema 2: carregamento de um capacitor RC

f(t) = 5·(1 − e^(−t)) − 3,8 · intervalo [0, 3] s · Newton t0 = 0 · Secante t0 = 0 e t1 = 3

Entrada no programa: `5*(1 - exp(-x)) - 3.8` e `5*exp(-x)`

| Método | Raiz (s) | Iterações | \|f(raiz)\| |
|---|---|---|---|
| Bissecção | 1,4271168709 | 21 | 6,18·10⁻⁷ |
| Falsa Posição | 1,4271170326 | 25 | 8,12·10⁻⁷ |
| Newton-Raphson | 1,4271163488 | 5 | 8,18·10⁻⁹ |
| Secante | 1,4271163561 | 9 | 5,55·10⁻¹⁰ |

Solução analítica: t = −ln(0,24) ≈ 1,4271 s.

### Resumo

- **Newton-Raphson** foi o mais rápido nos três casos (3 a 5 iterações), pela convergência quadrática perto da raiz.
- **Secante** ficou logo atrás (4 a 9 iterações), sem precisar da derivada.
- **Bissecção** foi previsível (20 a 24 iterações): o intervalo cai à metade a cada passo.
- **Falsa Posição** variou muito (5 a 25 iterações). Nos dois problemas a curva é dobrada sempre para o mesmo lado no intervalo, uma das pontas fica fixa, e o método chegou a ser mais lento que a Bissecção.

---

## Falhas tratadas

O programa não trava nessas situações; o motivo aparece na coluna **Observação** da tabela.

| Observação | Quando acontece | Métodos |
|---|---|---|
| `Falha: não há mudança de sinal no intervalo` | f(a) e f(b) têm o mesmo sinal | Bissecção, Falsa Posição |
| `Falha: derivada nula` | f'(x) = 0 em alguma iteração | Newton-Raphson |
| `Falha: divisão por zero` | f(b) = f(a), ou f(x1) = f(x0) | Falsa Posição, Secante |
| `OK (saiu do intervalo)` | o método convergiu, mas em algum passo x saiu de [a, b] | Newton-Raphson, Secante |
| `Não convergiu` | atingiu o máximo de iterações sem \|f(x)\| < ε | todos |

Quando aparecer `OK (saiu do intervalo)`, confira a raiz: o método pode ter encontrado outra raiz da função, fora do intervalo pedido.

Erros de digitação (função inválida, valor não numérico) mostram a mensagem de erro e voltam para a pergunta de novo cálculo.

---

## Estrutura do código

O código está todo no arquivo `simulador_zeros.py`:

| Parte | Função |
|---|---|
| `bisseccao`, `falsa_posicao`, `newton`, `secante` | Os quatro métodos. Cada um devolve a raiz, o número de iterações e a observação. |
| `historico` | Guarda \|f(x)\| de cada iteração de cada método, usado no gráfico de convergência. |
| `medir` | Executa um método e mede o tempo com `time.perf_counter()`. |
| `ler_numero` | Lê um número do teclado, aceitando vírgula ou ponto decimal. |
| `mostrar_grafico` | Desenha o gráfico da função e o gráfico de convergência. |
| Bloco `if __name__ == "__main__":` | Entrada de dados, tabela comparativa e repetição do cálculo. |

---

## Equipe

| Integrante | Participação |
|---|---|
| [Nome 1] | [descrição] |
| [Nome 2] | [descrição] |
| [Nome 3] | [descrição] |
