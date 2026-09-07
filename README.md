# Weather-Based Activity Agent

## 1. Problem Statement

The Weather-Based Activity Agent is a rational agent that takes current weather conditions as input and recommends a suitable activity.

The agent considers:
- Temperature
- Weather condition
- Wind level

Based on these inputs, it uses decision rules to recommend either an indoor or outdoor activity.

## 2. Objective

The objective of the agent is to select a safe and suitable activity according to the given weather conditions.

## 3. Approach

The project uses a rule-based rational agent.

The agent follows the process:

**Perceive → Decide → Act**

- **Perceive:** Takes temperature, weather condition and wind level from the user.
- **Decide:** Applies predefined decision rules.
- **Act:** Recommends a suitable indoor or outdoor activity.

### Decision Rules

| Condition | Recommendation |
|---|---|
| Rainy / Stormy | Indoor activity |
| Temperature ≥ 35°C | Indoor activity |
| High wind | Indoor activity |
| Sunny / Clear with suitable temperature | Outdoor activity |
| Cloudy / Partly cloudy | Outdoor activity |
| Unknown weather | Safe indoor activity |

## 4. Project Structure

```text
weather-activity-agent/
├── src/
│   └── weather_agent.py
├── tests/
│   └── test_weather_agent.py
├── docs/
├── README.md
├── requirements.txt
├── .gitignore
└── LICENSE