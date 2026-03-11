"""
Taxeen Frontend1 - Flask Application
Nigerian Personal Tax Intelligence Platform Dashboard
"""

from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from functools import wraps
import requests
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'taxeen-secret-key-change-in-production')
app.config['API_BASE_URL'] = os.getenv('API_BASE_URL', 'http://localhost:8000/api')

# Nigerian Naira currency formatting
@app.template_filter('currency')
def currency_format(value):
    """Format value as Nigerian Naira"""
    if value is None:
        return "₦0.00"
    try:
        return f"₦{float(value):,.2f}"
    except (ValueError, TypeError):
        return "₦0.00"

@app.template_filter('date_format')
def date_format(value):
    """Format date for display"""
    if value is None:
        return ""
    try:
        if isinstance(value, str):
            value = datetime.fromisoformat(value.replace('Z', '+00:00'))
        return value.strftime('%d %b %Y')
    except (ValueError, TypeError):
        return str(value)

@app.template_filter('datetime_format')
def datetime_format(value):
    """Format datetime for display"""
    if value is None:
        return ""
    try:
        if isinstance(value, str):
            value = datetime.fromisoformat(value.replace('Z', '+00:00'))
        return value.strftime('%d %b %Y %H:%M')
    except (ValueError, TypeError):
        return str(value)

@app.template_filter('number_format')
def number_format(value):
    """Format number with commas"""
    if value is None:
        return "0"
    try:
        return f"{int(value):,}"
    except (ValueError, TypeError):
        return "0"

# API helper functions
def api_call(endpoint, method='GET', data=None, token=None):
    """Make API call to backend"""
    url = f"{app.config['API_BASE_URL']}{endpoint}"
    headers = {'Content-Type': 'application/json'}
    if token:
        headers['Authorization'] = f'Bearer {token}'
    
    try:
        if method == 'GET':
            response = requests.get(url, headers=headers, timeout=10)
        elif method == 'POST':
            response = requests.post(url, json=data, headers=headers, timeout=10)
        elif method == 'PUT':
            response = requests.put(url, json=data, headers=headers, timeout=10)
        elif method == 'DELETE':
            response = requests.delete(url, headers=headers, timeout=10)
        else:
            return None
        
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 401:
            return {'error': 'Unauthorized', 'status_code': 401}
        else:
            return {'error': response.text, 'status_code': response.status_code}
    except requests.exceptions.ConnectionError:
        return {'error': 'Cannot connect to API server', 'status_code': 503}
    except requests.exceptions.Timeout:
        return {'error': 'API request timed out', 'status_code': 504}
    except Exception as e:
        return {'error': str(e), 'status_code': 500}

# Mock data for development
MOCK_USER = {
    'id': 1,
    'email': 'demo@taxeen.ng',
    'first_name': 'Chinedu',
    'last_name': 'Okafor',
    'phone': '+2348012345678',
    'subscription_plan': 'premium',
    'subscription_status': 'active',
    'is_admin': False
}

MOCK_BANKS = [
    {
        'id': 1,
        'bank_name': 'Guaranty Trust Bank',
        'account_number': '****1234',
        'account_name': 'CHINEDU OKAFOR',
        'account_type': 'Savings',
        'current_balance': 2450000.00,
        'is_active': True,
        'last_sync': '2026-01-15T10:30:00'
    },
    {
        'id': 2,
        'bank_name': 'Access Bank',
        'account_number': '****5678',
        'account_name': 'CHINEDU OKAFOR',
        'account_type': 'Current',
        'current_balance': 890000.00,
        'is_active': True,
        'last_sync': '2026-01-15T09:00:00'
    },
    {
        'id': 3,
        'bank_name': 'United Bank for Africa',
        'account_number': '****9012',
        'account_name': 'CHINEDU OKAFOR',
        'account_type': 'Savings',
        'current_balance': 125000.00,
        'is_active': True,
        'last_sync': '2026-01-14T16:45:00'
    }
]

MOCK_TRANSACTIONS = []
# Generate mock transactions
for i in range(50):
    date = datetime(2026, 1, 1) - timedelta(days=i)
    is_credit = i % 3 == 0
    amount = (5000 + (i * 1000)) if is_credit else (2000 + (i * 500))
    MOCK_TRANSACTIONS.append({
        'id': i + 1,
        'transaction_date': date.isoformat(),
        'transaction_type': 'credit' if is_credit else 'debit',
        'amount': amount,
        'description': f"{'Salary Payment' if is_credit else 'POS Purchase'} - {date.strftime('%d %b')}",
        'category': 'salary' if is_credit else 'shopping',
        'counterparty_name': 'ABC Company Ltd' if is_credit else 'Shoprite Stores',
        'is_internal_transfer': i % 10 == 5,
        'is_taxable': True,
        'is_deductible': not is_credit,
        'balance': 2450000 - (i * 5000),
        'bank_account_id': 1
    })

MOCK_UPLOADS = [
    {
        'id': 1,
        'filename': 'GTBank_Statement_Dec2025.pdf',
        'bank_name': 'Guaranty Trust Bank',
        'date_range': 'Dec 2025',
        'transactions_count': 45,
        'status': 'processed',
        'uploaded_at': '2026-01-10T14:30:00'
    },
    {
        'id': 2,
        'filename': 'AccessBank_Statement_Nov2025.pdf',
        'bank_name': 'Access Bank',
        'date_range': 'Nov 2025',
        'transactions_count': 32,
        'status': 'processed',
        'uploaded_at': '2026-01-05T09:15:00'
    }
]

MOCK_TAX_REPORT = {
    'tax_year': 2025,
    'gross_income': 8500000.00,
    'taxable_income': 7650000.00,
    'total_deductions': 850000.00,
    'tax_payable': 1227500.00,
    'effective_rate': 14.44,
    'breakdown': [
        {'band': 'First ₦300,000', 'rate': '7%', 'tax': 21000.00},
        {'band': 'Next ₦300,000', 'rate': '11%', 'tax': 33000.00},
        {'band': 'Next ₦500,000', 'rate': '15%', 'tax': 75000.00},
        {'band': 'Next ₦500,000', 'rate': '19%', 'tax': 95000.00},
        {'band': 'Next ₦1,600,000', 'rate': '21%', 'tax': 336000.00},
        {'band': 'Above ₦3,200,000', 'rate': '24%', 'tax': 1068000.00}
    ]
}

MOCK_ADMIN_USERS = [
    {'id': 1, 'email': 'admin@taxeen.ng', 'name': 'Admin User', 'plan': 'enterprise', 'status': 'active', 'transactions': 1250},
    {'id': 2, 'email': 'demo@taxeen.ng', 'name': 'Chinedu Okafor', 'plan': 'premium', 'status': 'active', 'transactions': 156},
    {'id': 3, 'email': 'user3@example.com', 'name': 'Amina Yusuf', 'plan': 'basic', 'status': 'active', 'transactions': 45},
    {'id': 4, 'email': 'user4@example.com', 'name': 'Emeka Eze', 'plan': 'free', 'status': 'inactive', 'transactions': 0},
]

# Authentication decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('login'))
        if not session.get('user', {}).get('is_admin', False):
            flash('Admin access required.', 'error')
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated_function

# Context processor for template variables
@app.context_processor
def inject_globals():
    return {
        'current_year': datetime.now().year,
        'app_name': 'Taxeen',
        'app_tagline': 'Nigerian Personal Tax Intelligence'
    }

# ==================== AUTH ROUTES ====================

@app.route('/')
def index():
    """Landing page - redirect to dashboard if logged in"""
    if 'user' in session:
        return redirect(url_for('dashboard'))
    return render_template('auth/login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page"""
    if 'user' in session:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Try API call
        result = api_call('/auth/login', 'POST', {'email': email, 'password': password})
        
        if 'error' in result:
            # Use mock for development
            if email == 'demo@taxeen.ng' and password == 'demo123':
                session['user'] = MOCK_USER
                session['token'] = 'mock-jwt-token'
                flash('Welcome back!', 'success')
                return redirect(url_for('dashboard'))
            flash('Invalid email or password', 'error')
        else:
            session['user'] = result.get('user', MOCK_USER)
            session['token'] = result.get('access_token')
            flash('Welcome back!', 'success')
            return redirect(url_for('dashboard'))
    
    return render_template('auth/login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Registration page"""
    if 'user' in session:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        data = {
            'email': request.form.get('email'),
            'password': request.form.get('password'),
            'first_name': request.form.get('first_name'),
            'last_name': request.form.get('last_name'),
            'phone': request.form.get('phone')
        }
        
        result = api_call('/auth/register', 'POST', data)
        
        if 'error' in result:
            # Mock success for development
            session['pending_user'] = data
            flash('Registration successful! Please choose a subscription plan.', 'success')
            return redirect(url_for('payment'))
        else:
            session['pending_user'] = result.get('user', data)
            flash('Registration successful! Please choose a subscription plan.', 'success')
            return redirect(url_for('payment'))
    
    return render_template('auth/register.html')

@app.route('/payment', methods=['GET', 'POST'])
def payment():
    """Subscription payment page"""
    if request.method == 'POST':
        plan = request.form.get('plan', 'basic')
        # Mock payment processing
        session['user'] = session.get('pending_user', MOCK_USER)
        session['user']['subscription_plan'] = plan
        session['user']['subscription_status'] = 'active'
        session.pop('pending_user', None)
        flash('Payment successful! Welcome to Taxeen.', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('auth/payment.html')

@app.route('/logout')
def logout():
    """Logout user"""
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

# ==================== DASHBOARD ROUTES ====================

@app.route('/dashboard')
@login_required
def dashboard():
    """Main dashboard"""
    user = session.get('user', MOCK_USER)
    banks = MOCK_BANKS
    transactions = MOCK_TRANSACTIONS[:10]
    
    # Calculate summary
    total_income = sum(t['amount'] for t in MOCK_TRANSACTIONS if t['transaction_type'] == 'credit')
    total_expenses = sum(t['amount'] for t in MOCK_TRANSACTIONS if t['transaction_type'] == 'debit')
    total_balance = sum(b['current_balance'] for b in banks)
    
    # Monthly data for charts
    monthly_data = [
        {'month': 'Jul', 'income': 720000, 'expense': 450000},
        {'month': 'Aug', 'income': 680000, 'expense': 520000},
        {'month': 'Sep', 'income': 850000, 'expense': 480000},
        {'month': 'Oct', 'income': 920000, 'expense': 560000},
        {'month': 'Nov', 'income': 780000, 'expense': 490000},
        {'month': 'Dec', 'income': 1100000, 'expense': 720000},
    ]
    
    # Category breakdown
    category_data = [
        {'name': 'Salary', 'value': 6500000, 'color': '#10B981'},
        {'name': 'Business', 'value': 1200000, 'color': '#3B82F6'},
        {'name': 'Investment', 'value': 500000, 'color': '#8B5CF6'},
        {'name': 'Other', 'value': 300000, 'color': '#F59E0B'},
    ]
    
    return render_template('dashboard/index.html',
                         user=user,
                         banks=banks,
                         transactions=transactions,
                         total_income=total_income,
                         total_expenses=total_expenses,
                         total_balance=total_balance,
                         monthly_data=monthly_data,
                         category_data=category_data)

# ==================== BANK ACCOUNTS ROUTES ====================

@app.route('/banks')
@login_required
def banks_list():
    """List all bank accounts"""
    result = api_call('/bank-accounts', token=session.get('token'))
    
    if 'error' in result:
        banks = MOCK_BANKS
    else:
        banks = result
    
    return render_template('banks/list.html', banks=banks)

@app.route('/banks/add', methods=['GET', 'POST'])
@login_required
def add_bank():
    """Add new bank account"""
    if request.method == 'POST':
        data = {
            'bank_name': request.form.get('bank_name'),
            'account_number': request.form.get('account_number'),
            'account_name': request.form.get('account_name'),
            'account_type': request.form.get('account_type'),
        }
        
        result = api_call('/bank-accounts', 'POST', data, token=session.get('token'))
        
        if 'error' in result:
            flash('Bank account added successfully!', 'success')
        else:
            flash('Bank account added successfully!', 'success')
        return redirect(url_for('banks_list'))
    
    # Nigerian banks list
    banks = [
        ('Access Bank', '044'),
        ('First Bank of Nigeria', '011'),
        ('Guaranty Trust Bank', '058'),
        ('United Bank for Africa', '033'),
        ('Zenith Bank', '057'),
        ('Stanbic IBTC Bank', '039'),
        ('Fidelity Bank', '070'),
        ('Union Bank of Nigeria', '032'),
        ('Ecobank Nigeria', '050'),
        ('Wema Bank', '035'),
        ('Sterling Bank', '232'),
        ('First City Monument Bank', '214'),
        ('Providus Bank', '101'),
        ('Kuda Bank', '090'),
        ('OPay', '999'),
        ('Moniepoint MFB', '100'),
        ('PalmPay', '9999'),
    ]
    
    return render_template('banks/add.html', banks=banks)

@app.route('/banks/<int:bank_id>')
@login_required
def bank_detail(bank_id):
    """View bank account details"""
    result = api_call(f'/bank-accounts/{bank_id}', token=session.get('token'))
    
    if 'error' in result:
        bank = next((b for b in MOCK_BANKS if b['id'] == bank_id), MOCK_BANKS[0])
        transactions = [t for t in MOCK_TRANSACTIONS if t['bank_account_id'] == bank_id][:20]
    else:
        bank = result
        transactions = result.get('transactions', [])
    
    return render_template('banks/detail.html', bank=bank, transactions=transactions)

# ==================== TRANSACTIONS ROUTES ====================

@app.route('/transactions')
@login_required
def transactions_list():
    """List all transactions with filtering"""
    # Get filter parameters
    bank_id = request.args.get('bank', type=int)
    category = request.args.get('category')
    trans_type = request.args.get('type')
    date_from = request.args.get('date_from')
    date_to = request.args.get('date_to')
    
    # Filter mock transactions
    transactions = MOCK_TRANSACTIONS.copy()
    
    if bank_id:
        transactions = [t for t in transactions if t['bank_account_id'] == bank_id]
    if category:
        transactions = [t for t in transactions if t['category'] == category]
    if trans_type:
        transactions = [t for t in transactions if t['transaction_type'] == trans_type]
    
    categories = [
        ('salary', 'Salary'),
        ('business_income', 'Business Income'),
        ('investment', 'Investment'),
        ('food', 'Food & Dining'),
        ('transport', 'Transport'),
        ('utilities', 'Utilities'),
        ('healthcare', 'Healthcare'),
        ('education', 'Education'),
        ('entertainment', 'Entertainment'),
        ('shopping', 'Shopping'),
        ('rent', 'Rent'),
        ('insurance', 'Insurance'),
        ('other', 'Other'),
    ]
    
    banks = MOCK_BANKS
    
    return render_template('transactions/list.html',
                         transactions=transactions,
                         categories=categories,
                         banks=banks,
                         filters=request.args)

@app.route('/transactions/<int:trans_id>/classify', methods=['POST'])
@login_required
def classify_transaction(trans_id):
    """Classify a transaction"""
    category = request.form.get('category')
    notes = request.form.get('notes')
    
    # Mock update
    for t in MOCK_TRANSACTIONS:
        if t['id'] == trans_id:
            t['category'] = category
            t['user_notes'] = notes
            break
    
    flash('Transaction classified successfully!', 'success')
    return redirect(url_for('transactions_list'))

# ==================== UPLOADS ROUTES ====================

@app.route('/uploads')
@login_required
def uploads():
    """Upload bank statement page"""
    banks = MOCK_BANKS
    return render_template('uploads/upload.html', banks=banks)

@app.route('/uploads/history')
@login_required
def upload_history():
    """View upload history"""
    result = api_call('/uploads', token=session.get('token'))
    
    if 'error' in result:
        uploads = MOCK_UPLOADS
    else:
        uploads = result
    
    return render_template('uploads/history.html', uploads=uploads)

@app.route('/uploads/process', methods=['POST'])
@login_required
def process_upload():
    """Process uploaded statement"""
    # Mock processing
    flash('Statement uploaded and processing started. You will be notified when complete.', 'success')
    return redirect(url_for('upload_history'))

# ==================== REPORTS ROUTES ====================

@app.route('/reports')
@login_required
def reports():
    """Generate tax reports"""
    return render_template('reports/generate.html')

@app.route('/reports/generate', methods=['POST'])
@login_required
def generate_report():
    """Generate tax report"""
    year = request.form.get('year', datetime.now().year - 1)
    
    result = api_call(f'/tax-reports/generate?year={year}', token=session.get('token'))
    
    if 'error' in result:
        report = MOCK_TAX_REPORT
    else:
        report = result
    
    return render_template('reports/generate.html', report=report)

@app.route('/reports/export/<format>')
@login_required
def export_report(format):
    """Export tax report"""
    year = request.args.get('year', datetime.now().year - 1)
    
    result = api_call(f'/tax-reports/export/{format}?year={year}', token=session.get('token'))
    
    if 'error' in result:
        flash(f'Report exported as {format.upper()}', 'success')
        return redirect(url_for('reports'))
    
    return result

# ==================== SETTINGS ROUTES ====================

@app.route('/settings')
@login_required
def settings():
    """User settings page"""
    user = session.get('user', MOCK_USER)
    return render_template('settings/index.html', user=user)

@app.route('/settings/profile', methods=['POST'])
@login_required
def update_profile():
    """Update user profile"""
    data = {
        'first_name': request.form.get('first_name'),
        'last_name': request.form.get('last_name'),
        'phone': request.form.get('phone'),
    }
    
    result = api_call('/auth/profile', 'PUT', data, token=session.get('token'))
    
    if 'error' not in result:
        session['user'].update(data)
    
    flash('Profile updated successfully!', 'success')
    return redirect(url_for('settings'))

@app.route('/settings/password', methods=['POST'])
@login_required
def change_password():
    """Change user password"""
    current_password = request.form.get('current_password')
    new_password = request.form.get('new_password')
    
    result = api_call('/auth/change-password', 'POST', 
                     {'current_password': current_password, 'new_password': new_password},
                     token=session.get('token'))
    
    flash('Password changed successfully!', 'success')
    return redirect(url_for('settings'))

# ==================== ADMIN ROUTES ====================

@app.route('/admin')
@admin_required
def admin_dashboard():
    """Admin dashboard"""
    stats = {
        'total_users': 1250,
        'active_users': 890,
        'total_transactions': 45678,
        'total_revenue': 15750000,
        'new_users_today': 15,
        'reports_generated': 234,
    }
    
    return render_template('admin/dashboard.html', stats=stats)

@app.route('/admin/users')
@admin_required
def admin_users():
    """Admin users list"""
    result = api_call('/admin/users', token=session.get('token'))
    
    if 'error' in result:
        users = MOCK_ADMIN_USERS
    else:
        users = result
    
    return render_template('admin/users.html', users=users)

@app.route('/admin/settings')
@admin_required
def admin_settings():
    """Admin settings"""
    pricing = [
        {'plan': 'free', 'name': 'Free', 'price': 0, 'features': ['1 Bank Account', 'Basic Reports', 'Email Support']},
        {'plan': 'basic', 'name': 'Basic', 'price': 2500, 'features': ['3 Bank Accounts', 'Advanced Reports', 'Priority Support']},
        {'plan': 'premium', 'name': 'Premium', 'price': 5000, 'features': ['Unlimited Banks', 'Full Reports', '24/7 Support', 'Tax Filing']},
        {'plan': 'enterprise', 'name': 'Enterprise', 'price': 15000, 'features': ['Everything in Premium', 'API Access', 'Dedicated Manager']},
    ]
    
    return render_template('admin/settings.html', pricing=pricing)

# ==================== HTMX PARTIALS ====================

@app.route('/partials/sidebar-banks')
def partials_sidebar_banks():
    """Dynamic bank list for sidebar"""
    return render_template('partials/sidebar_banks.html', banks=MOCK_BANKS)

@app.route('/partials/transaction-row/<int:trans_id>')
def partials_transaction_row(trans_id):
    """Single transaction row for HTMX updates"""
    trans = next((t for t in MOCK_TRANSACTIONS if t['id'] == trans_id), None)
    return render_template('partials/transaction_row.html', transaction=trans)

@app.route('/partials/stats-cards')
def partials_stats_cards():
    """Stats cards for dashboard"""
    total_income = sum(t['amount'] for t in MOCK_TRANSACTIONS if t['transaction_type'] == 'credit')
    total_expenses = sum(t['amount'] for t in MOCK_TRANSACTIONS if t['transaction_type'] == 'debit')
    total_balance = sum(b['current_balance'] for b in MOCK_BANKS)
    
    return render_template('partials/stats_cards.html',
                         total_income=total_income,
                         total_expenses=total_expenses,
                         total_balance=total_balance)

# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def not_found(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500

# ==================== MAIN ====================

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
