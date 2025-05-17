
from datetime import datetime, timedelta

def analisar_jogos_antecipados():
    hoje = datetime.now().date()
    dias = [hoje + timedelta(days=i) for i in range(4)]
    resultados = []
    for dia in dias:
        resultados.append(f"📅 Análises para o dia {dia.strftime('%d/%m/%Y')}:
- Flamengo x Vasco
- Palmeiras x Santos")
    return "\n\n".join(resultados)

def analisar_partida_especifica(nome_partida):
    return f"📊 Análise da partida: {nome_partida}\n🔍 Chances equilibradas, últimos jogos indicam empate.\n🔥 Estatísticas mostram alta média de gols.\nSugestão: Ambas marcam."
