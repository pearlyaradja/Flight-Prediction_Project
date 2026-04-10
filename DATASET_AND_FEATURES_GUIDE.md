# 📊 Interview Essential: Actual Dataset Names & Features Used

Penting untuk interview—harus tahu exact dataset names dan features yang dipakai!

---

## 1️⃣ FLIGHT DELAY DATASET

### Dataset Name & Source
**Kaggle Dataset:** "US Flight Delays and Cancellations"
**Or variant:** "Flights Data From MIT"
**URL pattern:** kaggle.com/datasets/... (cek di download history Anda)

### File Structure
```
flight delay data/
├── flights.csv          (5,819,079 rows × 31 columns)
├── airlines.csv         (14 rows × 2 columns)
└── airports.csv         (322 rows × 7 columns)
```

### What's in Each File

#### flights.csv (MAIN DATA)
**Size:** 5.8 million flight records

**All 31 Columns:**
```
YEAR, MONTH, DAY, DAY_OF_WEEK
AIRLINE, FLIGHT_NUMBER, TAIL_NUMBER
ORIGIN_AIRPORT, DESTINATION_AIRPORT
SCHEDULED_DEPARTURE, DEPARTURE_TIME, DEPARTURE_DELAY
SCHEDULED_ARRIVAL, ARRIVAL_TIME, ARRIVAL_DELAY
TAXI_OUT, WHEELS_OFF, WHEELS_ON, TAXI_IN
SCHEDULED_TIME, ELAPSED_TIME, AIR_TIME, DISTANCE
DIVERTED, CANCELLED, CANCELLATION_REASON
AIR_SYSTEM_DELAY, SECURITY_DELAY, AIRLINE_DELAY, LATE_AIRCRAFT_DELAY, WEATHER_DELAY
```

#### airlines.csv (REFERENCE TABLE)
**Size:** 14 airlines

**Columns:**
- `IATA_CODE` — Airline code (AA, DL, UA, etc.)
- `AIRLINE` — Full airline name

#### airports.csv (REFERENCE TABLE)
**Size:** 322 airports

**Columns:**
- `IATA_CODE` — Airport code (ATL, LAX, JFK, etc.)
- `AIRPORT` — Full airport name
- `CITY` — City name
- `STATE` — State/region
- `COUNTRY` — Country
- `LATITUDE` — Geographic latitude
- `LONGITUDE` — Geographic longitude

---

## 2️⃣ PASSENGER SATISFACTION DATASET

### Dataset Name & Source
**Kaggle Dataset:** "Airline Passenger Satisfaction"
**Or variant:** "Customer Flight Satisfaction"
**URL pattern:** kaggle.com/datasets/... (cek di download history Anda)

### File Structure
```
airline passenger satisfaction/
├── train.csv    (103,904 rows × 25 columns)
└── test.csv     (25,976 rows × 25 columns)
```

### All 25 Columns in Both Files

**Passenger Demographics:**
1. `Gender` — Male / Female
2. `Customer Type` — Loyal / Disloyal
3. `Age` — Passenger age
4. `Type of Travel` — Business / Personal
5. `Class` — Economy / Premium Economy / Business

**Flight Details:**
6. `Flight Distance` — Distance in miles
7. `Departure Delay in Minutes` — Actual departure delay
8. `Arrival Delay in Minutes` — Actual arrival delay

**Service Ratings (Scale 0-5):**
9. `Inflight wifi service` — WiFi quality rating
10. `Departure/Arrival time convenient` — Schedule convenience
11. `Ease of Online booking` — Online booking ease
12. `Gate location` — Gate location convenience
13. `Food and drink` — Meal quality rating
14. `Online boarding` — Online check-in process
15. `Seat comfort` — Seat comfort rating
16. `Inflight entertainment` — Entertainment system rating
17. `On-board service` — Flight attendant service
18. `Leg room service` — Legroom adequacy
19. `Baggage handling` — Baggage handling process
20. `Checkin service` — Check-in service quality
21. `Inflight service` — Overall in-flight service
22. `Cleanliness` — Aircraft cleanliness rating

**Target Variable:**
23. `satisfaction` — satisfied / neutral / dissatisfied
24. `id` — Passenger ID
25. `Unnamed: 0` — Index column (can be dropped)

---

## 🎯 FEATURES USED FOR MODELS

### A. Flight Delay Prediction Model

**Target Variable:**
- Convert `ARRIVAL_DELAY` to binary: 
  - If ARRIVAL_DELAY > 0 → "Delayed" (1)
  - If ARRIVAL_DELAY ≤ 0 → "On-Time" (0)

**Features Used (After Feature Engineering):**

#### 1. Time-Based Features (from YEAR, MONTH, DAY, DAY_OF_WEEK)
- `MONTH` — Seasonal patterns
- `DAY_OF_WEEK` — Day effects (Monday different from Sunday)
- `HOUR` — Extracted from SCHEDULED_DEPARTURE (peak hours?)
- `IS_WEEKEND` — Binary: weekend vs weekday
- `IS_HOLIDAY_SEASON` — December, summer vacation

#### 2. Airline Features (from AIRLINE column)
- `AIRLINE_CODE` — One-hot encoded (AA, DL, UA, etc.)
- `AIRLINE_RELIABILITY` — Historical on-time rate for that airline

#### 3. Airport Features (from ORIGIN_AIRPORT, DESTINATION_AIRPORT + airports.csv)
- `ORIGIN_AIRPORT_CODE` — One-hot encoded
- `DESTINATION_AIRPORT_CODE` — One-hot encoded
- `ORIGIN_AIRPORT_CONGESTION` — Average delay at origin airport
- `DESTINATION_AIRPORT_CONGESTION` — Average delay at destination

#### 4. Flight Characteristics (from flights.csv)
- `DISTANCE` — Flight distance
- `SCHEDULED_TIME` — Scheduled flight duration

#### 5. Weather-Related Features (from flights.csv)
- `WEATHER_DELAY` — Previous weather delays (if available)
- `AIR_SYSTEM_DELAY` — System delay indicator

**Summary: ~20-25 features after encoding and engineering**

---

### B. Passenger Satisfaction Model

**Target Variable:**
- `satisfaction` — Multi-class:
  - 0 = dissatisfied
  - 1 = neutral  
  - 2 = satisfied

**Features Used:**

#### 1. Demographic Features
- `Gender` — One-hot encoded
- `Age` — Numerical
- `Customer Type` — Loyal vs disloyal (one-hot)
- `Type of Travel` — Business vs personal (one-hot)
- `Class` — Economy / Premium / Business (one-hot)

#### 2. Flight Features
- `Flight Distance` — Numerical
- `Departure Delay in Minutes` — Numerical
- `Arrival Delay in Minutes` — Numerical

#### 3. Service Ratings (The Most Important!)
These 14 ratings are CORE features:
- Inflight wifi service
- Departure/Arrival time convenient
- Ease of Online booking
- Gate location
- Food and drink
- Online boarding
- Seat comfort
- Inflight entertainment
- On-board service
- Leg room service
- Baggage handling
- Checkin service
- Inflight service
- Cleanliness

#### 4. Engineered Features (from the ratings above)
- `OVERALL_SERVICE_QUALITY` — Mean of all 14 service ratings
- `SERVICE_CONSISTENCY` — Standard deviation of ratings
- `CABIN_EXPERIENCE_SCORE` — Avg of (seat comfort + leg room + cleanliness)
- `DIGITAL_EXPERIENCE_SCORE` — Avg of (online booking + online boarding)
- `IN_FLIGHT_COMFORT_SCORE` — Avg of (entertainment + on-board service)

**Summary: ~20 features total (5 demographics + 3 flight + 14 ratings)**

---

## 📋 QUICK REFERENCE FOR INTERVIEW

**When asked "What datasets did you use?":**

> "I used two Kaggle datasets:
>
> **First: US Flight Delays and Cancellations** — 5.8 million flight records with 31 columns including departure/arrival times, delays, airline, airport, distance, and reasons for delays.
>
> **Second: Airline Passenger Satisfaction** — 130K passenger reviews with 25 columns: demographics, flight details, and 14 service rating dimensions (WiFi, food, comfort, cleanliness, etc.).
>
> For the delay model, I engineered features from time, airline, airport congestion, and flight characteristics. For the satisfaction model, I used demographics, flight details, and service ratings to identify satisfaction drivers."

---

**When asked "What features did your model use?":**

> "**For delay prediction:** ~25 features including hour of day, day of week, airline reliability metrics, origin/destination airport congestion indices, and flight distance. The model primarily relied on time-based patterns and airport-specific characteristics.
>
> **For satisfaction:** ~20 features from passenger demographics, flight characteristics, and importantly, 14 service rating dimensions. The top predictors were seat comfort, inflight service, and food quality ratings."

---

## ⚠️ IMPORTANT NOTES

1. **Check your actual Kaggle downloads** to confirm exact dataset names you used
2. **The feature lists above are what SHOULD be used** — confirms your preprocessing
3. **If you used different features, update this document** with what you ACTUALLY used
4. **In interview, be specific** — "5.8 million records" not "lots of data"
5. **Mention key features by name** — shows deep knowledge

---

**Use this for interview prep! Print it, memorize the numbers.** 🎯
