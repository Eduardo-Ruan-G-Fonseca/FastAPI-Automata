# Automata API - Implementation of Automata with FastAPI

## 📌 About the API
This API allows the simulation of three types of automata:
1. **DFA** (Deterministic Finite Automaton)
2. **DPDA** (Deterministic Pushdown Automaton)
3. **DTM** (Deterministic Turing Machine)

The API was developed using **FastAPI** and the **Automata** library to process and analyze automata.

## 🔹 Features
- Send automaton configurations via JSON.
- Check if an input is accepted by the corresponding automaton.
- Generate and visualize the automaton diagram (for DFA and DPDA).

## 🔹 Endpoints
- `POST /dfa/` → Processes a DFA, checks if it accepts the input, and generates the diagram.
- `POST /dpda/` → Processes a DPDA and checks if it accepts the input.
- `POST /dtm/` → Processes a Deterministic Turing Machine (DTM) and checks if it accepts the input.
- `GET /` → Serves a simple web interface to interact with the API.

## 📜 Automatic Documentation
- Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## 🚀 How to Run
### 1️⃣ Install Dependencies
Make sure you have **Python 3.8+** installed. Run:
```sh
pip install fastapi automata
```

### 2️⃣ Start the API
```sh
fastapi dev main.py
```

The API will be accessible at: [http://127.0.0.1:8000](http://127.0.0.1:8000)

## 📌 Usage Examples
### 🔹 Example JSON for DFA
```json
{
  "states": ["q0", "q1", "q2"],
  "input_symbols": ["0", "1"],
  "transitions": {
    "q0": {"0": "q1", "1": "q0"},
    "q1": {"0": "q2", "1": "q0"},
    "q2": {"0": "q2", "1": "q2"}
  },
  "initial_state": "q0",
  "final_states": ["q2"],
  "input": "001"
}
```
![image](https://github.com/user-attachments/assets/7e7af2f9-4d77-4679-96e4-7db7595e1bb3)


### 🔹 Example JSON for DPDA
```json
{
  "states": ["q0", "q1", "q2"],
  "input_symbols": ["a", "b"],
  "stack_symbols": ["X", "Z"],
  "transitions": {
    "q0": {"a": {"Z": ["q1", ["X", "Z"]]}},
    "q1": {"b": {"X": ["q2", [""]]}},
    "q2": {}
  },
  "initial_state": "q0",
  "initial_stack_symbol": "Z",
  "final_states": ["q2"],
  "input": "ab"
}
```

### 🔹 Example JSON for DTM
```json
{
  "states": ["q0", "q1", "q2"],
  "input_symbols": ["0", "1"],
  "tape_symbols": ["0", "1", "_"],
  "transitions": {
    "q0": {"0": ["q1", "1", "R"]},
    "q1": {"1": ["q2", "0", "R"]},
    "q2": {"_": ["q2", "_", "R"]}
  },
  "initial_state": "q0",
  "blank_symbol": "_",
  "final_states": ["q2"],
  "input": "01"
}
```
![image](https://github.com/user-attachments/assets/dbf147c2-ed4a-4ffe-a43d-9251e61d1e4f)

## 📌 Expected Responses
### 🔹 DFA
```json
{
  "accepted": true,
  "diagram_path": "/static/dfa_diagram.png"
}
```

### 🔹 DPDA
```json
{
  "accepted": true,
  "diagram_path": "/static/dpda_diagram.png"
}
```

### 🔹 DTM
```json
{
  "accepted": true
}
```

## 📌 Practical Assignment
This project is part of a practical assignment in the **Theory of Computation** course. The goal is to develop a REST API that manipulates and analyzes automata, connecting theoretical concepts to real-world applications.

### 📌 Assignment Requirements
1. Implement a RESTful API using **FastAPI**.
2. Support three types of automata (**DFA, DPDA, and DTM**).
3. Document the API using **Swagger UI and ReDoc**.
4. Generate diagrams for DFA and DPDA.
5. Provide a web interface to interact with the automata.

The API allows users to submit automata in JSON format, test inputs, and visualize responses, including graphical representations of the processed automata. The final goal is to reinforce the learning of automata and their applicability in computing.

## 🛠 Technologies Used
- **Python 3.8+**
- **FastAPI** for creating RESTful endpoints.
- **Automata** for handling and analyzing automata.

## 📄 License
This project is licensed under the **MIT License**.

