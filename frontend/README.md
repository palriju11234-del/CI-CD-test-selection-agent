# QUBIS Website (React + Vite + Tailwind CSS)

This is a modern, high-fidelity React application implementing the QUBIS design.

## Features
- **Hero Section**: Exact 1440×900 desktop composition featuring the human hand, robotic arm, QUBIS robot, and ambient glow, with full responsive adaptations.
- **How It Works**: 5-step automated pipeline process cards with new frosted glassmorphic card design and SVG background.
- **Features**: Split banner layout with 5 distinct feature cards highlighting intelligent test selection capabilities.
- **Documentation**: Onboarding documentation walkthrough with numbered step cards.
- **Login CTA**: Conversion card leading to contact/auth flow.
- **Smooth Navigation**: Desktop and mobile navigation with active section indicator and responsive hamburger menu.

## Tech Stack
- **Framework**: React 18 + Vite
- **Styling**: Tailwind CSS + Custom CSS Design Tokens
- **Typography**: Google Fonts (Inter & Orbitron)

## Getting Started

1. **Start the Python API** from the repository root in a separate terminal:
   ```bash
   python web_api.py
   ```
   The API listens on `http://127.0.0.1:8000` and starts `run_pipeline.py` when the dashboard Run Pipeline button is pressed.

2. **Install Dependencies**:
   ```bash
   cd frontend
   npm install
   ```

3. **Run Development Server**:
   ```bash
   npm run dev
   ```
   Open [http://localhost:3000](http://localhost:3000) in your browser.

4. **Production Build**:
   ```bash
   npm run build
   ```
