"""
Taxeen Website1 - Flask Marketing Site
Landing page for Nigerian Personal Tax SaaS
"""

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'taxeen-marketing-secret')

# Nigerian Naira currency formatting
@app.template_filter('currency')
def currency_format(value):
    if value is None:
        return "₦0"
    try:
        return f"₦{int(value):,}"
    except (ValueError, TypeError):
        return "₦0"

@app.template_filter('number_format')
def number_format(value):
    """Format number with commas"""
    if value is None:
        return "0"
    try:
        return f"{int(value):,}"
    except (ValueError, TypeError):
        return "0"

@app.context_processor
def inject_globals():
    return {
        'current_year': datetime.now().year,
        'app_name': 'Taxeen',
        'app_tagline': 'Nigerian Personal Tax Intelligence'
    }

# ==================== PUBLIC ROUTES ====================

@app.route('/')
def index():
    """Landing page"""
    return render_template('index.html')

@app.route('/features')
def features():
    """Features page"""
    return render_template('features.html')

@app.route('/pricing')
def pricing():
    """Pricing page"""
    plans = [
        {
            'name': 'Basic',
            'price': 2500,
            'period': 'year',
            'features': ['3 Bank Accounts', 'Basic Tax Reports', 'Email Support'],
            'recommended': False
        },
        {
            'name': 'Premium',
            'price': 5000,
            'period': 'year',
            'features': ['Unlimited Banks', 'Full Tax Reports', 'Priority Support', 'Tax Filing'],
            'recommended': True
        },
        {
            'name': 'Enterprise',
            'price': 15000,
            'period': 'year',
            'features': ['Everything in Premium', 'API Access', 'Dedicated Manager', 'Custom Reports'],
            'recommended': False
        }
    ]
    return render_template('pricing.html', plans=plans)

@app.route('/about')
def about():
    """About page"""
    return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    """Contact page"""
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        # In production, send email or save to database
        flash('Thank you for your message! We will get back to you soon.', 'success')
        return redirect(url_for('contact'))
    return render_template('contact.html')

@app.route('/blog')
def blog():
    """Blog page"""
    posts = [
        {'id': 1, 'title': 'Understanding Nigerian Personal Income Tax 2026', 'date': '2026-01-15', 'excerpt': 'Learn about the new tax bands and how they affect you.'},
        {'id': 2, 'title': 'How to Calculate Your Tax Using Bank Statements', 'date': '2026-01-10', 'excerpt': 'A step-by-step guide to tax calculation from your transactions.'},
        {'id': 3, 'title': 'Top 5 Tax Deductions You Should Know About', 'date': '2026-01-05', 'excerpt': 'Maximize your tax savings with these allowable deductions.'},
    ]
    return render_template('blog.html', posts=posts)

@app.route('/faq')
def faq():
    """FAQ page"""
    faqs = [
        {'q': 'What is Taxeen?', 'a': 'Taxeen is a Nigerian personal tax intelligence platform that helps you calculate your income tax using your bank statements.'},
        {'q': 'How does Taxeen work?', 'a': 'Upload your bank statement, we extract your transactions, classify them, and calculate your tax based on Nigerian tax rules.'},
        {'q': 'Is my data secure?', 'a': 'Yes! We use AES-256 encryption for sensitive data, and your bank statements are deleted after processing.'},
        {'q': 'What tax year does Taxeen support?', 'a': 'Taxeen supports the 2026 Nigerian Personal Income Tax rates and rules.'},
        {'q': 'Can I use Taxeen for business taxes?', 'a': 'Taxeen is designed for personal income tax. For business taxes, please consult a tax professional.'},
    ]
    return render_template('faq.html', faqs=faqs)

# ==================== ADMIN ROUTES ====================

@app.route('/admin')
def admin_dashboard():
    """Admin dashboard"""
    stats = {
        'users': 1250,
        'subscribers': 890,
        'revenue': 4450000,
        'reports': 234
    }
    return render_template('admin/dashboard.html', stats=stats)

@app.route('/admin/content')
def admin_content():
    """Admin content management"""
    return render_template('admin/content.html')

# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def not_found(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
