"""CSV loader module for ExploreJP - ONLY reads CSV files."""

import pandas as pd
from pathlib import Path


def load_cities_from_csv(csv_path: Path | None = None) -> pd.DataFrame:
    """Load cities from CSV file using pandas.
    
    Args:
        csv_path: Path to CSV file. If None, uses default data/cities.csv
    
    Returns:
        DataFrame with city data
    """
    if csv_path is None:
        csv_path = Path(__file__).parent.parent / "data" / "cities.csv"
    
    return pd.read_csv(csv_path)
