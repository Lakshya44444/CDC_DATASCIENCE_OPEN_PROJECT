#  Multimodal Real Estate Valuation Project

This project develops a **multimodal property valuation model** that combines:

-  **tabular housing attributes**
-  **satellite imagery**

to estimate real estate prices.

Tabular data captures measurable property characteristics, while satellite images capture **neighborhood quality** such as:

- greenery
- population density
- accessibility
- nearby development

By **fusing both data types**, the model improves the reliability of automated real-estate valuation systems.

---

##  Repository Structure

```
├── notebook/
│   ├── processed_data/
│   ├── 24410015_final.csv
│   ├── best_multimodal_model.pth
│   ├── best_multimodal_model_finetuned.pth
│   ├── preprocessing.ipynb
│   └── model_training.ipynb
│
├── data_fetcher.py
├── data_fetcher_2.py
├── main.py
├── mapbox_usage_log.json
├── 24410015_report.pdf
├── output.png
├── output_2.png
└── requirements.txt

```

**Note:**  
`24410015_final.csv` is the submission.csv.

---

## 🛠 Installation and Setup

### 1️. Clone the repository

```bash
git clone https://github.com/Lakshya44444/CDC_DATASCIENCE_OPEN_PROJECT.git
cd CDC_DATASCIENCE_OPEN_PROJECT
```

### 2️ Install dependencies

> Python **3.8+ recommended**

```bash
pip install -r requirements.txt
```

### 3️ Add your Mapbox API key

Create a `.env` file in the project root:

```
MAPBOX_ACCESS_TOKEN=your_token_here
```

This is required by `data_fetcher.py` for downloading satellite imagery.

---

##  Usage

###  1. Data Collection (Satellite Images)

```bash
python data_fetcher.py
```

Features:

- automatic logging  
- rate limiting  
- usage tracked in `mapbox_usage_log.json`

---

###  2. Data Preprocessing

Open in Jupyter:

```
notebook/preprocessing.ipynb
```

This notebook performs:

- dataset cleaning  
- feature engineering  
- scaling and transformations  
- saving processed files to `processed_data/`

---

###  3. Model Training

Open:

```
notebook/model_training.ipynb
```

Includes:

- multimodal network architecture  
- stage-1: frozen backbone training  
- stage-2: ResNet fine-tuning  
- evaluation and visualization  

 Pretrained models already included:

- `best_multimodal_model.pth`
- `best_multimodal_model_finetuned.pth`

So **retraining is optional**.

---

##  Results

The model was benchmarked against a **tabular-only baseline**.

| Model | R² Score | Notes |
|------|---------|-------|
| XGBoost (tabular only) | 0.898 | high accuracy on structured features |
| Multimodal network | 0.884 | incorporates visual neighborhood context |

### Key insights learned from imagery

-  greener surroundings → **higher prices**
-  dense concrete regions → **lower prices**
-  accessibility and open areas → **increase valuation**
---

##  Tech Stack

- Python  
- PyTorch  
- scikit-learn  
- XGBoost  
- pandas & numpy  
- Mapbox Static Image API  

---

##  License

This work is part of the **CDC Data Science Open Project**  
and is intended for **educational and research use**.

---

 If you find this project useful, feel free to star the repository!
