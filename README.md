# Nutrition Calculator API

A FastAPI-based application that uses Google's Gemini AI model to analyze food images and provide detailed nutritional information. The API can identify food items in images and calculate their calories, healthiness, and nutrient breakdown.

## Features

- Image-based food recognition
- Calorie calculation for identified food items
- Healthiness assessment
- Detailed nutrient breakdown (carbohydrates, protein, fats, fiber, sugar)
- RESTful API endpoints

## Prerequisites

- Python 3.7+
- Google API Key for Gemini AI
- FastAPI
- Required Python packages (listed in requirements.txt)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd NutritionCalculator
```

2. Install the required packages:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root and add your Google API key:
```
GOOGLE_API_KEY=your_api_key_here
```

## Running the Application

1. Start the FastAPI server:
```bash
uvicorn main:app --reload
```

2. The API will be available at `http://localhost:8000`

## API Endpoints

### GET /
- Welcome message endpoint
- Returns: `{"message": "Welcome to the Nutrition Calculator API!"}`

### POST /calculate-nutrition/
- Analyzes an uploaded food image and returns nutritional information
- Accepts: Image file (JPG, JPEG, or PNG)
- Returns: JSON response with:
  - Total calories
  - List of food items with their calories
  - Healthiness assessment
  - Nutrient breakdown

## Example Response

```json
{
    "total_calories": 500,
    "food_items": [
        {"item": "Chicken Sandwich", "calories": 350},
        {"item": "French Fries", "calories": 150}
    ],
    "healthiness": "Moderately Healthy",
    "nutrient_breakdown": {
        "carbohydrates": "45%",
        "protein": "30%",
        "fats": "25%",
        "fiber": "5g",
        "sugar": "2g"
    }
}
```

## Error Handling

The API includes error handling for:
- Missing image uploads
- Invalid file types
- Processing errors
- JSON parsing errors

## Technologies Used

- FastAPI
- Google Gemini AI
- Python-dotenv
- Uvicorn

## License

MIT License

Copyright (c) 2025 Rohan Darji

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
