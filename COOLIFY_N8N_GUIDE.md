# 🚀 Guide de Déploiement Coolify + n8n 2.0

> **Mise à jour : Janvier 2026**  
> Compatible avec n8n 2.0+, MCPO 0.0.18+, MCP Protocol 2025-11-25

---

## 📋 Prérequis

- ✅ **Coolify** installé et fonctionnel
- ✅ **n8n 2.0+** déjà déployé sur Coolify (ou à déployer)
- ✅ Un compte Polymarket (optionnel pour le mode DEMO)

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                          COOLIFY                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────┐         ┌────────────────────────────────┐ │
│  │     n8n 2.0+    │◀───────▶│   Polymarket MCP + MCPO        │ │
│  │                 │         │                                │ │
│  │  MCP Client     │ Stream- │   ┌────────────────────────┐   │ │
│  │  Tool (native)  │ able    │   │  MCPO 0.0.18+          │   │ │
│  │                 │ HTTP    │   │  (Streamable HTTP)     │   │ │
│  │  Instance-Level │         │   └───────────┬────────────┘   │ │
│  │  MCP Access     │         │               │                │ │
│  │                 │         │   ┌───────────▼────────────┐   │ │
│  │  port: 5678     │         │   │  polymarket_mcp.server │   │ │
│  └─────────────────┘         │   └────────────────────────┘   │ │
│                              │                                │ │
│                              │   port: 8000                   │ │
│                              └────────────────────────────────┘ │
│                                                                 │
│  Network: coolify (internal)                                    │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📦 Étape 1 : Créer le projet sur Coolify

### 1.1 Créer un nouveau projet

1. Connectez-vous à votre dashboard Coolify
2. Cliquez sur **"New Project"**
3. Nommez-le : `polymarket-mcp`

### 1.2 Ajouter un service Docker Compose

1. Dans le projet, cliquez sur **"+ Add Resource"**
2. Sélectionnez **"Docker Compose"**
3. Source : **Git Repository**
4. URL : `https://github.com/caiovicentino/polymarket-mcp-server.git`
   - Ou votre propre fork

### 1.3 Configuration du déploiement

Dans les paramètres du déploiement :

- **Docker Compose File** : `docker-compose.coolify.yml`
- **Dockerfile** : `Dockerfile.coolify`

---

## ⚙️ Étape 2 : Configurer les variables d'environnement

Dans Coolify, allez dans **Environment Variables** et ajoutez :

### Variables de base (Mode DEMO)

```env
# Mode DEMO - lecture seule, pas de trading
DEMO_MODE=true

# Logs
LOG_LEVEL=INFO
```

### Variables pour le trading réel (optionnel)

```env
# Désactiver le mode DEMO pour trader
DEMO_MODE=false

# Wallet Polygon (OBLIGATOIRE pour trader)
POLYGON_PRIVATE_KEY=votre_cle_privee_sans_0x
POLYGON_ADDRESS=0xVotreAdressePolygon

# Limites de sécurité (ajustez selon votre tolérance au risque)
MAX_ORDER_SIZE_USD=100
MAX_TOTAL_EXPOSURE_USD=1000
MAX_POSITION_SIZE_PER_MARKET=500
REQUIRE_CONFIRMATION_ABOVE_USD=50

# Optionnel : Credentials API Polymarket (pour limites de rate plus élevées)
POLYMARKET_API_KEY=
POLYMARKET_PASSPHRASE=
```

---

## 🚀 Étape 3 : Déployer

1. Cliquez sur **"Deploy"**
2. Attendez que le build se termine (~2-5 minutes)
3. Vérifiez les logs pour confirmer le démarrage

### Vérification du déploiement

Une fois déployé, le serveur MCP sera accessible sur le réseau interne Coolify :

```
http://polymarket-mcp:8000
```

Ou via l'URL externe si vous l'avez configurée.

---

## 🔗 Étape 4 : Connecter n8n 2.0+

### Méthode 1 : Instance-Level MCP Access (Recommandée) ✅

> **Nouveauté n8n 2.0 (Décembre 2025)** : Connectez votre instance n8n une seule fois !

1. Dans n8n, allez dans **Settings** → **MCP**
2. Cliquez sur **"Add MCP Server"**
3. Configurez :
   - **Name** : `Polymarket`
   - **URL** : `http://polymarket-mcp:8000` (réseau interne Coolify)
   - **Transport** : `Streamable HTTP`
   - **Authentication** : `None` (ou OAuth 2.0 si configuré)
4. Cliquez sur **"Test Connection"**
5. Sauvegardez

### Méthode 2 : MCP Client Tool (par workflow)

Dans un workflow n8n :

1. Ajoutez un node **"MCP Client Tool"**
2. Configurez :
   - **Server URL** : `http://polymarket-mcp:8000`
   - **Tool** : Sélectionnez parmi les 45 outils disponibles
   - **Arguments** : Selon l'outil choisi

---

## 🛠️ Étape 5 : Créer vos premiers workflows

### Exemple 1 : Alerte sur marchés tendance

```
┌─────────────┐     ┌────────────────┐     ┌───────────────┐
│  Schedule   │────▶│  MCP Client    │────▶│  Telegram/    │
│  Trigger    │     │  get_trending  │     │  Discord      │
│  (chaque h) │     │  _markets      │     │  Alert        │
└─────────────┘     └────────────────┘     └───────────────┘
```

**Nodes :**
1. **Schedule Trigger** : Toutes les heures
2. **MCP Client Tool** : 
   - Tool: `get_trending_markets`
   - Arguments: `{"timeframe": "24h", "limit": 5}`
3. **Telegram** : Envoie les résultats

### Exemple 2 : Analyse automatique d'opportunités

```
┌─────────────┐     ┌────────────────┐     ┌────────────────┐     ┌──────────┐
│  Schedule   │────▶│  MCP Client    │────▶│  MCP Client    │────▶│  Filter  │
│  Trigger    │     │  get_markets   │     │  analyze_      │     │  Score   │
│             │     │                │     │  opportunity   │     │  > 80    │
└─────────────┘     └────────────────┘     └────────────────┘     └────┬─────┘
                                                                       │
                                                            ┌──────────▼───────┐
                                                            │  Telegram Alert  │
                                                            │  "Opportunité!"  │
                                                            └──────────────────┘
```

### Exemple 3 : Trading automatique (Mode complet uniquement)

```
┌─────────────┐     ┌────────────────┐     ┌────────────────┐
│  Webhook    │────▶│  MCP Client    │────▶│  MCP Client    │
│  /signal    │     │  analyze_      │     │  place_order   │
│             │     │  opportunity   │     │  (si score>85) │
└─────────────┘     └────────────────┘     └────────────────┘
```

---

## 📊 Outils MCP Disponibles

### 🔍 Market Discovery (8 outils)
- `search_markets` - Rechercher des marchés
- `get_trending_markets` - Marchés tendance
- `get_markets_by_category` - Par catégorie
- `get_markets_closing_soon` - Fermeture proche
- `get_featured_markets` - Marchés mis en avant
- `get_sports_markets` - Marchés sportifs
- `get_crypto_markets` - Marchés crypto
- `get_market_events` - Événements

### 📈 Market Analysis (10 outils)
- `get_market_prices` - Prix en temps réel
- `get_orderbook` - Carnet d'ordres
- `get_market_liquidity` - Liquidité
- `get_historical_prices` - Historique
- `analyze_opportunity` - **Analyse IA** avec recommandation
- `compare_markets` - Comparaison
- `get_top_holders` - Top holders
- `assess_risk` - Évaluation du risque
- `get_spread` - Spread bid/ask
- `get_volume_metrics` - Métriques de volume

### 💼 Trading (12 outils) - Mode complet uniquement
- `place_limit_order` - Ordre limite
- `place_market_order` - Ordre market
- `place_batch_orders` - Ordres en lot
- `get_suggested_price` - Prix suggéré IA
- `get_order_status` - Statut d'un ordre
- `get_order_history` - Historique
- `get_open_orders` - Ordres ouverts
- `cancel_order` - Annuler un ordre
- `cancel_all_orders` - Annuler tout
- `smart_trade` - Trade intelligent
- `rebalance_position` - Rééquilibrer
- `execute_strategy` - Exécuter stratégie

### 📊 Portfolio (8 outils)
- `get_positions` - Positions actuelles
- `get_portfolio_value` - Valeur totale
- `get_pnl` - Profit/Perte
- `analyze_portfolio_risk` - Risque portfolio
- `get_trade_history` - Historique trades
- `get_activity_log` - Journal d'activité
- `get_performance_metrics` - Métriques
- `optimize_portfolio` - Optimisation IA

### ⚡ Real-time (7 outils)
- `subscribe_price` - Abonnement prix
- `subscribe_orderbook` - Abonnement orderbook
- `subscribe_order_status` - Statut ordres
- `subscribe_trades` - Trades
- `unsubscribe` - Désabonnement
- `get_subscriptions` - Liste abonnements
- `get_health_status` - Santé système

---

## 🔧 Dépannage

### Le serveur ne démarre pas

```bash
# Vérifier les logs dans Coolify
# Ou en SSH :
docker logs polymarket-mcp
```

### Erreur de connexion depuis n8n

1. Vérifiez que les deux services sont sur le même réseau Coolify
2. Testez la connexion :
   ```bash
   curl http://polymarket-mcp:8000/health
   ```

### Mode DEMO ne fonctionne pas

Vérifiez que `DEMO_MODE=true` est bien configuré dans les variables d'environnement.

---

## 📚 Ressources

- [Documentation Polymarket MCP](./README.md)
- [n8n MCP Documentation](https://docs.n8n.io/integrations/builtin/cluster-nodes/sub-nodes/n8n-nodes-langchain.toolmcp/)
- [MCPO GitHub](https://github.com/open-webui/mcpo)
- [MCP Protocol Spec](https://modelcontextprotocol.io)

---

## ⚠️ Avertissement

Le trading sur les marchés de prédiction comporte des risques financiers. 
- Commencez en mode DEMO
- N'investissez que ce que vous pouvez perdre
- Testez vos stratégies avant de les automatiser

---

*Mis à jour : 5 janvier 2026*
