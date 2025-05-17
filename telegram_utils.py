from analise import analisar_jogos_hoje, analisar_jogo_especifico
from previsao import prever_resultado_ia
from apostas import sugestao_aposta_simples

# Função para analisar jogos de hoje (sem parâmetros)
def analisar_jogos():
    return analisar_jogos_hoje()

# Função para analisar um jogo específico
def analisar_jogo_individual(jogo):
    return analisar_jogo_especifico(jogo)

# Previsão com IA
def prever_resultado(jogo):
    return prever_resultado_ia(jogo)

# Sugestão de aposta simples
def sugestao_aposta():
    return sugestao_aposta_simples()
