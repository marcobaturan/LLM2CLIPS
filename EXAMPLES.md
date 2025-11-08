# 📚 LLM2CLIPS - Example Problems

This document contains ready-to-use example problems you can copy and paste into LLM2CLIPS.

---

## 🎯 Classification Examples

### Example 1: Age Classification

```
Problem: Classify people by age group
Data: Person named John is 25 years old
Rules: 
- Child: age < 13
- Teenager: age 13-17
- Adult: age 18-64
- Senior: age >= 65
```

---

### Example 2: Temperature Classification

```
Problem: Classify temperature readings
Data: Current temperature is 35 degrees Celsius
Rules:
- Hot: temperature > 30
- Warm: temperature 20-30
- Cool: temperature 10-19
- Cold: temperature < 10
```

---

### Example 3: Grade Classification

```
Problem: Assign letter grades to students
Data: Student Alice scored 87 points
Rules:
- A: 90-100 points
- B: 80-89 points
- C: 70-79 points
- D: 60-69 points
- F: below 60 points
```

---

## 🏦 Decision-Making Examples

### Example 4: Loan Approval

```
Problem: Decide if a loan application should be approved
Data: Applicant has income of $4500, credit score of 720, and debt ratio of 25%
Rules:
- Approve if: income > $3000 AND credit score > 680 AND debt ratio < 40%
- Review if: income > $2500 AND credit score > 650 AND debt ratio < 50%
- Reject otherwise
```

---

### Example 5: College Admission

```
Problem: Determine college admission status
Data: Student has GPA of 3.6, SAT score of 1350, and 2 extracurricular activities
Rules:
- Admit if: GPA > 3.5 AND SAT > 1300
- Waitlist if: GPA > 3.0 AND SAT > 1200
- Reject otherwise
```

---

### Example 6: Job Candidate Screening

```
Problem: Screen job candidates for interview
Data: Candidate has 5 years experience, Bachelor's degree, knows Python and JavaScript
Rules:
- Strong candidate: experience >= 5 years AND degree AND 2+ skills
- Moderate candidate: experience >= 3 years AND (degree OR 3+ skills)
- Weak candidate: others
```

---

## 🏥 Diagnostic Examples

### Example 7: Medical Triage

```
Problem: Classify patient urgency level
Data: Patient has high fever (40°C), chest pain, and difficulty breathing
Rules:
- Critical: chest pain OR difficulty breathing OR fever > 39.5
- Urgent: fever > 38.5 AND (cough OR headache)
- Normal: other symptoms
```

---

### Example 8: Computer Troubleshooting

```
Problem: Diagnose computer issues
Data: Computer won't start, power light is off, fan is not spinning
Rules:
- Power supply issue: power light off AND fan not spinning
- Hardware failure: power light on BUT no display AND beeping sound
- Software issue: boots but crashes during startup
```

---

### Example 9: Plant Health Diagnosis

```
Problem: Diagnose plant health problems
Data: Plant has yellow leaves, drooping stems, and dry soil
Rules:
- Underwatered: dry soil AND drooping stems
- Overwatered: wet soil AND yellow leaves
- Nutrient deficiency: yellow leaves BUT soil moisture normal
```

---

## 🎓 Educational Examples

### Example 10: Student Performance Assessment

```
Problem: Assess student academic performance
Data: Student has grade average of 75%, attendance of 85%, and completed 90% of assignments
Rules:
- Excellent: grade > 90% AND attendance > 90% AND assignments > 95%
- Good: grade > 80% AND attendance > 85% AND assignments > 90%
- Satisfactory: grade > 70% AND attendance > 80%
- Needs improvement: others
```

---

### Example 11: Course Recommendation

```
Problem: Recommend next course for student
Data: Student completed Intro to Programming with grade A, enjoys problem-solving
Rules:
- Data Structures: completed intro AND grade >= B
- Web Development: completed intro AND interested in design
- Algorithms: completed intro AND enjoys problem-solving AND grade >= A
```

---

## 🚗 Automotive Examples

### Example 12: Car Maintenance Scheduler

```
Problem: Determine car maintenance needs
Data: Car has 45000 miles, last oil change at 40000 miles, tires are 3 years old
Rules:
- Oil change needed: miles since last change > 5000
- Tire replacement needed: tire age > 5 years OR tread depth < 2mm
- General inspection: miles > 50000 OR age > 3 years
```

---

### Example 13: Traffic Light Decision

```
Problem: Decide driver action at traffic light
Data: Light is yellow, car is 20 meters from intersection, speed is 50 km/h
Rules:
- Stop: light is red OR (light is yellow AND distance > 30m)
- Proceed with caution: light is yellow AND distance < 15m
- Go: light is green
```

---

## 🍽️ Food & Beverage Examples

### Example 14: Coffee Recommendation

```
Problem: Recommend coffee based on time and preference
Data: It's 3 PM, customer prefers mild flavor, wants cold beverage
Rules:
- Morning (6-11 AM) + strong = Espresso
- Afternoon (12-5 PM) + cold = Iced Latte
- Evening (6-10 PM) = Decaf
- Cold preference + any time = Cold Brew
```

---

### Example 15: Recipe Difficulty Classification

```
Problem: Classify recipe difficulty
Data: Recipe has 12 ingredients, takes 45 minutes, requires oven and mixer
Rules:
- Easy: ingredients < 8 AND time < 30 AND basic tools only
- Medium: ingredients 8-15 AND time 30-60
- Hard: ingredients > 15 OR time > 60 OR special equipment required
```

---

## 💼 Business Examples

### Example 16: Customer Segment Classification

```
Problem: Classify customers into segments
Data: Customer spent $5000 last year, made 15 purchases, member for 3 years
Rules:
- VIP: spending > $3000 AND purchases > 10
- Regular: spending > $1000 AND purchases > 5
- Occasional: spending > $500
- Inactive: spending < $500 OR no purchases in last year
```

---

### Example 17: Product Pricing Strategy

```
Problem: Determine product pricing strategy
Data: Product cost is $50, competitor price is $80, quality rating is high
Rules:
- Premium pricing: quality high AND competitor price > cost * 1.5
- Competitive pricing: competitor price within 10% of our cost * 1.3
- Discount pricing: need to clear inventory OR seasonal sale
```

---

## 🌦️ Weather Examples

### Example 18: Clothing Recommendation

```
Problem: Recommend clothing based on weather
Data: Temperature is 15°C, raining, wind speed is 20 km/h
Rules:
- Heavy jacket: temperature < 10 OR (temperature < 15 AND raining)
- Light jacket: temperature 10-20 AND not raining
- T-shirt: temperature > 25
- Add umbrella: if raining
- Add scarf: if wind speed > 15 km/h
```

---

## 🎮 Gaming Examples

### Example 19: Game Difficulty Selector

```
Problem: Select appropriate game difficulty
Data: Player completed 5 games, average score is 85%, prefers challenge
Rules:
- Expert: completed > 3 games AND average score > 80% AND prefers challenge
- Advanced: completed > 2 games AND average score > 70%
- Intermediate: completed > 1 game
- Beginner: no games completed OR average score < 50%
```

---

## 🔋 IoT & Smart Home Examples

### Example 20: Smart Thermostat Control

```
Problem: Control home thermostat automatically
Data: Room temperature is 18°C, outside temperature is 5°C, occupancy is detected, time is 7 PM
Rules:
- Heat to 22°C: occupied AND temperature < 20 AND time 6 AM - 10 PM
- Heat to 18°C: unoccupied OR time 10 PM - 6 AM
- No heating: temperature > 23
- Fan mode: temperature > 20 AND < 23
```

---

## 💡 Tips for Writing Good Problems

1. **Be Specific**: Include actual data values
2. **State Rules Clearly**: Use AND, OR, comparisons explicitly
3. **Include Context**: What domain? What's the goal?
4. **Provide Examples**: At least one example data point
5. **Keep it Simple**: Start with 2-3 rules, add complexity later

---

## 🚀 Quick Start

1. Run the program:
   ```bash
   python llm2clips.py
   ```

2. Copy one of the examples above

3. Paste when prompted

4. See the magic happen!

---

**Happy Expert System Building!** 🧠✨

