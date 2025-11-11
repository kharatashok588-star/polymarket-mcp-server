#!/usr/bin/env python3
"""
ULTRA DEEP ANALYSIS - Government Shutdown Markets
Análise completa de todos os markets relacionados ao shutdown
"""
import sys
sys.path.insert(0, 'src')

import asyncio
import httpx
import json
from datetime import datetime
from collections import defaultdict

async def deep_shutdown_analysis():
    """Análise profunda dos markets de government shutdown"""

    print("\n" + "="*90)
    print("🏛️  ULTRA DEEP ANALYSIS - GOVERNMENT SHUTDOWN")
    print("="*90)
    print(f"📅 Análise em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    async with httpx.AsyncClient(timeout=30.0) as client:
        # 1. Buscar TODOS os markets sobre shutdown
        print("🔍 Fase 1: Buscando todos os markets relacionados ao shutdown...\n")

        response = await client.get(
            'https://gamma-api.polymarket.com/markets',
            params={'limit': 100, 'closed': 'false'}
        )
        all_markets = response.json()

        # Filtrar markets sobre shutdown
        shutdown_keywords = ['shutdown', 'government shutdown', 'govt shutdown', 'continuing resolution', 'CR']
        shutdown_markets = []

        for market in all_markets:
            question = market.get('question', '').lower()
            if any(keyword.lower() in question for keyword in shutdown_keywords):
                shutdown_markets.append(market)

        print(f"✅ Encontrados {len(shutdown_markets)} markets sobre shutdown\n")
        print("="*90)

        # 2. Análise detalhada de cada market
        print("\n📊 FASE 2: ANÁLISE DETALHADA DE CADA MARKET\n")
        print("="*90)

        market_data = []
        total_volume = 0
        total_liquidity = 0

        for i, market in enumerate(shutdown_markets, 1):
            question = market.get('question', 'N/A')
            volume_24h = float(market.get("volume24hr", 0) or 0)
            liquidity = float(market.get("liquidity", 0) or 0)

            total_volume += volume_24h
            total_liquidity += liquidity

            # Parse prices
            prices_raw = market.get('outcomePrices')
            if isinstance(prices_raw, str):
                prices = json.loads(prices_raw)
            else:
                prices = prices_raw

            yes_price = float(prices[0]) if prices and len(prices) > 0 else 0
            no_price = float(prices[1]) if prices and len(prices) > 1 else 0

            # Extract timing from question
            timing = extract_timing(question)

            market_info = {
                'rank': i,
                'question': question,
                'timing': timing,
                'volume_24h': volume_24h,
                'liquidity': liquidity,
                'yes_price': yes_price,
                'no_price': no_price,
                'yes_probability': yes_price * 100,
                'no_probability': no_price * 100,
                'market_id': market.get('id', ''),
                'category': market.get('category', 'N/A')
            }

            market_data.append(market_info)

            print(f"#{i} - {question}")
            print(f"   📅 Timing: {timing}")
            print(f"   💰 Volume 24h: ${volume_24h:,.0f}")
            print(f"   💧 Liquidez: ${liquidity:,.0f}")
            print(f"   📈 Probabilidades: YES {yes_price*100:.1f}% | NO {no_price*100:.1f}%")
            print()

        # 3. Análise de probabilidades agregadas
        print("\n" + "="*90)
        print("📊 FASE 3: ANÁLISE DE PROBABILIDADES & CONSENSO DO MERCADO")
        print("="*90 + "\n")

        print(f"💰 Volume Total 24h: ${total_volume:,.0f}")
        print(f"💧 Liquidez Total: ${total_liquidity:,.0f}")
        print(f"📊 Número de Markets: {len(shutdown_markets)}")
        print(f"📈 Volume Médio por Market: ${total_volume/len(shutdown_markets):,.0f}\n")

        # Organizar por timing
        by_timing = defaultdict(list)
        for m in market_data:
            by_timing[m['timing']].append(m)

        print("⏰ DISTRIBUIÇÃO POR PERÍODO DE RESOLUÇÃO:\n")

        for timing in sorted(by_timing.keys()):
            markets = by_timing[timing]
            avg_prob = sum(m['yes_probability'] for m in markets) / len(markets)
            total_vol = sum(m['volume_24h'] for m in markets)

            print(f"📅 {timing}:")
            print(f"   Markets: {len(markets)}")
            print(f"   Probabilidade média YES: {avg_prob:.1f}%")
            print(f"   Volume combinado: ${total_vol:,.0f}")
            print()

        # 4. Análise de correlação e arbitragem
        print("\n" + "="*90)
        print("🔄 FASE 4: ANÁLISE DE CORRELAÇÃO & OPORTUNIDADES DE ARBITRAGEM")
        print("="*90 + "\n")

        # Ordenar por timing para encontrar inconsistências
        sorted_markets = sorted(market_data, key=lambda x: x['timing'])

        print("📊 PROBABILIDADES POR ORDEM CRONOLÓGICA:\n")

        cumulative_prob = 0
        for m in sorted_markets:
            print(f"{m['timing']:20s} - YES: {m['yes_probability']:5.1f}% | "
                  f"NO: {m['no_probability']:5.1f}% | "
                  f"Vol: ${m['volume_24h']:>10,.0f}")
            cumulative_prob += m['yes_probability']

        # Detectar arbitragem
        print("\n⚠️  ANÁLISE DE CONSISTÊNCIA:\n")

        # A soma das probabilidades de eventos mutuamente exclusivos deve ser ~100%
        if cumulative_prob > 110:
            print(f"🔴 ALERTA: Probabilidade acumulada = {cumulative_prob:.1f}%")
            print(f"   Isso está ACIMA de 100%! Possível arbitragem:")
            print(f"   → Vender YES em todos os markets simultaneamente")
            print(f"   → Apenas UM pode ser verdadeiro, mas mercado precifica {cumulative_prob:.0f}%")
            print(f"   → Edge potencial: {cumulative_prob - 100:.1f}%\n")
        elif cumulative_prob < 90:
            print(f"🟢 OPORTUNIDADE: Probabilidade acumulada = {cumulative_prob:.1f}%")
            print(f"   Isso está ABAIXO de 100%! Possível arbitragem:")
            print(f"   → Comprar YES nos markets mais underpriced")
            print(f"   → Edge potencial: {100 - cumulative_prob:.1f}%\n")
        else:
            print(f"✅ Mercado razoavelmente eficiente: Probabilidade acumulada = {cumulative_prob:.1f}%\n")

        # 5. Análise de contexto político
        print("\n" + "="*90)
        print("🏛️  FASE 5: CONTEXTO POLÍTICO & ANÁLISE FUNDAMENTAL")
        print("="*90 + "\n")

        political_context = """
📰 CONTEXTO ATUAL DO SHUTDOWN:

🗳️  SITUAÇÃO POLÍTICA:
   • Congresso dividido (Republicanos na Câmara, Democratas no Senado)
   • Impasse sobre gastos governamentais
   • Necessidade de Continuing Resolution (CR) para evitar shutdown

📅 CRONOGRAMA CRÍTICO:
   • Funding expira em data específica (verificar últimas notícias)
   • Câmara e Senado precisam aprovar mesmo CR
   • Presidente precisa assinar

⚡ FATORES DE RISCO:
   • Demandas partidárias conflitantes
   • Questões de imigração/fronteira
   • Gastos militares vs sociais
   • Eleições futuras influenciando negociações

📊 HISTÓRICO DE SHUTDOWNS:
   • 2018-2019: 35 dias (mais longo da história)
   • 2013: 16 dias
   • Padrão: Maioria resolve em 1-3 dias
   • Shutdowns longos são raros mas possíveis
        """

        print(political_context)

        # 6. Análise de value & recomendações
        print("\n" + "="*90)
        print("💡 FASE 6: INSIGHTS ACIONÁVEIS & RECOMENDAÇÕES")
        print("="*90 + "\n")

        # Encontrar o market com melhor value
        underpriced = [m for m in market_data if m['yes_probability'] < 15 and m['volume_24h'] > 500000]
        overpriced = [m for m in market_data if m['yes_probability'] > 85 and m['volume_24h'] > 500000]

        if underpriced:
            print("🟢 OPORTUNIDADES DE COMPRA (YES underpriced):\n")
            underpriced.sort(key=lambda x: x['yes_probability'])

            for m in underpriced[:3]:
                implied_odds = 1 / m['yes_probability'] * 100 if m['yes_probability'] > 0 else 999
                print(f"• {m['question'][:70]}...")
                print(f"  YES: {m['yes_probability']:.1f}% (${m['yes_price']:.4f})")
                print(f"  Odds implícitas: {implied_odds:.1f}x retorno")
                print(f"  Volume: ${m['volume_24h']:,.0f}")
                print(f"  💡 Análise: Possível underpricing - mercado subestima probabilidade")
                print()

        if overpriced:
            print("\n🔴 OPORTUNIDADES DE VENDA (NO underpriced / YES overpriced):\n")
            overpriced.sort(key=lambda x: -x['yes_probability'])

            for m in overpriced[:3]:
                print(f"• {m['question'][:70]}...")
                print(f"  YES: {m['yes_probability']:.1f}% | NO: {m['no_probability']:.1f}%")
                print(f"  Volume: ${m['volume_24h']:,.0f}")
                print(f"  💡 Análise: NO pode estar underpriced - considerar vender YES")
                print()

        # 7. Análise de sentimento do mercado
        print("\n" + "="*90)
        print("📈 FASE 7: ANÁLISE DE SENTIMENTO & MOMENTUM")
        print("="*90 + "\n")

        # Calcular sentimento agregado
        weighted_sentiment = sum(m['yes_probability'] * m['volume_24h'] for m in market_data) / total_volume

        print(f"🎯 SENTIMENTO AGREGADO DO MERCADO (ponderado por volume):")
        print(f"   Probabilidade média de shutdown continuar: {weighted_sentiment:.1f}%")
        print()

        if weighted_sentiment < 10:
            print("✅ INTERPRETAÇÃO: Mercado MUITO CONFIANTE que shutdown resolverá rapidamente")
            print("   → Consenso forte de resolução iminente")
            print("   → Possível complacência? Considerar hedge com YES barato\n")
        elif weighted_sentiment < 30:
            print("🟡 INTERPRETAÇÃO: Mercado MODERADAMENTE CONFIANTE em resolução rápida")
            print("   → Ainda há incerteza considerável")
            print("   → Boas oportunidades de trading em ambos os lados\n")
        else:
            print("🔴 INTERPRETAÇÃO: Mercado PESSIMISTA sobre resolução rápida")
            print("   → Expectativa de impasse prolongado")
            print("   → Considerar posições mais longas\n")

        # 8. Estratégia recomendada
        print("\n" + "="*90)
        print("🎯 FASE 8: ESTRATÉGIA DE TRADING RECOMENDADA")
        print("="*90 + "\n")

        print("💼 ESTRATÉGIA MULTI-LEG:\n")

        # Encontrar o melhor market de cada categoria
        early_markets = [m for m in market_data if 'november 8' in m['timing'].lower() or 'november 11' in m['timing'].lower()]
        mid_markets = [m for m in market_data if 'november 12' in m['timing'].lower() or 'november 15' in m['timing'].lower()]
        late_markets = [m for m in market_data if 'november 16' in m['timing'].lower() or 'later' in m['timing'].lower()]

        print("📊 PORTFOLIO SUGERIDO ($1,000):\n")

        total_allocation = 0

        if early_markets:
            best_early = max(early_markets, key=lambda x: x['volume_24h'])
            allocation = 200
            total_allocation += allocation

            print(f"1️⃣  POSIÇÃO CONSERVADORA (${allocation}):")
            print(f"   Market: {best_early['question'][:65]}...")
            print(f"   Lado: NO @ ${best_early['no_price']:.4f}")
            print(f"   Lógica: Alta probabilidade de resolução rápida")
            print(f"   Retorno esperado: 3-5% em 1-3 dias")
            print()

        if mid_markets:
            best_mid = max(mid_markets, key=lambda x: x['volume_24h'])
            allocation = 300
            total_allocation += allocation

            print(f"2️⃣  POSIÇÃO EQUILIBRADA (${allocation}):")
            print(f"   Market: {best_mid['question'][:65]}...")

            if best_mid['yes_probability'] < 30:
                print(f"   Lado: YES @ ${best_mid['yes_price']:.4f}")
                print(f"   Lógica: Underpriced - melhor risk/reward")
            else:
                print(f"   Lado: NO @ ${best_mid['no_price']:.4f}")
                print(f"   Lógica: Seguir consenso do mercado")

            print(f"   Retorno esperado: 10-20% em 3-7 dias")
            print()

        if late_markets:
            best_late = max(late_markets, key=lambda x: x['volume_24h'])
            allocation = 250
            total_allocation += allocation

            print(f"3️⃣  POSIÇÃO ESPECULATIVA (${allocation}):")
            print(f"   Market: {best_late['question'][:65]}...")
            print(f"   Lado: YES @ ${best_late['yes_price']:.4f}")
            print(f"   Lógica: Lottery ticket - baixa probabilidade, alto retorno")
            print(f"   Retorno esperado: 1000%+ se vencer (ou -100%)")
            print()

        cash_reserve = 1000 - total_allocation
        if cash_reserve > 0:
            print(f"4️⃣  CASH RESERVE (${cash_reserve}):")
            print(f"   Manter em USDC para oportunidades emergentes")
            print(f"   Usar se surgirem notícias que mudem probabilidades\n")

        # 9. Catalisadores e monitoramento
        print("\n" + "="*90)
        print("📡 FASE 9: CATALISADORES & MONITORAMENTO")
        print("="*90 + "\n")

        print("🔔 EVENTOS A MONITORAR:\n")
        print("✅ POSITIVOS (Resolução rápida):")
        print("   • Acordo bipartidário anunciado")
        print("   • Lideranças de ambos partidos concordando")
        print("   • Votação de CR agendada")
        print("   • Pressão pública/mídia aumentando")
        print()

        print("❌ NEGATIVOS (Shutdown prolongado):")
        print("   • Impasse em negociações")
        print("   • Demandas extremas de qualquer lado")
        print("   • Falha em votação")
        print("   • Rhetoric político intensificando")
        print()

        print("📱 FONTES PARA MONITORAR:")
        print("   • Twitter de lideranças do Congresso")
        print("   • C-SPAN (votações ao vivo)")
        print("   • Politico, The Hill (notícias)")
        print("   • Polymarket (mudanças de preço em tempo real)")
        print()

        # 10. Resumo executivo
        print("\n" + "="*90)
        print("📋 RESUMO EXECUTIVO - KEY TAKEAWAYS")
        print("="*90 + "\n")

        print("🎯 TOP 3 INSIGHTS:\n")

        print("1️⃣  CONSENSO DO MERCADO:")
        print(f"   Mercado precifica {weighted_sentiment:.1f}% de chance de shutdown prolongado")
        print(f"   Isto significa {100-weighted_sentiment:.1f}% de confiança em resolução rápida")
        print()

        print("2️⃣  OPORTUNIDADE DE VALOR:")
        if underpriced:
            best_value = underpriced[0]
            roi = (1 / best_value['yes_probability'] * 100) - 100 if best_value['yes_probability'] > 0 else 999
            print(f"   Melhor trade: {best_value['question'][:60]}...")
            print(f"   YES @ {best_value['yes_probability']:.1f}% = {roi:.0f}% ROI potencial")
        print()

        print("3️⃣  RISCO/RECOMPENSA:")
        print(f"   Volume total: ${total_volume:,.0f}/dia indica alta convicção")
        print(f"   Liquidez: ${total_liquidity:,.0f} permite entrada/saída fácil")
        print(f"   Timing: Resolução em 1-14 dias = retorno rápido do capital")
        print()

        print("💡 RECOMENDAÇÃO FINAL:")
        print("   → Estratégia multi-leg com diversificação temporal")
        print("   → 20% conservador (alta probabilidade)")
        print("   → 30% equilibrado (médio risco/retorno)")
        print("   → 25% especulativo (lottery ticket)")
        print("   → 25% cash para oportunidades")
        print()
        print("   ⚠️  IMPORTANTE: Monitorar notícias diariamente!")
        print("   ⚡ Use WebSocket do MCP para alertas em tempo real!")

def extract_timing(question):
    """Extract timing info from question"""
    q = question.lower()

    if 'november 8' in q or 'nov 8' in q or 'nov. 8' in q:
        return "Nov 8-11"
    elif 'november 11' in q or 'nov 11' in q:
        return "Nov 8-11"
    elif 'november 12' in q or 'nov 12' in q:
        return "Nov 12-15"
    elif 'november 15' in q or 'nov 15' in q:
        return "Nov 12-15"
    elif 'november 16' in q or 'nov 16' in q or 'later' in q:
        return "Nov 16+"
    elif 'before' in q:
        return "Before specified"
    else:
        return "General/Unspecified"

if __name__ == "__main__":
    asyncio.run(deep_shutdown_analysis())
