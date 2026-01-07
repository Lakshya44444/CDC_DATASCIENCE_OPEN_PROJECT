Multimodal Real Estate Valuation Project
This project develops a multimodal property valuation model that combines tabular housing attributes with satellite imagery to estimate real estate prices. Tabular data captures measurable property characteristics, while satellite images capture neighborhood quality such as greenery, density, accessibility, and nearby development. The model fuses both forms of information to improve the reliability of automated valuation systems.
Repository structure
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
├── output.png
├── output_2.png
└── requirements.txt

The file 24410015_final.csv is the primary dataset used in preprocessing and training.

Installation and setup
Clone the repository:
git clone https://github.com/Lakshya44444/CDC_DATASCIENCE_OPEN_PROJECT.git
cd CDC_DATASCIENCE_OPEN_PROJECT

Install dependencies (Python 3.8 or higher recommended):
pip install -r requirements.txt

Create a .env file in the project root and add your Mapbox API key:
MAPBOX_ACCESS_TOKEN=your_token_here

This is required for data_fetcher.py.

Usage1. Data collection

To download satellite imagery:
python data_fetcher.py

The script supports automatic logging and rate limiting through mapbox_usage_log.json.
2. Data preprocessing
Open and run:
notebook/preprocessing.ipynb

This notebook performs:


dataset cleaning


feature engineering


scaling and transformations


saving processed files to processed_data




          
            
          
        
  
        
    

3. Model training
Open:
notebook/model_training.ipynb

This notebook includes:


multimodal model definition


stage-1 frozen backbone training


stage-2 fine-tuning of ResNet layers


evaluation and visualization


Pretrained model files are already included, so training is optional.

Results
The model was benchmarked against a strong tabular baseline.
ModelR² ScoreNotesXGBoost (tabular only)0.898high accuracy on structured featuresMultimodal network0.884incorporates visual neighborhood context
Important observations learned from images:


greenery correlates with higher prices


dense concrete regions correlate with lower prices


open surroundings and accessibility influence valuations



Tech stack


Python


PyTorch


scikit-learn


XGBoost


pandas and numpy


Mapbox Static Image API



License
This work is part of the CDC Data Science Open Project and is intended for educational and research use.