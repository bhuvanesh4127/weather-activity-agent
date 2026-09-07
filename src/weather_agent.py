def recommend_activity(temperature, weather, wind):
    """Recommend an activity based on weather conditions."""

    weather = weather.strip().lower()
    wind = wind.strip().lower()

    # Decision rules
    if weather in ["rainy", "rain", "stormy", "thunderstorm"]:
        return "Indoor activity recommended: Watch a movie, read a book, or play indoor games."

    elif temperature >= 35:
        return "Indoor activity recommended: Stay cool indoors and watch a movie or play games."

    elif wind == "high":
        return "Indoor activity recommended: Avoid outdoor activities because of strong wind."

    elif weather in ["sunny", "clear"] and temperature < 35 and wind in ["low", "moderate"]:
        return "Outdoor activity recommended: Go for a walk, cycling, or play outdoor games."

    elif weather in ["cloudy", "partly cloudy"]:
        return "Outdoor activity recommended: Take a walk or visit a nearby park."

    else:
        return "Indoor activity recommended: Choose a safe indoor activity."


def main():
    print("====================================")
    print("     WEATHER-BASED ACTIVITY AGENT")
    print("====================================")

    temperature = float(input("Enter temperature (°C): "))
    weather = input("Enter weather condition: ")
    wind = input("Enter wind level (low/moderate/high): ")

    print("\nAgent Decision:")
    print(recommend_activity(temperature, weather, wind))


if __name__ == "__main__":
    main()