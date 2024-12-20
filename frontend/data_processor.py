import pandas as pd
import pickle
from collections import Counter
from typing import Dict, List, Any

class FashionDataProcessor:
    def __init__(self):
        self.dataset_path = 'c:/Users/k/Desktop/Projects/app/frontend/ai_assistant/fashion_dataset_full.pkl'
        self.df = self._load_dataset()

    def _load_dataset(self) -> pd.DataFrame:
        with open(self.dataset_path, 'rb') as f:
            return pickle.load(f)

    def get_category_stats(self) -> Dict[str, int]:
        """Get count of items in each master category"""
        return self.df['masterCategory'].value_counts().to_dict()

    def get_gender_distribution(self) -> Dict[str, int]:
        """Get distribution of products by gender"""
        return self.df['gender'].value_counts().to_dict()

    def get_top_brands(self, limit: int = 10) -> Dict[str, int]:
        """Get top brands by number of products"""
        return self.df['brand'].value_counts().head(limit).to_dict()

    def get_season_distribution(self) -> Dict[str, int]:
        """Get distribution of products by season"""
        return self.df['season'].value_counts().to_dict()

    def get_products_by_filters(self, filters: Dict[str, Any] = None) -> pd.DataFrame:
        """Get products based on filters"""
        filtered_df = self.df
        if filters:
            for column, value in filters.items():
                if value and column in self.df.columns:
                    filtered_df = filtered_df[filtered_df[column] == value]
        
        return filtered_df[['productDisplayName', 'brand', 'gender', 'masterCategory', 
                          'subCategory', 'baseColour', 'season', 'year', 'image_url']]

    def get_filter_options(self) -> Dict[str, List[str]]:
        """Get all possible values for filter dropdowns"""
        return {
            'gender': sorted(self.df['gender'].unique().tolist()),
            'masterCategory': sorted(self.df['masterCategory'].unique().tolist()),
            'subCategory': sorted(self.df['subCategory'].unique().tolist()),
            'baseColour': sorted(self.df['baseColour'].unique().tolist()),
            'season': sorted(self.df['season'].unique().tolist()),
            'brand': sorted(self.df['brand'].unique().tolist())
        }

    def get_yearly_trends(self) -> Dict[str, int]:
        """Get product count by year"""
        return self.df['year'].value_counts().sort_index().to_dict()

    def get_color_distribution(self) -> Dict[str, int]:
        """Get distribution of products by base color"""
        return self.df['baseColour'].value_counts().to_dict()
