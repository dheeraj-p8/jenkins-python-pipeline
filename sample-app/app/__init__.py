from flask import Flask
import secrets
import os

def create_app():
    """Application factory pattern with security configurations"""
    app = Flask(__name__)
    
    # Generate a secure random key if not provided in environment
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', secrets.token_hex(32))
    
    # Security headers
    @app.after_request
    def add_security_headers(response):
        # Prevent MIME type sniffing
        response.headers['X-Content-Type-Options'] = 'nosniff'
        # Protect against clickjacking
        response.headers['X-Frame-Options'] = 'DENY'
        # Enable browser XSS protection
        response.headers['X-XSS-Protection'] = '1; mode=block'
        # Enable strict HTTPS
        response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        return response
    
    # Secure session configuration
    app.config.update(
        SESSION_COOKIE_SECURE=True,        # Ensure cookies only sent over HTTPS
        SESSION_COOKIE_HTTPONLY=True,      # Prevent JavaScript access to session cookie
        SESSION_COOKIE_SAMESITE='Lax',     # Protect against CSRF
        PERMANENT_SESSION_LIFETIME=3600,    # Session timeout in seconds (1 hour)
        DEBUG=False,                       # Disable debug mode in production
    )
    
    return app