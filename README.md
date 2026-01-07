🏡 Multimodal AI for Real Estate Valuation

Bridging the "Condition Gap" by fusing satellite imagery with financial data to predict property prices.

(Above: Grad-CAM visualization showing the model identifying high-value features like greenery vs. low-value density.)

📖 Overview

Real estate valuation typically relies on tabular data (square footage, bedrooms, year built). However, this ignores the visual context—curb appeal, privacy, and neighborhood density—that heavily influences market value.

This project implements a Two-Stream Late Fusion Neural Network that processes:

Structured Data: 26 engineered financial features (e.g., Wealth Maps, Cyclical Time).

Unstructured Data: High-resolution RGB satellite imagery ($224 \times 224$ pixels).

The result is a robust valuation model ($R^2 \approx 0.88$) that not only predicts price but visually explains its decisions using Gradient-weighted Class Activation Mapping (Grad-CAM).

🚀 Key Features

Multimodal Architecture: Combines a ResNet18 CNN (Visual Stream) with a deep Multi-Layer Perceptron (Tabular Stream).

Late Fusion: Modalities are processed independently and fused at the penultimate layer for optimal weight balancing.

Advanced Feature Engineering: * Spatial: K-Means Micro-Clustering & Target-Encoded Zip Wealth.

Temporal: Cyclical Sine/Cosine encoding for seasonality ("The Spring Rush").

Interaction: Polynomial features capturing Quality $\times$ Size dynamics.

Explainable AI (XAI): Integrated SHAP for tabular feature importance and Grad-CAM for visual attention mapping.

Automated Pipeline: Scripts for programmatic image acquisition (Mapbox API), outlier removal, and log-normal target transformation.

📊 Performance Results

We benchmarked the Multimodal Network against a state-of-the-art XGBoost ensemble.

Model Architecture

Features Used

RMSE (Log)

$R^2$ Score

XGBoost (Baseline)

26 Tabular Features

0.165

0.9015

Multimodal NN (Fusion)

Tabular + Satellite

0.171

0.8835

Insight: While the tabular data is the dominant predictor ($90\%$ of variance), the Neural Network successfully integrated the visual signal. The Grad-CAM analysis confirmed the model learned to associate tree canopies and privacy with wealth and impervious surfaces (concrete) with lower value, providing interpretability that XGBoost lacks.

🛠️ Project Structure

├── 📁 processed_data/       # Cleaned CSVs and Scaler artifacts
│   ├── train_final.csv
│   ├── test_final.csv
│   └── scaler.pkl
├── 📁 images_mapbox_zoom18/ # Satellite imagery folder
├── 📁 report_images/        # EDA & Result visualizations
├── 📄 preprocessing.ipynb   # Data cleaning, Feature Eng., & EDA
├── 📄 training.ipynb        # Model training loop (PyTorch)
├── 📄 inference.py          # Generates submission_final.csv
├── 📄 gradcam.py            # Generates Explainability Heatmaps
├── 📄 ma.py                 # Mapbox Image Downloader Script
└── 📄 README.md             # Project Documentation


💻 Installation & Usage

1. Prerequisites

Python 3.8+

PyTorch (CUDA recommended for training)

Mapbox API Key (for image downloading)

2. Setup Environment

# Clone repository
git clone [https://github.com/yourusername/multimodal-real-estate.git](https://github.com/yourusername/multimodal-real-estate.git)
cd multimodal-real-estate

# Install dependencies
pip install pandas numpy scikit-learn matplotlib seaborn torch torchvision tqdm pillow python-dotenv shap opencv-python


3. Run the Pipeline

Step A: Download Images
Create a .env file with MAPBOX_TOKEN=your_token_here and run:

python ma.py


Step B: Preprocessing
Run preprocessing.ipynb to clean data, engineer features, and generate train_final.csv.

Step C: Train Model
Run training.ipynb. This will save the best weights to best_multimodal_model_finetuned.pth.

Step D: Inference & Submission

python inference.py


Output: submission_final.csv

📈 Visual Insights (EDA)

1. The "Spring Rush" (Seasonality):
Sales volume peaks significantly between April and August.

2. Geospatial Wealth Distribution:
Clustering analysis reveals distinct high-value pockets (Red) vs. industrial zones (Blue).

🧠 Model Interpretability

SHAP Analysis (Tabular):
The model identified zip_wealth (Location) and grade (Quality) as the top two drivers of price, confirming real estate domain knowledge.

Grad-CAM (Visual):
The model's visual attention (Red Hotspots) correlates strongly with private structures and greenery.

📜 License

This project is licensed under the MIT License.

Author: Lakshya Gupta

Date: January 7, 2026
