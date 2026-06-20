import pandas as pd
import numpy as np


def process_crop_csv(filepath, user_id):
    try:
        if filepath.endswith('.csv'):
            df = pd.read_csv(filepath)
        else:
            df = pd.read_excel(filepath)

        df.columns = [c.strip().lower().replace(' ', '_') for c in df.columns]

        col_map = {
            'state_name': 'state', 'district_name': 'district',
            'crop_year': 'crop_year', 'season': 'season',
            'crop': 'crop', 'area': 'area', 'production': 'production'
        }
        df.rename(columns=col_map, inplace=True)

        required = ['state', 'district', 'crop_year', 'season', 'crop', 'area']
        missing = [c for c in required if c not in df.columns]
        if missing:
            return {'success': False, 'error': f"Missing columns: {missing}"}

        df.dropna(subset=['state', 'district', 'crop', 'area'], inplace=True)
        df['production'] = pd.to_numeric(df['production'], errors='coerce').fillna(0)
        df['area'] = pd.to_numeric(df['area'], errors='coerce')
        df.dropna(subset=['area'], inplace=True)
        df = df[df['area'] > 0]

        df['yield_per_hectare'] = df['production'] / df['area']

        for col in ['state', 'district', 'season', 'crop']:
            df[col] = df[col].astype(str).str.strip().str.title()

        # Cap at 10,000 rows — enough for ML training, fast to insert
        df = df.head(10000)

        from extensions import db
        from models import CropData

        # Bulk insert using list of dicts (much faster than row-by-row)
        records = [
            CropData(
                user_id=user_id,
                state=str(row['state']),
                district=str(row['district']),
                crop_year=int(row['crop_year']),
                season=str(row['season']),
                crop=str(row['crop']),
                area=float(row['area']),
                production=float(row['production']),
                yield_per_hectare=float(row['yield_per_hectare'])
            )
            for _, row in df.iterrows()
        ]

        # Insert in batches of 500
        batch_size = 500
        for i in range(0, len(records), batch_size):
            db.session.bulk_save_objects(records[i:i+batch_size])
            db.session.commit()

        return {'success': True, 'rows_inserted': len(records)}

    except Exception as e:
        db.session.rollback()
        return {'success': False, 'error': str(e)}
