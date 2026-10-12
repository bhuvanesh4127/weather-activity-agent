"""Beginner-friendly rules, CSP backtracking, AC-3-style propagation and reasoning traces."""

ACTIVITIES = [
    "Cycling", "Sports practice", "Picnic", "Laundry drying",
    "Outdoor study", "Indoor study", "Indoor games", "Rest"
]
OUTDOOR = {"Cycling", "Sports practice", "Picnic", "Outdoor study"}
RAIN_SENSITIVE = {"Cycling", "Picnic", "Laundry drying", "Outdoor study", "Sports practice"}
EXERCISE = {"Cycling", "Sports practice"}

def assess(row, activity):
    """Return status, suitability score, warnings and a plain-language explanation."""
    temp = float(row["Temperature °C"])
    rain = float(row["Rain chance %"])
    aqi = float(row["AQI"])
    wind = float(row["Wind km/h"])
    warnings = []
    reasons = []
    score = 80

    if not row["Available"]:
        return "Not recommended", 0, ["User is unavailable"], "The user marked this day as unavailable."

    if activity in OUTDOOR:
        if rain >= 60:
            warnings.append("High rain chance")
            score -= 40
            reasons.append("rain chance is high")
        elif rain >= 35:
            score -= 15
            reasons.append("some rain is possible")
        if temp >= 36:
            warnings.append("High temperature")
            score -= 35
            reasons.append("temperature is very high")
        elif temp >= 33:
            score -= 15
            reasons.append("temperature is hot")
        elif temp < 10:
            score -= 15
            reasons.append("temperature is cold")
        if aqi >= 151:
            warnings.append("Poor air quality: avoid outdoor exercise")
            score -= 45
            reasons.append("AQI is very high")
        elif aqi >= 101:
            warnings.append("Unhealthy air quality for sensitive groups")
            score -= 25
            reasons.append("AQI is elevated")
        elif aqi >= 51:
            score -= 5
            reasons.append("AQI is moderate")
        if wind >= 35:
            warnings.append("Strong wind")
            score -= 20
            reasons.append("wind is strong")
    else:
        reasons.append("this is an indoor or flexible activity")

    if activity == "Laundry drying":
        if rain >= 35:
            score -= 30
            reasons.append("rain may prevent clothes from drying")
        if temp >= 20 and rain < 35:
            score += 10
            reasons.append("warm, low-rain conditions support drying")

    if activity == "Picnic":
        score += 5

    score = max(0, min(100, int(score)))
    status = "Not recommended" if warnings and score < 50 else "Suitable"
    if not reasons:
        reasons.append("entered conditions are generally suitable under the demo rules")
    explanation = "Recommendation based on " + ", ".join(reasons) + "."
    return status, score, warnings, explanation

def utility(row, activity, preferred):
    """A simple utility score; safety filtering is performed before utility ranking."""
    status, score, warnings, _ = assess(row, activity)
    preference_bonus = 10 if activity == preferred else 0
    # A warning that triggers a hard restriction cannot be overridden by preference.
    hard_restricted = (
        not row["Available"] or
        (activity in OUTDOOR and float(row["AQI"]) >= 151) or
        (activity in OUTDOOR and float(row["Temperature °C"]) >= 40) or
        (activity in OUTDOOR and float(row["Rain chance %"]) >= 85)
    )
    if hard_restricted:
        return -1
    return min(100, score + preference_bonus)

def initial_domains(rows):
    domains = {}
    for row in rows:
        valid = []
        for activity in ACTIVITIES:
            status, score, warnings, _ = assess(row, activity)
            if utility(row, activity, "") >= 0 and (status == "Suitable" or activity not in OUTDOOR):
                valid.append(activity)
        # Keep at least one fallback domain value, even if the input conditions are severe.
        if not valid:
            valid = ["Indoor study", "Rest"]
        domains[row["Day"]] = valid
    return domains

def ac3_filter(domains, days):
    """Small AC-3-style propagation: adjacent days should not repeat the same activity if avoidable."""
    domains = {day: list(values) for day, values in domains.items()}
    queue = [(days[i], days[i + 1]) for i in range(len(days) - 1)]
    removed = 0
    while queue:
        left, right = queue.pop(0)
        removed_now = revise(domains, left, right)
        removed += removed_now
        if removed_now:
            if not domains[left]:
                return domains, removed
            for prior in days:
                if prior != left and prior != right and abs(days.index(prior) - days.index(left)) == 1:
                    queue.append((prior, left))
    return domains, removed

def revise(domains, left, right):
    """Return how many left-domain values were removed by the adjacency constraint."""
    removed = 0
    for value in list(domains[left]):
        if not any(other != value for other in domains[right]):
            if len(domains[left]) > 1:
                domains[left].remove(value)
                removed += 1
    return removed

def plan_week(rows, preferred):
    days = [r["Day"] for r in rows]
    row_by_day = {r["Day"]: r for r in rows}
    domains = initial_domains(rows)
    domains, removed = ac3_filter(domains, days)
    assignments = {}
    stats = {"nodes": 0, "backtracks": 0}

    def backtrack(index):
        if index == len(days):
            return True
        day = days[index]
        options = sorted(
            domains[day],
            key=lambda a: utility(row_by_day[day], a, preferred),
            reverse=True
        )
        for activity in options:
            stats["nodes"] += 1
            if index > 0 and assignments.get(days[index - 1]) == activity and len(options) > 1:
                continue
            assignments[day] = activity
            if backtrack(index + 1):
                return True
            assignments.pop(day, None)
            stats["backtracks"] += 1
        return False

    success = backtrack(0)
    if not success:
        # Safe simple fallback: select the highest-utility feasible activity per day.
        assignments = {}
        for day in days:
            assignments[day] = max(domains[day], key=lambda a: utility(row_by_day[day], a, preferred))

    plan = []
    for day in days:
        row = row_by_day[day]
        activity = assignments[day]
        status, score, warnings, explanation = assess(row, activity)
        u = utility(row, activity, preferred)
        if u < 0:
            u = 0
        plan.append({
            "Day": day,
            "Activity": activity,
            "Expected utility": int(u),
            "Suitability": score,
            "Warnings": warnings,
            "Explanation": explanation
        })
    return {"plan": plan, "nodes": stats["nodes"], "backtracks": stats["backtracks"], "ac3_removed": removed}

def forward_chain(row):
    """Apply simple rules to known facts and return conclusions with a trace."""
    facts = []
    conclusions = []
    temp = float(row["Temperature °C"])
    rain = float(row["Rain chance %"])
    aqi = float(row["AQI"])
    if not row["Available"]:
        facts.append("User is unavailable.")
        conclusions.append("Do not schedule an activity for this day.")
    else:
        facts.append("User is available.")
    if rain >= 60:
        facts.append(f"Rain chance is high ({rain:.0f}%).")
        conclusions.append("Prefer indoor activities because of rain risk.")
    if temp >= 36:
        facts.append(f"Temperature is very high ({temp:.0f}°C).")
        conclusions.append("Avoid strenuous outdoor activity and consider a cooler option.")
    if aqi >= 151:
        facts.append(f"AQI is very high ({aqi:.0f}).")
        conclusions.append("Avoid outdoor exercise and follow local air-quality guidance.")
    if not conclusions:
        conclusions.append("No configured warning rule fired; this is not a guarantee of safety.")
    return {"facts": facts, "conclusions": conclusions}

def answer_question(row, activity):
    """Backward chaining: start from the goal and check each prerequisite."""
    trace = [f"Goal: determine whether {activity} is suitable on {row['Day']}."]
    if not row["Available"]:
        trace.append("Rule: if user is unavailable, no activity can be scheduled.")
        return {"status": "Not recommended", "answer": f"{activity} is not recommended because you are unavailable.", "trace": trace}
    trace.append("Check 1: user availability passed.")
    status, score, warnings, explanation = assess(row, activity)
    trace.append(f"Check 2: weather and environmental rules returned suitability {score}/100.")
    if warnings:
        trace.append("Warnings found: " + "; ".join(warnings) + ".")
    else:
        trace.append("No warning was triggered by the simplified rules.")
    trace.append("Conclusion: " + status + ".")
    return {"status": status, "answer": f"{activity}: {status.lower()}. {explanation}", "trace": trace}
