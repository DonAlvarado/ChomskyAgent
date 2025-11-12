# 🧠 **ChomskyAgent – Arquitectura y Contexto del Proyecto**

---

## 📘 **Propósito General**

**ChomskyAgent** es una aplicación web inteligente desarrollada en **Python (Flask)** que analiza y clasifica **gramáticas formales** y **autómatas** dentro de la **Jerarquía de Chomsky (Tipos 0–3)**.  
El sistema combina análisis sintáctico formal, razonamiento simbólico tipo IA, visualización automática de diagramas y generación de reportes.

El objetivo general es crear un **agente explicativo y educativo**, capaz de:
1. Analizar y clasificar automáticamente gramáticas y autómatas.
2. Explicar el razonamiento detrás de la clasificación.
3. Visualizar la información con diagramas dinámicos.
4. Generar reportes PDF completos y ejemplos automáticos.
5. Incluir un modo “Tutor de Chomsky” para práctica interactiva.

---

## ⚙️ **Arquitectura General**

El sistema está dividido en tres capas principales, con comunicación controlada mediante interfaces y APIs REST:

---

##💡 **Resumen de Componentes**
🖥️ 1. Frontend – Interfaz Web

Tecnologías:
TailwindCSS, Alpine.js, GSAP, Jinja2 (para plantillas HTML).

Características:

Pantalla de inicio animada (intro.html) con degradado turquesa.
Dashboard con menú lateral translúcido y secciones:
Analizador de gramáticas
Conversor Regex ⇄ AFD ⇄ Gramática
Chat del agente IA
Generador de ejemplos
Comparador de gramáticas
Generador de reportes PDF
Animaciones suaves con GSAP y hover effects elegantes.

Paleta principal:
#40E0D0 (Turquoise)
#79ECE0 (Light Turquoise)
#B2F7EF (Celeste)
#D1F7F3 (Mint Green)
#EFF7F6 (Mint Cream)