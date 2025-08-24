# TinyGPT - Proyecto de Preentrenamiento con MoE

Este proyecto implementa una versión minimalista del modelo GPT (Generative Pre-trained Transformer), con el objetivo de experimentar con arquitectura Mixture of Experts (MoE) para reemplazar las capas Feed-Forward tradicionales del Transformer.

## Objetivos principales

1. **Preentrenar un modelo tipo GPT pequeño (`TinyGPT`) desde cero**, utilizando un corpus de texto tokenizado.
2. **Extender la arquitectura para incluir Mixture of Experts (MoE)** en lugar del tradicional bloque FFN (Feed Forward Network).
3. **Comparar comportamiento de inferencia** entre estrategias:
   - Greedy decoding
   - Muestreo con temperatura
   - Muestreo top‑k y top‑p (nucleus sampling)

---

## Estructura del código

- `TinyGPT_es.ipynb`: Notebook principal con explicaciones, entrenamiento y experimentación.
- `trainer_local.py`: Módulo para entrenamiento personalizado.
- `generateV2()`: Función de generación de texto autoregresiva.
- `MoELayer`, `Expert`, `Gate`: Componentes para la arquitectura Mixture of Experts.

---

## Resultados esperados

- Comparación entre un modelo GPT estándar y uno con MoE.
- Análisis del comportamiento de generación con diferentes estrategias de muestreo.
- Exploración de eficiencia y uso de GPU con AMP y MoE.

---

## Autor

Trabajo práctico realizado en el marco de la **Posgrado de Especialización en Inteligencia Artificial (UBA)**.
