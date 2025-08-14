# IBGE Trabalhe Conosco - Portal Gov.br

## Overview
This project implements a comprehensive enrollment and simplified selection process system for employees of the Brazilian Institute of Geography and Statistics (IBGE), integrated with the Brazilian government's "Trabalhe Conosco" portal. The system handles multi-stage registrations, CPF validation via external API, PIX payments, and psychometric exam scheduling, all within a responsive interface designed with government standards. The business vision is to streamline the recruitment process for public sector roles, ensuring efficiency and transparency, with high market potential for broader government application.

## User Preferences
The user prefers a clear and objective communication style. They want to be informed about changes and progress regularly. For development, an iterative approach is preferred, with clear explanations for any significant technical decisions or architectural choices. The user wants to ensure the project adheres to the specified design and functional requirements without deviations.

## System Architecture
The application follows a client-server architecture. The backend is developed using Flask (Python), handling API integrations, data processing, and database interactions. The frontend is built with HTML5, CSS3, and Tailwind CSS, ensuring a responsive and modern user experience. The UI/UX design adheres to the official Brazilian government visual identity, incorporating elements like the national emblem and standard governmental templates. Core technical implementations include a multi-step enrollment flow, real-time CPF validation, and integration with payment gateways for PIX transactions. The system's design prioritizes security, data integrity (with LGPD compliance popups), and user-friendly navigation with visual progress indicators. PostgreSQL is used as the relational database.

## External Dependencies
The project integrates with the following external services:
- **VEXY PAYMENTS API**: For processing PIX payments, including token authentication, PIX generation, and payment verification.
- **CPF Validation API**: `https://consulta.fontesderenda.blog` for real-time CPF validation.
- **ViaCEP**: For address lookup and validation (although not explicitly detailed in functionality, it's a standard Brazilian integration).