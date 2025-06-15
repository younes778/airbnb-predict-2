import pickle
import numpy as np
import json

class AirbnbPricePredictor:
    def __init__(self):
        with open('airbnb_gbm_model.pkl', 'rb') as f:
          self.model = pickle.load(f)
        with open('airbnb_scaler.pkl', 'rb') as f:
          self.scaler = pickle.load(f)
        
        with open('model_metadata.json', 'r') as f:
            metadata = json.load(f)
        
        self.feature_names = metadata['feature_names']
        self.numerical_features = metadata['numerical_features']
        self.category_mappings = metadata['category_mappings']
        self.default_values = metadata['default_values']
    
    def predict_price(self, 
                     latitude, 
                     longitude, 
                     neighbourhood_group, 
                     room_type,
                     neighbourhood=None,
                     minimum_nights=None,
                     number_of_reviews=None,
                     reviews_per_month=None,
                     calculated_host_listings_count=None,
                     availability_365=None):
        """
        Predict Airbnb price with minimal required parameters.
        
        Required parameters:
        - latitude: Property latitude
        - longitude: Property longitude  
        - neighbourhood_group: One of the borough names
        - room_type: Type of room (e.g., 'Entire home/apt', 'Private room', 'Shared room')
        
        Optional parameters (will use defaults if not provided):
        - neighbourhood: Specific neighborhood name
        - minimum_nights: Minimum nights required
        - number_of_reviews: Total number of reviews
        - reviews_per_month: Average reviews per month
        - calculated_host_listings_count: Number of listings by host
        - availability_365: Days available per year
        """
        
        # Use defaults for optional parameters
        if minimum_nights is None:
            minimum_nights = self.default_values['minimum_nights']
        if number_of_reviews is None:
            number_of_reviews = self.default_values['number_of_reviews']
        if reviews_per_month is None:
            reviews_per_month = self.default_values['reviews_per_month']
        if calculated_host_listings_count is None:
            calculated_host_listings_count = self.default_values['calculated_host_listings_count']
        if availability_365 is None:
            availability_365 = self.default_values['availability_365']
        
        # Create feature vector
        features = {}
        
        # Numerical features
        features['latitude'] = latitude
        features['longitude'] = longitude
        features['minimum_nights'] = minimum_nights
        features['number_of_reviews'] = number_of_reviews
        features['reviews_per_month'] = reviews_per_month
        features['calculated_host_listings_count'] = calculated_host_listings_count
        features['availability_365'] = availability_365
        
        # Engineered features
        features['NEW_availability_ratio'] = availability_365 / 365
        features['NEW_daily_average_reviews'] = reviews_per_month / 30
        features['NEW_annual_income'] = self.default_values['NEW_annual_income']
        if reviews_per_month > 0:
            features['NEW_average_stay_duration'] = number_of_reviews / reviews_per_month
        else:
            features['NEW_average_stay_duration'] = 0
        features['NEW_house_occupancy_rate'] = 365 - availability_365
        features['NEW_income'] = self.default_values['NEW_income']
        
        # One-hot encode categorical variables
        # Initialize all categorical features to 0
        for feature_name in self.feature_names:
            if feature_name.startswith(('ng_', 'rt_', 'n_')):
                features[feature_name] = 0
        
        # Set neighbourhood_group
        ng_feature = f"ng_{neighbourhood_group}"
        if ng_feature in features:
            features[ng_feature] = 1
        
        # Set room_type  
        rt_feature = f"rt_{room_type}"
        if rt_feature in features:
            features[rt_feature] = 1
        
        # Set neighbourhood if provided
        if neighbourhood:
            n_feature = f"n_{neighbourhood}"
            if n_feature in features:
                features[n_feature] = 1
        
        # Create feature array in correct order
        feature_array = np.array([features.get(name, 0) for name in self.feature_names]).reshape(1, -1)
        
        # Scale numerical features
        numerical_indices = [self.feature_names.index(col) for col in self.numerical_features if col in self.feature_names]
        feature_array[:, numerical_indices] = self.scaler.transform(feature_array[:, numerical_indices])
        
        # Make prediction
        log_price = self.model.predict(feature_array)[0]
        price = np.expm1(log_price)  # Reverse log transform
        
        return round(price, 2)
# Example usage
if __name__ == "__main__":
    # Initialize predictor
    predictor = AirbnbPricePredictor()
    
    # Test prediction with minimal parameters
    predicted_price = predictor.predict_price(
        latitude=40.7589,
        longitude=-73.9851,
        neighbourhood_group="Manhattan",
        room_type="Entire home/apt"
    )
    
    print(f"Predicted price: ${predicted_price}")