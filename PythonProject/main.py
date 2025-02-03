"""
Automatos API - Implementação de autômatos com FastAPI

📌 Esta API processa três tipos de autômatos:
1️⃣ DFA (Deterministic Finite Automaton)
2️⃣ DPDA (Deterministic Pushdown Automaton)
3️⃣ DTM (Deterministic Turing Machine)

🔹 Funcionalidades:
- Enviar configurações via JSON.
- Verificar se a entrada é aceita pelo autômato.
- Gerar e visualizar o diagrama do autômato.

🔹 Endpoints:
- `/dfa/`  → Processa um DFA e retorna se aceita a entrada e gera o diagrama.
- `/dpda/` → Processa um DPDA e verifica se aceita a entrada.
- `/dtm/`  → Processa uma Máquina de Turing Determinística (DTM).

🔹 Documentação automática:
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

# Instância do FastAPI
app = FastAPI(
    title="Automatos API",
    description="API para simulação de autômatos (DFA, DPDA, DTM) com geração de diagramas.",
    version="1.0.0"
)

# Diretório de arquivos estáticos
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
os.makedirs(STATIC_DIR, exist_ok=True)

# Caminhos das imagens geradas
IMAGE_PATH_DFA = os.path.join(STATIC_DIR, "dfa_diagram.png")
IMAGE_PATH_DPDA = os.path.join(STATIC_DIR, "dpda_diagram.png")

# Servindo arquivos estáticos
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


### 📌 SERVIR O HTML DA INTERFACE
@app.get("/", response_class=FileResponse, summary="Servir a interface web")
async def serve_ui():
    """📜 Servir a interface HTML da API na raiz `/`."""
    return os.path.join(STATIC_DIR, "index.html")


# ========================== DFA ==========================
class DFAConfig(BaseModel):
    """📌 Modelo para configurar um Autômato Finito Determinístico (DFA)."""
    states: Set[str]
    input_symbols: Set[str]
    transitions: Dict[str, Dict[str, str]]
    initial_state: str
    final_states: Set[str]
    input: str

@app.post("/dfa/", summary="Processar um DFA", description="🔹 Envia um DFA e verifica se aceita a entrada. Retorna os detalhes do processamento e gera um diagrama.")
def my_dfa(dfa_config: DFAConfig):
    my_dfa = DFA(
        states=dfa_config.states,
        input_symbols=dfa_config.input_symbols,
        transitions=dfa_config.transitions,
        initial_state=dfa_config.initial_state,
        final_states=dfa_config.final_states
    )

    result = my_dfa.accepts_input(dfa_config.input)

    # Gera o diagrama do DFA e salva
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
    """📌 Modelo para configurar um Autômato com Pilha Determinístico (DPDA)."""
    states: Set[str]
    input_symbols: Set[str]
    stack_symbols: Set[str]
    transitions: Dict[str, Dict[str, Dict[str, list]]]
    initial_state: str
    initial_stack_symbol: str
    final_states: Set[str]
    input: str

@app.post("/dpda/", summary="Processar um DPDA", description="🔹 Envia um DPDA e verifica se aceita a entrada.")
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

    # Gera o diagrama do DPDA (opcional)
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
    """📌 Modelo para configurar uma Máquina de Turing Determinística (DTM)."""
    states: Set[str]
    input_symbols: Set[str]
    tape_symbols: Set[str]
    transitions: Dict[str, Dict[str, tuple]]
    initial_state: str
    blank_symbol: str
    final_states: Set[str]
    input: str

@app.post("/dtm/", summary="Processar uma DTM", description="🔹 Envia uma Máquina de Turing e verifica se aceita a entrada.")
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
