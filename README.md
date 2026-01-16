# Triathlon Program Generator

An AI-powered workout program generator for triathlon training using Anthropic's Claude LLM.

## Features

- **Structured Workouts**: Generate detailed swim, bike, and run workouts with intervals and recovery periods
- **Periodization**: Monthly training plans with progressive overload
- **Training Goals**: Customized programs for Sprint, Olympic, Half Ironman, and Full Ironman distances
- **Data Persistence**: Save and track workout history
- **Web Interface**: Easy-to-use web application

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables:
```bash
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
```

4. Run the application:
```bash
python app/main.py
```

5. Open your browser to `http://localhost:8000`

## Usage

1. Navigate to the web interface
2. Select your training goal (distance/race type)
3. Specify your current fitness level and available training hours
4. Generate a personalized workout program
5. View and save your workouts

## API Endpoints

- `POST /api/workouts/generate` - Generate a new workout program
- `GET /api/workouts` - List all saved workouts
- `GET /api/workouts/{id}` - Get a specific workout
- `DELETE /api/workouts/{id}` - Delete a workout

## Deployment

### Deploy to Azure App Services

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions on deploying to Azure.

**Quick deploy:**
```bash
az login
az webapp up --name triathlon-program-generator --runtime "PYTHON:3.11" --sku B1
```

Then set your `ANTHROPIC_API_KEY` in Azure Portal → Configuration → Application Settings.

## License

MIT
