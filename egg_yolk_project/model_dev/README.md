# 🥚 Egg Yolk Color Prediction - Model Development (SVR)

This repository contains the complete **Model Development Lifecycle** for predicting egg yolk color scores (DSM Yolk Color Fan 1–15) using Digital Image Processing and Support Vector Regression (SVR).

---

## 📁 Repository Structure

```
├── color_service.py           # Core color extraction & RGB to CIELAB conversion
├── build_features.py          # Batch feature extraction pipeline (generates features.csv)
├── train_compare_models.py    # Stratified 5-Fold Cross-Validation & Benchmark of 5 ML Models
├── train_compare_models.ipynb # Jupyter Notebook with evaluation tables & per-class error breakdown
├── export_best_model.py       # Full-dataset training & production export script
├── model.pkl                  # Serialized SVR (RBF Kernel) pipeline model (39.8 KB)
├── requirements.txt           # Required Python packages
└── data/                      # Dataset tables (features.csv, labels.csv)
```

---

## 📊 Benchmark Evaluation Results (Stratified 5-Fold Cross-Validation)

```
==========================================================================================
MODEL TRAIN vs TEST COMPARISON RESULTS (Stratified 5-Fold Cross-Validation)
==========================================================================================
            Model  Train R2  Test R2  Train MAE  Test MAE  Train RMSE  Test RMSE
 SVR (RBF Kernel)    0.9173   0.9004     0.6233    0.6967      0.8571     0.9393  🏆
Gradient Boosting    0.9612   0.8900     0.4474    0.7206      0.5870     0.9875
    Random Forest    0.9847   0.8853     0.2665    0.7326      0.3693     1.0059
Linear Regression    0.8494   0.8448     0.8916    0.8978      1.1570     1.1729
 Ridge Regression    0.8276   0.8246     0.9788    0.9829      1.2381     1.2477
==========================================================================================

Best Performing Model: SVR (RBF Kernel) (Test R^2 = 0.9004)
```

---

## 🚀 How to Run

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Train & Evaluate Models:**
   ```bash
   python train_compare_models.py
   ```

3. **Export Best Model:**
   ```bash
   python export_best_model.py
   ```
