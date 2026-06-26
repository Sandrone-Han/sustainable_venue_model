# Sustainable Venue Food Waste Collection Optimisation Model

## 1. Project Overview

This project transforms an initial PowerPoint-based sustainable venue proposal into a runnable Python mathematical optimisation model. The original idea focused on improving sustainability for Birmingham venues. This implementation converts that idea into a data-driven model that can calculate food waste generation, evaluate collection routes, estimate carbon emissions, and compare baseline and optimised strategies.

The model focuses on food waste collection from multiple venues. Each venue has estimated visitor flow, food supply, food waste generation, and simplified two-dimensional location coordinates. A treatment centre is used as the start and end point of the collection route.

The project compares two route strategies:

1. A manually defined baseline route.
2. An optimised route found by exhaustive search.

The model then calculates the total route distance and carbon emissions for both diesel and electric vehicles. It also generates visual outputs, including route maps and carbon emission comparison charts.

---

## 2. 中文项目说明

本项目将最初的可持续场馆 PPT 概念转化为一个可运行的 Python 数学优化模型。原始项目主要停留在展示层面，提出了面向伯明翰场馆的可持续技术方案。本项目进一步将该概念转化为可计算、可比较、可优化的模型。

模型以多个伯明翰场馆为对象，输入数据包括人流量、食物供应量、厨余垃圾量和简化二维坐标。程序首先读取场馆数据，然后计算场馆之间的距离矩阵。之后，模型会计算人工设定的 baseline route，并通过穷举搜索方法自动寻找总距离最短的 optimised route。

最终，模型会对比 baseline route 和 optimised route 在总行驶距离、柴油车碳排放和电动车碳排放方面的差异，并生成可视化图像。这使得原本的可持续发展建议能够转化为量化结果，从而更适合用于课程项目展示、报告撰写和后续模型扩展。

---

## 3. Project Aim

The aim of this project is to develop a simple but complete optimisation model for sustainable food waste collection from Birmingham venues.

The project aims to:

* Convert a conceptual sustainability proposal into a computational model.
* Estimate food waste generation from venue-level input data.
* Calculate distances between venues.
* Compare a baseline route with an optimised route.
* Estimate carbon emissions under diesel and electric vehicle scenarios.
* Visualise route optimisation and emission reduction results.
* Link the technical model to Sustainable Development Goals.

---

## 4. Problem Statement

Large venues generate significant food waste during events. If food waste collection routes are not planned efficiently, unnecessary travel distance and carbon emissions may be produced.

This project addresses the following question:

How can a food waste collection route for multiple Birmingham venues be optimised to reduce total travel distance and carbon emissions?

The model assumes that a collection vehicle starts from a treatment centre, visits all venues once, collects food waste, and then returns to the treatment centre.

---

## 5. Project Structure

The project folder is organised as follows:

```text
sustainable_venue_model
│
├── main.py
├── README.md
├── requirements.txt
│
├── data
│   └── venues.csv
│
└── outputs
    ├── baseline_route_map.png
    ├── optimised_route_map.png
    └── emissions_comparison.png
```

### File Description

| File or Folder             | Description                                                                                                                           |
| -------------------------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| `main.py`                  | Main Python script containing data loading, distance calculation, route optimisation, carbon emission calculation, and visualisation. |
| `README.md`                | Project documentation file.                                                                                                           |
| `requirements.txt`         | List of required Python packages.                                                                                                     |
| `data/venues.csv`          | Input dataset containing venue information.                                                                                           |
| `outputs/`                 | Folder for generated figures.                                                                                                         |
| `baseline_route_map.png`   | Visualisation of the manually defined baseline route.                                                                                 |
| `optimised_route_map.png`  | Visualisation of the optimised route.                                                                                                 |
| `emissions_comparison.png` | Bar chart comparing carbon emissions under different scenarios.                                                                       |

---

## 6. Input Data

The input data are stored in:

```text
data/venues.csv
```

The CSV file contains the following columns:

| Column           | Description                           |
| ---------------- | ------------------------------------- |
| `venue`          | Name of the venue.                    |
| `visitor_flow`   | Estimated number of visitors.         |
| `food_supply_kg` | Estimated food supply in kilograms.   |
| `waste_rate`     | Assumed food waste rate.              |
| `waste_kg`       | Estimated food waste in kilograms.    |
| `x`              | Simplified x-coordinate of the venue. |
| `y`              | Simplified y-coordinate of the venue. |

The current input dataset is:

```csv
venue,visitor_flow,food_supply_kg,waste_rate,waste_kg,x,y
Treatment Centre,0,0,0,0,0,0
Birmingham Arena,8000,3000,0.20,600,2,5
Symphony Hall,3000,1200,0.20,240,3,4
Edgbaston Stadium,15000,6000,0.20,1200,6,2
NEC Birmingham,20000,8000,0.20,1600,10,7
University Venue,5000,2000,0.20,400,5,1
```

---

## 7. Model Assumptions

The model uses several simplifying assumptions to make the optimisation problem suitable for a compact Python demonstration.

### 7.1 Venue Location

The model uses simplified two-dimensional coordinates instead of real geographic coordinates. This allows the route optimisation logic to be demonstrated clearly without requiring map APIs or real traffic data.

### 7.2 Food Waste Generation

Food waste is estimated using:

```text
Food waste = food supply × waste rate
```

In this project, the waste rate is assumed to be 20 percent for all venues.

### 7.3 Route Structure

The collection vehicle:

1. Starts from the treatment centre.
2. Visits each venue once.
3. Collects food waste from all venues.
4. Returns to the treatment centre.

### 7.4 Vehicle Capacity

The current version focuses on route distance and carbon emissions. Vehicle capacity constraints are not included in this version. This can be added in future versions to extend the model from a travelling salesman problem to a vehicle routing problem.

### 7.5 Carbon Emission Factors

The model uses the following assumed emission factors:

```text
Diesel vehicle: 0.25 kg CO2 per km
Electric vehicle: 0.08 kg CO2 per km
```

These values are used for demonstration and comparative analysis.

---

## 8. Mathematical Model

### 8.1 Distance Calculation

The model calculates the distance between two venues using Euclidean distance:

```text
distance = sqrt((x1 - x2)^2 + (y1 - y2)^2)
```

where:

```text
x1, y1 = coordinates of the first venue
x2, y2 = coordinates of the second venue
```

### 8.2 Total Route Distance

The total route distance is calculated by summing the distances between consecutive venues in the route:

```text
total route distance = sum of all route segment distances
```

For example, if the route is:

```text
Treatment Centre -> Venue A -> Venue B -> Treatment Centre
```

then the total distance is:

```text
distance(Treatment Centre, Venue A)
+ distance(Venue A, Venue B)
+ distance(Venue B, Treatment Centre)
```

### 8.3 Carbon Emission Calculation

Carbon emissions are calculated using:

```text
carbon emissions = total route distance × emission factor
```

The model calculates emissions for both diesel and electric vehicle scenarios.

### 8.4 Optimisation Objective

The optimisation objective is:

```text
Minimise total route distance
```

Since carbon emissions are directly proportional to total route distance, minimising distance also reduces carbon emissions.

---

## 9. Optimisation Method

The project currently uses exhaustive search.

Exhaustive search tests every possible visiting order for the venues. The treatment centre is fixed as both the start and end point. The other venues are rearranged in all possible orders. For each possible route, the total route distance is calculated. The route with the smallest total distance is selected as the optimised route.

This method is suitable for the current small dataset because there are only five collection venues. With five venues, the number of possible routes is:

```text
5! = 120 routes
```

This is small enough for Python to calculate directly.

For larger datasets, this method can be replaced by a genetic algorithm or a vehicle routing optimisation method.

---

## 10. Baseline Route

The baseline route is manually defined as:

```text
Treatment Centre
-> Birmingham Arena
-> Symphony Hall
-> Edgbaston Stadium
-> NEC Birmingham
-> University Venue
-> Treatment Centre
```

This route represents the original non-optimised collection strategy. It is used as a comparison benchmark.

---

## 11. Optimised Route

The optimised route is generated automatically by the Python program. The program tests all possible route permutations and selects the shortest one.

The exact optimised route depends on the input coordinates in `venues.csv`.

The program prints the optimised route in the terminal after execution.

---

## 12. Output Results

After running the model, the program outputs:

* Venue data summary.
* Total collected food waste.
* Baseline route distance.
* Baseline diesel vehicle emissions.
* Baseline electric vehicle emissions.
* Optimised route distance.
* Optimised diesel vehicle emissions.
* Optimised electric vehicle emissions.
* Percentage reduction in distance and emissions.
* Generated output figure paths.

The output figures are saved in:

```text
outputs/
```

---

## 13. Output Figures

### 13.1 Baseline Route Map

File name:

```text
outputs/baseline_route_map.png
```

This figure shows the manually defined food waste collection route.

### 13.2 Optimised Route Map

File name:

```text
outputs/optimised_route_map.png
```

This figure shows the shortest route found by the optimisation model.

### 13.3 Emissions Comparison Chart

File name:

```text
outputs/emissions_comparison.png
```

This figure compares four scenarios:

```text
Baseline Diesel
Optimised Diesel
Baseline EV
Optimised EV
```

The chart helps show how route optimisation and vehicle electrification can reduce carbon emissions.

---

## 14. How to Run the Project

### 14.1 Install Python

Make sure Python is installed on the computer.

On Windows, the project can be run using:

```bash
py main.py
```

### 14.2 Install Required Package

Install the required Python package:

```bash
py -m pip install matplotlib
```

Or install all packages from `requirements.txt`:

```bash
py -m pip install -r requirements.txt
```

### 14.3 Run the Model

From the project folder, run:

```bash
py main.py
```

The terminal should display the route analysis and comparison results.

---

## 15. Requirements

The project requires:

```text
Python 3
matplotlib
```

The `requirements.txt` file should contain:

```text
matplotlib
```

---

## 16. Example Terminal Output

A successful run should display output similar to:

```text
Venue data loaded successfully.
--------------------------------------------------------------------------------
Venue                       Visitors    Food kg   Waste kg      X      Y
--------------------------------------------------------------------------------
Treatment Centre                  0        0.0        0.0    0.0    0.0
Birmingham Arena               8000     3000.0      600.0    2.0    5.0
Symphony Hall                  3000     1200.0      240.0    3.0    4.0
Edgbaston Stadium             15000     6000.0     1200.0    6.0    2.0
NEC Birmingham                20000     8000.0     1600.0   10.0    7.0
University Venue               5000     2000.0      400.0    5.0    1.0
--------------------------------------------------------------------------------

Total collected food waste: 4040.00 kg

Baseline route analysis:
--------------------------------------------------------------------------------
Treatment Centre -> Birmingham Arena -> Symphony Hall -> Edgbaston Stadium -> NEC Birmingham -> University Venue -> Treatment Centre
--------------------------------------------------------------------------------
Total route distance:       calculated by the program
Diesel vehicle emissions:   calculated by the program
Electric vehicle emissions: calculated by the program
--------------------------------------------------------------------------------

Optimised route analysis:
--------------------------------------------------------------------------------
The optimised route is calculated by the program.
--------------------------------------------------------------------------------
Total route distance:       calculated by the program
Diesel vehicle emissions:   calculated by the program
Electric vehicle emissions: calculated by the program
--------------------------------------------------------------------------------
```

---

## 17. Relevance to Sustainable Development Goals

This project is related to several Sustainable Development Goals.

### SDG 11: Sustainable Cities and Communities

The model supports more sustainable urban event management by reducing unnecessary vehicle travel and improving the planning of waste collection operations.

### SDG 12: Responsible Consumption and Production

The project addresses food waste management by estimating food waste generation and supporting more efficient collection planning.

### SDG 13: Climate Action

The model estimates carbon emissions and compares diesel and electric vehicle scenarios. It demonstrates how route optimisation and low-emission transport can contribute to emission reduction.

---

## 18. Project Significance

The main significance of this project is that it turns a general sustainability idea into a measurable optimisation model. Instead of only describing sustainable solutions, the model provides numerical outputs that can be analysed and compared.

The project demonstrates how mathematical optimisation and Python programming can support sustainable decision-making for event venues.

The model provides:

* A clear input dataset.
* A computable distance model.
* A baseline strategy.
* An optimised strategy.
* Carbon emission estimation.
* Visual evidence of improvement.
* A connection between engineering modelling and sustainability goals.

---

## 19. Limitations

The current model has several limitations:

1. The venue coordinates are simplified rather than real geographic coordinates.
2. Road network distance is not considered.
3. Real traffic conditions are not included.
4. Vehicle capacity constraints are not included.
5. Collection time windows are not included.
6. Food waste generation is estimated using a fixed waste rate.
7. Emission factors are assumed for demonstration purposes.

These limitations are acceptable for an initial project demo, but they should be acknowledged in the final presentation or report.

---

## 20. Future Improvements

The model can be improved in several ways:

### 20.1 Use Real Geographic Coordinates

The simplified coordinates can be replaced with real latitude and longitude data for Birmingham venues.

### 20.2 Use Real Road Distances

Instead of Euclidean distance, the model could use road distance from map data or routing APIs.

### 20.3 Add Vehicle Capacity Constraints

Vehicle capacity can be added so that the model becomes a vehicle routing problem instead of a simple travelling salesman problem.

### 20.4 Add Multiple Vehicles

The model can be extended to support multiple collection vehicles.

### 20.5 Add Genetic Algorithm Optimisation

For larger datasets, exhaustive search becomes inefficient. A genetic algorithm can be used to find near-optimal routes more efficiently.

### 20.6 Add Cost Analysis

The model can include fuel cost, electricity cost, labour cost, and waste treatment cost.

### 20.7 Add Real-Time Event Data

Visitor flow and waste generation could be updated dynamically based on real event attendance data.

---

## 21. Possible Presentation Description

The following description can be used in a project presentation:

This project converts a sustainable venue concept into a Python-based optimisation model. The model uses venue-level data, including visitor flow, food supply, food waste generation, and location coordinates, to calculate a food waste collection route. A baseline route is compared with an optimised route found by exhaustive search. The model then estimates carbon emissions for diesel and electric vehicles and generates visual outputs. The results show how route optimisation and vehicle electrification can support sustainable event management and contribute to SDG 11, SDG 12, and SDG 13.

中文版本：

本项目将可持续场馆概念转化为一个基于 Python 的优化模型。模型使用场馆人流量、食物供应量、厨余垃圾量和位置坐标作为输入，计算厨余垃圾清运路线。项目对比了人工设定的 baseline route 和通过穷举搜索得到的 optimised route，并进一步计算柴油车和电动车场景下的碳排放。结果表明，路线优化和车辆电动化能够帮助降低运输距离和碳排放，从而支持可持续城市管理、负责任消费与生产以及气候行动等可持续发展目标。

---

## 22. Conclusion

This project successfully upgrades the original PowerPoint-based sustainability proposal into a runnable optimisation model. The model demonstrates how Python, mathematical optimisation, and data visualisation can be used to support sustainable venue management.

By comparing baseline and optimised routes, the project provides quantitative evidence for reducing travel distance and carbon emissions. The model is simple, explainable, and suitable for further extension into more advanced routing, carbon accounting, and sustainability decision-support systems.

