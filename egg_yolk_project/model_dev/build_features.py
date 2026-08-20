"""
Build Features Script
Scans dataset images from pic_egg_yolk (class4..class15),
copies/organizes them into data/raw_images,
generates labels.csv and extracts color features into data/features.csv.
"""

import os
import shutil
import pandas as pd
from color_service import extract_color_features


def build_dataset_and_features():
    # Source dataset path
    source_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'pic_egg_yolk'))
    
    # Destination directories
    base_dev_dir = os.path.dirname(__file__)
    data_dir = os.path.join(base_dev_dir, 'data')
    raw_images_dir = os.path.join(data_dir, 'raw_images')
    
    os.makedirs(raw_images_dir, exist_ok=True)

    labels_data = []
    features_data = []

    print(f"Scanning images from: {source_dir}")
    
    # Identify class folders
    if not os.path.exists(source_dir):
        print(f"Warning: Source directory '{source_dir}' not found. Checking raw_images directory instead.")
        source_dir = raw_images_dir

    class_folders = sorted(
        [d for d in os.listdir(source_dir) if d.startswith('class') and os.path.isdir(os.path.join(source_dir, d))],
        key=lambda x: int(x.replace('class', ''))
    )

    total_images = 0

    for class_folder in class_folders:
        fan_score = int(class_folder.replace('class', ''))
        folder_path = os.path.join(source_dir, class_folder)
        image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]

        for img_name in image_files:
            src_img_path = os.path.join(folder_path, img_name)
            
            # Destination image path inside raw_images
            dest_filename = f"class{fan_score}_{img_name}"
            dest_img_path = os.path.join(raw_images_dir, dest_filename)
            
            # Copy to raw_images if not already present
            if not os.path.exists(dest_img_path):
                shutil.copy2(src_img_path, dest_img_path)

            # Record label
            labels_data.append({
                'image_filename': dest_filename,
                'original_class': class_folder,
                'fan_score': fan_score
            })

            # Extract color features
            features = extract_color_features(dest_img_path)
            features_data.append({
                'image_filename': dest_filename,
                'fan_score': fan_score,
                'r': features['r'],
                'g': features['g'],
                'b': features['b'],
                'l': features['l'],
                'a': features['a'],
                'b_lab': features['b_lab']
            })

            total_images += 1

    print(f"Processed total {total_images} images across {len(class_folders)} classes.")

    # Save labels.csv
    labels_df = pd.DataFrame(labels_data)
    labels_csv_path = os.path.join(data_dir, 'labels.csv')
    labels_df.to_csv(labels_csv_path, index=False)
    print(f"Saved labels to: {labels_csv_path}")

    # Save features.csv
    features_df = pd.DataFrame(features_data)
    features_csv_path = os.path.join(data_dir, 'features.csv')
    features_df.to_csv(features_csv_path, index=False)
    print(f"Saved features to: {features_csv_path}")

    print("\nDataset summary:")
    print(features_df['fan_score'].value_counts().sort_index())
    
    return features_df


if __name__ == '__main__':
    build_dataset_and_features()
