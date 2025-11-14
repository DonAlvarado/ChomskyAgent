# ChomskyAgent  
Sistema Web para Análisis de Gramáticas, Autómatas y Expresiones Regulares  
Proyecto Final – Lenguajes Formales y Autómatas

---

## 📌 Descripción General

**ChomskyAgent** es una aplicación web modular que integra:

- Análisis automático de **gramáticas** (Clasificación Tipo 0–3).
- Análisis y validación de **autómatas** (AFD / AFN).
- Conversión de **expresiones regulares** a **AFD**.
- Generación de **reportes PDF** con visualizaciones.
- Un **Agente IA interno** capaz de interpretar instrucciones en lenguaje natural.
- Un **Modo Tutor** con preguntas generadas dinámicamente, incluyendo gramáticas  
  de **Tipo 0, Tipo 1, Tipo 2 y Tipo 3**, con distribución probabilística.
- Interfaces gráficas modernas implementadas con **Flask + TailwindCSS**.
- Visualización de autómatas y gramáticas usando **Graphviz**.

El sistema combina un backend robusto, un frontend interactivo y un módulo de IA  
que controla todas las acciones lógicas.

---

# 🧩 Arquitectura General

ChomskyAgent/
│
├── app/
│   ├── Back/
│   │   ├── api/                             # APIs REST para comunicación externa o entre módulos
│   │   │   ├── __init__.py
│   │   │   ├── grammar_api.py               # /api/grammar → analiza, clasifica y devuelve JSON
│   │   │   ├── automata_api.py              # /api/automata → análisis de autómatas
│   │   │   ├── converter_api.py             # /api/converter → regex ⇄ AFD ⇄ gramática
│   │   │   ├── report_api.py                # /api/report → genera PDF o devuelve JSON con metadatos
│   │   │   ├── tutor_api.py                 # /api/tutor → modo quiz, preguntas y respuestas
│   │   │   └── agent_api.py                 # /api/agent → comunicación directa con el agente IA
│   │   │
│   │   ├── front_cntrlls/                   # Rutas que renderizan plantillas HTML
│   │   │   ├── __init__.py
│   │   │   ├── home_routes.py               # / → intro.html
│   │   │   ├── dashboard_routes.py          # /dashboard → menú principal
│   │   │   ├── analyzer_routes.py           # /analyzer → vista HTML del analizador
│   │   │   ├── tutor_routes.py              # /tutor → vista HTML del modo tutor
│   │   │   ├── chat_routes.py               # /chat → vista HTML del chat IA
│   │   │   └── report_routes.py             # /reports → vista HTML de reportes
│   │   │
│   │   ├── interfaces/                      # Interfaces (contratos) entre módulos
│   │   │   ├── __init__.py
│   │   │   ├── IAnalyzer.py
│   │   │   ├── IVisualizer.py
│   │   │   ├── IGenerator.py
│   │   │   └── IAgent.py
│   │   │
│   │   ├── classifier/                      # Núcleo lógico del sistema
│   │   │   ├── __init__.py
│   │   │   ├── grammar_parser.py
│   │   │   ├── automata_parser.py
│   │   │   ├── classifier_engine.py
│   │   │   ├── converter.py
│   │   │   ├── example_generator.py
│   │   │   ├── equivalence_checker.py
│   │   │   ├── explainable_ai.py
│   │   │   ├── visualizer.py
│   │   │   ├── pdf_reporter.py
│   │   │   └── tutor_quiz.py
│   │   │
│   │   ├── utils/
│   │   │   ├── __init__.py
│   │   │   ├── validators.py
│   │   │   ├── file_manager.py
│   │   │   ├── graph_utils.py
│   │   │   ├── logger.py
│   │   │   └── config_loader.py
│   │   │
│   │   └── __init__.py
│   │
│   ├── AI/                                  # Agente inteligente (modo explicativo y tutor)
│   │   ├── __init__.py
│   │   ├── reasoner.py                      # Decide acciones según contexto
│   │   ├── memory.py                        # Guarda sesiones previas del usuario
│   │   ├── trainer.py                       # Entrenamiento opcional (scikit-learn)
│   │   ├── chatbot.py                       # Chat con el agente (modo tutor)
│   │   ├── action_manager.py                # Ejecuta tareas (PDF, ejemplo, explicación)
│   │   ├── nlp_utils.py                     # NLP básico con spaCy y regex
│   │   └── llm_connector.py                 # Integración opcional con Llama / Mistral
│   │
│   ├── Front/
│   │   ├── templates/
│   │   │   ├── intro.html
│   │   │   ├── layout.html
│   │   │   ├── dashboard.html
│   │   │   ├── analyzer.html
│   │   │   ├── tutor.html
│   │   │   ├── chat.html
│   │   │   ├── reports.html
│   │   │   └── about.html
│   │   │
│   │   ├── static/
│   │   │   ├── css/
│   │   │   │   ├── main.css
│   │   │   │   ├── animations.css
│   │   │   │   └── themes.css
│   │   │   ├── js/
│   │   │   │   ├── app.js
│   │   │   │   ├── dashboard.js
│   │   │   │   ├── analyzer.js
│   │   │   │   ├── chat.js
│   │   │   │   └── animations.js
│   │   │   ├── icons/
│   │   │   └── images/
│   │   │
│   │   └── resources/
│   │       ├── examples/
│   │       ├── docs/
│   │       └── config.json
│   │
│   ├── test/
│   │   ├── __init__.py
│   │   ├── test_classifier.py
│   │   ├── test_visualizer.py
│   │   ├── test_agent.py
│   │   ├── test_routes.py
│   │   └── test_api.py
│   │
│   ├── __init__.py
│   └── app.py                               # Configura Flask, registra blueprints y CORS
│
├── run.py
├── requirements.txt
├── tailwind.config.js
├── package.json
├── README.md
└── .gitignore

---

# 🔍 Módulo de IA

El módulo de IA consta de tres archivos principales:

## **1. reasoner.py**
Determina la **intención** del usuario según su mensaje:

- Contiene “→” → analizar gramática  
- Contiene “autómata / automata / afd / afn” → análisis de autómata  
- Contiene “regex / expresión regular” → conversión  
- Contiene “explica” → explicación de gramática  
- Contiene “quiz / pregunta / tutor” → generar ejercicio  
- Contiene “respuesta” → verificar respuesta  
- Contiene “pdf / reporte” → generar PDF  

Luego formatea la respuesta de forma HTML amigable.

---

## **2. action_manager.py**
Orquesta el flujo entre:

- Reasoner  
- extractores  
- APIs REST  
- estado persistente del análisis  

Mantiene:

- `last_rules`
- `last_automaton`
- `last_regex`
- `last_grammar_classification`

Esto permite que comandos como **“Explica la gramática anterior”** o  
**“Genera un PDF”** funcionen.

---

## **3. explainable_ai.py**
Encargado de extraer información desde texto libre:

- Reglas `A -> aB`
- Transiciones `(q0, a)=q1`
- Regex válidas

Además genera la explicación extendida de gramáticas.

---

# 🔬 Módulos de Análisis Formal

## Gramáticas
Usa:

- `grammar_parser.py`
- `classifier_engine.py`
- `GrammarVisualizer`

Clasifica gramáticas en:

- **Tipo 3:** Regulares  
- **Tipo 2:** Libres de contexto  
- **Tipo 1:** Sensibles al contexto  
- **Tipo 0:** Irrestrictas  

---

## Autómatas
Soporta:

- AFD  
- AFN  

El sistema detecta el tipo automáticamente mediante:

- estructura del autómata  
- cardinalidad de transiciones  
- determinismo  

---

## Expresiones Regulares → AFD
Pipeline:

1. Regex → NFA-ε  
2. NFA-ε → AFD  
3. Visualización via Graphviz  
4. Export a PDF

---

# 🧪 Modo Tutor (Versión Extendida)

El Tutor genera **gramáticas aleatorias** usando un generador completo:

### Tipos soportados:
| Tipo | Nombre | Probabilidad |
|------|--------|--------------|
| Tipo 3 | Regular | 30% |
| Tipo 2 | Libre de Contexto | 30% |
| Tipo 1 | Sensible al Contexto | 20% |
| Tipo 0 | Irrestricta | 20% |

El usuario recibe una gramática y debe clasificarla.

**El chequeo de respuestas** compara:

- Respuesta del usuario: `"Tipo X"`
- Tipo real (recortado): `"Tipo X (Nombre)"`

Permitiendo corrección robusta.

---

# 📄 Reportes PDF

Generados por:

- `pdf_reporter.py`
- Visualizadores DOT (grammar/dfa/nfa)

PDFs se guardan en:

Front/static/generated/


Y se listan desde la sección **Reportes**.

Cada PDF incluye:

- metadatos  
- visualización  
- resumen del análisis  

---

# 🌐 Rutas y Blueprints Principales

## Frontend
| Ruta | Blueprint | Descripción |
|------|-----------|-------------|
| `/` | home_bp | Página inicial |
| `/dashboard` | dashboard_bp | Panel principal |
| `/analyzer` | analyzer_bp | Analizador de gramáticas/autómatas |
| `/converter` | converter_routes_bp | Regex → AFD |
| `/compare` | compare_routes_bp | Comparación de gramáticas |
| `/chat` | chat_bp | Chat del agente IA |
| `/tutor` | tutor_bp | Modo Tutor |
| `/reports` | report_pages_bp | Visualización/descarga de PDFs |
| `/about` | about_bp | Página “Acerca de” |

## Backend (API REST)
| Endpoint | Función |
|----------|---------|
| `/api/grammar/analyze` | Analiza y clasifica gramáticas |
| `/api/automata/analyze` | Analiza autómatas |
| `/api/converter/regex2afd` | Regex → AFD |
| `/api/report/generate` | Crea PDFs |
| `/api/tutor/question` | Genera ejercicio |
| `/api/tutor/check` | Evalúa respuesta |
| `/api/agent/chat` | Respuesta del asistente IA |

---

# 🧭 Flujo Completo del Chat

1. Usuario envía mensaje  
2. `reasoner.py` determina la intención  
3. `action_manager.py` ejecuta la acción correcta  
4. Se consulta al backend si es necesario  
5. Se almacena el estado (última gramática/autómata)  
6. El Reasoner devuelve HTML formateado  

Ejemplo:

Usuario: Clasifica S -> aA A -> b
→ Reasoner detecta ANALYZE_GRAMMAR
→ ActionManager extrae reglas
→ API analiza la gramática
→ Reasoner formatea HTML de resultado


---

# 🧪 Pruebas Finales Recomendadas

### 1. Flujo completo:
- Gramática → Explicación  
- Regex → AFD  
- Autómata  
- PDF  
- Tutor → Pregunta → Respuesta  

### 2. Manejo de errores:
- Gramáticas inválidas  
- Regex mal escritas  
- Autómatas sin formato  
- PDF sin análisis previo  

### 3. Persistencia del estado:
- Analizar gramática → Generar PDF  
- Analizar regex → Generar PDF  

### 4. Modo tutor:
- Generar múltiples preguntas  
- Verificar variedad real entre Tipo 0–3  
- Responder correctamente e incorrectamente  

### 5. Navegación:
- Abrir todas las páginas del Front  
- Revisar que no existan 404  
- Verificar /about  

---

# 🛠 Instalación

### Requisitos:
- Python 3.10+
- pip
- virtualenv (opcional)
- Graphviz instalado en el sistema

### Instalación:

```bash
pip install -r requirements.txt

Ejecutar:

python app.py

Luego abrir:
http://127.0.0.1:5000

✔ Estado Final del Proyecto

Chat funcionando

Reasoner robusto

Autómatas, Gramáticas y Regex 100% operativos

PDFs correctos

Carpeta generated funcionando

Tutor FULL (Tipo 0–3 con probabilidades)

Rutas frontend completas

Página /about activa

Navegación estable

No hay 404s innecesarios

Sistema listo para presentación y uso académico

📌 Licencia

Proyecto académico. Uso libre para estudiantes y fines educativos.

👨‍💻 Autor

Desarrollado como proyecto final del curso Lenguajes Formales y Autómatas.
Universidad Rafael Landívar.