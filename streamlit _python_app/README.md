# Dynamic Streamlit Mental-Health Guardrail Lab

## Run
```bash
pip install -r requirements.txt
streamlit run app_v14_1.py
```

## What's new
This version is intentionally more interactive and dynamic:
- live message assessment
- adjustable risk thresholds
- dynamic risk gauge
- evidence/pattern inspection
- baseline vs guarded response cards
- session assessment history
- live dashboard metrics and charts
- architecture walkthrough slider
- interactive CSV EDA
- interactive metric/confusion-matrix lab
- thesis/viva presentation mode
- JSON and CSV export

## Model note
The default scorer is a transparent demonstration implementation so the app can run immediately.
For final thesis experiments, replace `demo_classifier_score()` with your trained RoBERTa inference
and connect the Qwen generation code from the notebook.

This is not a clinical or emergency service.
