# camera-autofocus-fuzzy-controller
Design and simulation of a fuzzy logic controller for camera autofocus using Python and scikit-fuzzy.
# Camera Autofocus Using Fuzzy Logic Controller

## Project Overview

This Project-Based Learning (PBL) project focuses on the design and simulation of a fuzzy logic controller for a camera autofocus system.

The controller uses sharpness error and its rate of change to determine the required lens motor movement. A fuzzy inference system, membership functions, and an eight-rule rule base are used to calculate the control output.

## Objectives

- Identify the input and output variables of the autofocus controller.
- Design triangular and trapezoidal membership functions.
- Develop an eight-rule fuzzy rule base.
- Implement fuzzification, rule evaluation, and defuzzification.
- Test the controller using different input combinations.

## System Variables

| Variable | Description | Range |
|---|---|---|
| E | Sharpness Error | -10 to +10 |
| dE | Rate of Change of Error | -5 to +5 |
| O | Lens Motor Step | -50 to +50 |

## Technologies Used

- Python
- NumPy
- Pandas
- Matplotlib
- scikit-fuzzy
- Streamlit
- Google Colab

## Sample Result

For the sample input:

- Sharpness Error: E = 4
- Rate of Change of Error: dE = 2

Rules R6 and R7 are activated. Using the weighted-average method, the calculated output is approximately **36.68 motor steps in the forward direction**.

## Project Files

- `Camera_Autofocus_Fuzzy_Controller.ipynb` — Notebook implementation and visualizations.
- `Camera_Autofocus_Streamlit_App.py` — Interactive Streamlit application.
- `docs/` — Project report and presentation.
- `requirements.txt` — Python dependencies.

## Running the Streamlit Application

Install the dependencies:

```bash
pip install -r requirements.txt
```

Launch the application:

```bash
streamlit run Camera_Autofocus_Streamlit_App.py
```

## Limitations and Future Scope

The current project is a software simulation and has not been tested with a physical camera lens or motor. Future work includes improving rule-base coverage and integrating the controller with camera hardware.

## Team Members

- Tharakan Rahil Ramchandran
- Shivam Nandi
- Arun Rathore

## Institution

L.D. College of Engineering, Ahmedabad  
Department of Electronics & Communication Engineering  
Academic Year: 2026–2027
