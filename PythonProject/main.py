"""
Automata API - Implementation of automata with FastAPI

📌 This API processes three types of automata:
1️⃣ DFA (Deterministic Finite Automaton)
2️⃣ DPDA (Deterministic Pushdown Automaton)
3️⃣ DTM (Deterministic Turing Machine)

🔹 Features:
- Send configurations via JSON.
- Check if the input is accepted by the automaton.
- Generate and visualize the automaton diagram.

🔹 Endpoints:
- `/dfa/`  → Processes a DFA, returns if it accepts the input, and generates the diagram.
- `/dpda/` → Processes a DPDA and checks if it accepts the input.
- `/dtm/`  → Processes a Deterministic Turing Machine (DTM).

🔹 Automatic documentation:
- 📜 Swagger UI: http://127.0.0.1:8000/docs
- 📜 ReDoc: http://127.0.0.1:8000/redoc
"""

import os
from fastapi import FastAPI
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel
from typing import Dict, Set
from automata.fa.dfa import DFA
from automata.pda.dpda import DPDA
from automata.tm.dtm import DTM
from fastapi.staticfiles import StaticFiles

# FastAPI instance
app = FastAPI(
    title="Automata API",
    description="API for automata simulation (DFA, DPDA, DTM) with diagram generation.",
    version="1.0.0"
)

# Static files directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
os.makedirs(STATIC_DIR, exist_ok=True)

# Paths for generated images
IMAGE_PATH_DFA = os.path.join(STATIC_DIR, "dfa_diagram.png")
IMAGE_PATH_DPDA = os.path.join(STATIC_DIR, "dpda_diagram.png")

# Serving static files
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

### 📌 SERVING THE HTML INTERFACE
@app.get("/", response_class=FileResponse, summary="Serve the web interface")
async def serve_ui():
    """📜 Serve the HTML interface of the API at `/`."""
    return os.path.join(STATIC_DIR, "index.html")

# ========================== DFA ==========================
class DFAConfig(BaseModel):
    """📌 Model to configure a Deterministic Finite Automaton (DFA)."""
    states: Set[str]
    input_symbols: Set[str]
    transitions: Dict[str, Dict[str, str]]
    initial_state: str
    final_states: Set[str]
    input: str

@app.post("/dfa/", summary="Process a DFA", description="🔹 Sends a DFA and checks if it accepts the input. Returns processing details and generates a diagram.")
def my_dfa(dfa_config: DFAConfig):
    my_dfa = DFA(
        states=dfa_config.states,
        input_symbols=dfa_config.input_symbols,
        transitions=dfa_config.transitions,
        initial_state=dfa_config.initial_state,
        final_states=dfa_config.final_states
    )

    result = my_dfa.accepts_input(dfa_config.input)

    # Generate and save DFA diagram
    diagram = my_dfa.show_diagram()
    diagram.draw(IMAGE_PATH_DFA, format="png")

    return JSONResponse(content={
        "states": list(dfa_config.states),
        "input_symbols": list(dfa_config.input_symbols),
        "transitions": dfa_config.transitions,
        "initial_state": dfa_config.initial_state,
        "final_states": list(dfa_config.final_states),
        "input": dfa_config.input,
        "accepted": result,
        "diagram_path": "/static/dfa_diagram.png"
    })

# ========================== DPDA ==========================
class DPDAConfig(BaseModel):
    """📌 Model to configure a Deterministic Pushdown Automaton (DPDA)."""
    states: Set[str]
    input_symbols: Set[str]
    stack_symbols: Set[str]
    transitions: Dict[str, Dict[str, Dict[str, list]]]
    initial_state: str
    initial_stack_symbol: str
    final_states: Set[str]
    input: str

@app.post("/dpda/", summary="Process a DPDA", description="🔹 Sends a DPDA and checks if it accepts the input.")
def my_dpda(dpda_config: DPDAConfig):
    my_dpda = DPDA(
        states=dpda_config.states,
        input_symbols=dpda_config.input_symbols,
        stack_symbols=dpda_config.stack_symbols,
        transitions=dpda_config.transitions,
        initial_state=dpda_config.initial_state,
        initial_stack_symbol=dpda_config.initial_stack_symbol,
        final_states=dpda_config.final_states,
        acceptance_mode='final_state'
    )

    result = my_dpda.accepts_input(dpda_config.input)

    # Generate DPDA diagram (optional)
    diagram = my_dpda.show_diagram()
    diagram.draw(IMAGE_PATH_DPDA, format="png")

    return JSONResponse(content={
        "states": list(dpda_config.states),
        "input_symbols": list(dpda_config.input_symbols),
        "stack_symbols": list(dpda_config.stack_symbols),
        "transitions": dpda_config.transitions,
        "initial_state": dpda_config.initial_state,
        "initial_stack_symbol": dpda_config.initial_stack_symbol,
        "final_states": list(dpda_config.final_states),
        "input": dpda_config.input,
        "accepted": result,
        "diagram_path": "/static/dpda_diagram.png"
    })

# ========================== DTM ==========================
class DTMConfig(BaseModel):
    """📌 Model to configure a Deterministic Turing Machine (DTM)."""
    states: Set[str]
    input_symbols: Set[str]
    tape_symbols: Set[str]
    transitions: Dict[str, Dict[str, tuple]]
    initial_state: str
    blank_symbol: str
    final_states: Set[str]
    input: str

@app.post("/dtm/", summary="Process a DTM", description="🔹 Sends a Turing Machine and checks if it accepts the input.")
def my_dtm(dtm_config: DTMConfig):
    my_dtm = DTM(
        states=dtm_config.states,
        input_symbols=dtm_config.input_symbols,
        tape_symbols=dtm_config.tape_symbols,
        transitions=dtm_config.transitions,
        initial_state=dtm_config.initial_state,
        blank_symbol=dtm_config.blank_symbol,
        final_states=dtm_config.final_states
    )

    result = my_dtm.accepts_input(dtm_config.input)

    return JSONResponse(content={
        "states": list(dtm_config.states),
        "input_symbols": list(dtm_config.input_symbols),
        "tape_symbols": list(dtm_config.tape_symbols),
        "transitions": dtm_config.transitions,
        "initial_state": dtm_config.initial_state,
        "blank_symbol": dtm_config.blank_symbol,
        "final_states": list(dtm_config.final_states),
        "input": dtm_config.input,
        "accepted": result
    })
