# Weather-Based Activity Agent

## Innovative Assignment 1 – Micro Level Project

**Course:** Foundations of Artificial Intelligence  
**Project Type:** Rational Agent  
**Project:** Weather-Based Activity Agent

---

## 1. Problem Formulation

The Weather-Based Activity Agent is a rule-based rational agent that recommends a suitable activity based on the current weather conditions.

The user provides three environmental inputs:

1. Temperature in degrees Celsius
2. Weather condition
3. Wind level

The agent observes these inputs, applies predefined decision rules, and recommends either an indoor or outdoor activity.

### Agent Components

**Percepts:**  
Temperature, weather condition, and wind level entered by the user.

**Actions:**  
Recommend an indoor or outdoor activity.

**Goal:**  
Select a safe and suitable activity according to the given weather conditions.

**Decision Rules:**  
- Rainy, stormy, or thunderstorm weather → Indoor activity
- Temperature of 35°C or above → Indoor activity
- High wind → Indoor activity
- Sunny or clear weather with suitable temperature → Outdoor activity
- Cloudy or partly cloudy weather → Outdoor activity
- Unknown weather → Safe indoor activity

The agent follows the basic rational-agent cycle:

**Perceive → Decide → Act**

---

## 2. Approach

The project uses a rule-based decision-making approach.

The `recommend_activity()` function receives temperature, weather condition, and wind level. It processes the inputs through a sequence of conditional rules.

The agent first checks unsafe conditions such as rain, storms, very high temperature, and high wind. If these conditions are detected, an indoor activity is recommended.

If the weather is suitable for outdoor activities, the agent recommends activities such as walking, cycling, or outdoor games.

The program also validates user input. Missing weather information, invalid temperature values, and invalid wind levels are handled with appropriate messages instead of allowing the program to crash.

### Perceive → Decide → Act

**Perceive:**  
The agent receives temperature, weather condition, and wind level from the user.

**Decide:**  
The decision rules are evaluated in order.

**Act:**  
The agent displays the recommended activity.

This makes the system a simple rational agent because its action is selected according to the current environmental information and its safety objective.

---

## 3. Algorithm

### Step 1
Start the program.

### Step 2
Read the temperature from the user.

### Step 3
Validate the temperature.

### Step 4
Read the weather condition.

### Step 5
Check whether the weather condition is missing.

### Step 6
Read the wind level.

### Step 7
Validate the wind level.

### Step 8
Apply the weather decision rules.

### Step 9
Display the recommended activity.

### Step 10
End the program.

---

## 4. Complexity Analysis

The agent uses a fixed number of decision rules.

Let the number of decision rules be `k`.

Since the current implementation contains a fixed set of rules, the value of `k` does not grow with the input size.

### Time Complexity

The decision-making process checks the rules sequentially.

Therefore:

**Time Complexity: O(k)**

Since `k` is fixed:

**Practical Time Complexity: O(1)**

### Space Complexity

The program stores only a few input values and temporary variables.

Therefore:

**Space Complexity: O(1)**

The automated test suite also uses a fixed number of test cases.

---

## 5. Results and Testing

The agent was tested using normal conditions, extreme conditions, unknown weather, and invalid inputs.

### Test Cases

| Test Case | Temperature | Weather | Wind | Expected Decision |
|---|---:|---|---|---|
| 1 | 28°C | Sunny | Low | Outdoor |
| 2 | 25°C | Rainy | Moderate | Indoor |
| 3 | 35°C | Sunny | Low | Indoor |
| 4 | 20°C | Cloudy | High | Indoor |
| 5 | 22°C | Foggy | Low | Safe indoor activity |
| 6 | abc | — | — | Invalid temperature message |
| 7 | 28°C | Empty | — | Missing weather message |
| 8 | 28°C | Sunny | Very high | Invalid wind message |

### Automated Testing

Five automated test cases were created using Python's `unittest` framework.

The tests cover:

- Sunny weather
- Rainy weather
- High temperature
- High wind
- Unknown weather

The automated test suite completed successfully with:

**Ran 5 tests — OK**

### Results

The manual tests confirmed that the agent responds differently according to the supplied environmental conditions.

Normal weather conditions can result in outdoor recommendations, while unsafe conditions result in indoor recommendations. Invalid and missing inputs are handled with clear error messages.

---

## 6. Evidence / Screenshots

The following screenshots should be included in the final PDF:

### Screenshot 1 – Normal Outdoor Recommendation

Show the program with:

- Temperature: 28°C
- Weather: sunny
- Wind: low

**Result:** Outdoor activity recommendation.

### Screenshot 2 – Rainy Weather

Show the program with:

- Temperature: 25°C
- Weather: rainy
- Wind: moderate

**Result:** Indoor activity recommendation.

### Screenshot 3 – Automated Tests

Show the terminal output displaying:

**Ran 5 tests**  
**OK**

### Screenshot 4 – Invalid Input Handling

Show an example such as an invalid temperature or invalid wind level being handled without crashing.

---

## 7. Limitations

The current version has some limitations:

- Weather information is entered manually by the user.
- The system does not currently obtain live weather information from an API.
- Recommendations are based on predefined rules.
- The number of activity recommendations is limited.

---

## 8. Future Improvements

The project can be improved by:

1. Connecting the agent to a live weather API.
2. Adding humidity information.
3. Adding precipitation probability.
4. Adding more weather conditions.
5. Providing more personalised activity recommendations.
6. Developing a graphical user interface.
7. Adding location-based weather information.

---

## 9. Reflection

The main challenge was designing decision rules that produce sensible recommendations for different weather conditions.

Another important part was handling invalid and missing user input so that the program does not crash.

The project helped demonstrate how a rational agent can observe its environment, evaluate conditions, and select an action based on a defined objective.

In the future, the project could be improved by using real-time weather data and more detailed decision rules.

### Honesty Note

AI assistance and online/reference material were used during development. The project code and design should be understood by the team members and explained during the viva.

---

## 10. Conclusion

The Weather-Based Activity Agent demonstrates a simple rational agent using rule-based decision making.

The agent receives weather-related information from the user, evaluates the conditions, and recommends an appropriate indoor or outdoor activity.

The project demonstrates the important AI concept of an agent interacting with its environment through the cycle:

**Perceive → Decide → Act**

The successful manual and automated tests show that the implemented rules work for normal, extreme, unknown, and invalid input conditions.