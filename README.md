# AI Fashion Stylist Store

A modern fashion e-commerce platform enhanced with AI-powered styling recommendations, powered by Django and HTMX. This application combines traditional e-commerce functionality with intelligent fashion advice to provide a unique shopping experience.

## Features

### 🤖 AI Fashion Stylist
- Personal styling recommendations based on your preferences and previous purchases
- Real-time outfit comparisons for items in your cart
- Style compatibility analysis
- Personalized fashion advice through an interactive chat interface

### 🛍️ Shopping Experience
- Intuitive product browsing and searching
- Smart filtering and sorting options
- Real-time cart updates using HTMX
- Seamless checkout process

### 💫 Dynamic User Interface
- HTMX-powered interactions for smooth, SPA-like experience
- No page refreshes for common actions
- Responsive design for all devices

## Demo

### Landing Page
./landingpage.mp4

### AI Stylist Interface
./chat.png

## Technology Stack

- **Backend**: Django
- **Frontend Enhancement**: HTMX
- **AI Integration**: Google-Fast-API
- **Authentication**: Django Authentication System

## Installation

1. Clone the repository:
```bash
git clone [https://github.com/Gudguykartik/DeepStyle]
cd [DeepStyle]
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. Run migrations:
```bash
python manage.py migrate
```

6. Start the development server:
```bash
python manage.py runserver
```

## Configuration

The application requires the following environment variables:

```
AI_SERVICE_KEY=your_ai_service_api_key
```

## Usage

1. Register for an account or log in
2. Browse the fashion collection
3. Interact with the AI Stylist for personalized recommendations
4. Add items to cart and use the comparison feature
5. Complete purchase through the secure checkout

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Acknowledgments

- Django community
- HTMX creators
- [Add other acknowledgments]
