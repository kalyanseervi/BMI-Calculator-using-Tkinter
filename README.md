
# 🏋️‍♂️ BMI Calculator with Gauge

The **BMI Calculator with Gauge** is a desktop application built with **Tkinter**. It allows users to calculate their Body Mass Index (BMI), save records, and visualize BMI trends and gauge data. The application also provides a robust database to store and retrieve user information.

---

## 🖥️ Features

- **BMI Calculation**:
  - Accepts weight (kg) and height (cm) as inputs.
  - Calculates BMI and categorizes it as *Underweight*, *Normal*, *Overweight*, or *Obese*.
- **Data Storage**:
  - Saves user details and BMI history into a local SQLite database.
- **Data Visualization**:
  - Interactive **BMI Gauge** using Plotly.
  - Graphical trends of BMI over time using Matplotlib.
- **User Management**:
  - Unique email-based user record storage.
  - Displays user-specific BMI history.
- **User-Friendly Interface**:
  - Modern UI/UX design for ease of use.
  - Responsive input validation and error handling.

---

## 🛠️ Technologies Used

- **Python**: Core language.
- **Tkinter**: For GUI development.
- **SQLite**: Lightweight database for storing user records.
- **Plotly**: For dynamic BMI gauge visualization.
- **Matplotlib**: For BMI trends over time.

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher installed on your system.
- Required Python packages:
  ```bash
  pip install matplotlib plotly
  ```

---

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/kalyanseervi/BMI-Calculator-using-Tkinter.git
   ```
2. Run the application:
   ```bash
   python bmi.py
   ```

---

## 📋 Usage

1. **Launch the application.**
2. **Input your details**:
   - Name, email, gender, weight (in kg), and height (in cm).
3. Click **Calculate and Save** to calculate BMI, display the gauge, and save records.
4. Use the following buttons:
   - **View Records**: See your past BMI history.
   - **View BMI Trends**: Visualize BMI changes over time in a graph.

---

## 📝 Screenshots

### Main Interface
![Main Interface](path/to/main-interface-screenshot.png)

### BMI Gauge
![BMI Gauge](path/to/bmi-gauge-screenshot.png)

### BMI Trends
![BMI Trends](path/to/bmi-trends-screenshot.png)

---

## ⚠️ Validation and Error Handling

- Ensures all fields are filled.
- Validates email format.
- Weight and height must be positive numbers.
- Prevents duplicate emails in the database.

---

## 📊 Categories of BMI

| BMI Range         | Category       |
|--------------------|----------------|
| Below 18.5         | Underweight    |
| 18.5 - 24.9        | Normal weight  |
| 25.0 - 29.9        | Overweight     |
| 30.0 and above     | Obese          |

---

## 📜 License

This project is licensed under the [MIT License](LICENSE).

---

## 💡 Future Enhancements

- Add multilingual support.
- Add more advanced visualizations.
- Provide export functionality for BMI records.

---

## 🤝 Contributing

Contributions are welcome! Follow these steps:

1. Fork the repository.
2. Create a new branch:
   ```bash
   git checkout -b feature-branch
   ```
3. Make your changes and commit:
   ```bash
   git commit -m "Add feature"
   ```
4. Push to your branch:
   ```bash
   git push origin feature-branch
   ```
5. Submit a pull request.

---

## 💬 Contact

For questions, reach out via **kalyanseerviy125@gmail.com**.
