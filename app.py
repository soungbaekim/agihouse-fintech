#!/usr/bin/env python3
"""
Finance Analyzer - Web Application
A Flask web app that provides an interactive frontend for the Finance Analyzer.
"""

import os
import json
import csv
import datetime
import argparse
from pathlib import Path
from flask import Flask, render_template, request, redirect, url_for, jsonify, flash, session
from werkzeug.utils import secure_filename

# Import core modules
from parsers.parser_factory import ParserFactory
from analysis.spending_analyzer import SpendingAnalyzer
from recommendations.savings_recommender import SavingsRecommender
from recommendations.investment_recommender import InvestmentRecommender

# Create Flask app
app = Flask(__name__, 
            template_folder='frontend/templates',
            static_folder='frontend/static')
app.secret_key = os.urandom(24)  # For flash messages and sessions
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload size
app.config['ALLOWED_EXTENSIONS'] = {'csv', 'xlsx', 'xls', 'pdf'}

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize components
parser_factory = ParserFactory()
analyzer = SpendingAnalyzer()
savings_recommender = SavingsRecommender()
investment_recommender = InvestmentRecommender()

def allowed_file(filename):
    """Check if the file has an allowed extension"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    """Render the home page"""
    # Get profile information if available
    profile_names = get_profile_names() if SAMPLE_PROFILES_AVAILABLE else []
    profile_descriptions = get_profile_descriptions() if SAMPLE_PROFILES_AVAILABLE else {}
    
    return render_template('index.html', 
                           profiles_available=SAMPLE_PROFILES_AVAILABLE,
                           profile_names=profile_names,
                           profile_descriptions=profile_descriptions)

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload"""
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    
    file = request.files['file']
    
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Process the file
        try:
            # Parse the statement
            statement_parser = parser_factory.get_parser(file_path)
            transactions = statement_parser.parse(file_path)
            
            # Store transactions in session
            session['file_path'] = file_path
            
            return redirect(url_for('analyze'))
        except Exception as e:
            flash(f'Error processing file: {str(e)}')
            return redirect(url_for('index'))
    else:
        flash('File type not allowed')
        return redirect(url_for('index'))

@app.route('/analyze')
def analyze():
    """Analyze the uploaded file and display results"""
    if 'file_path' not in session:
        flash('Please upload a file first')
        return redirect(url_for('index'))
    
    file_path = session['file_path']
    
    try:
        # Parse the statement
        statement_parser = parser_factory.get_parser(file_path)
        transactions = statement_parser.parse(file_path)
        
        # Analyze spending
        spending_analysis = analyzer.analyze(transactions)
        
        # Generate recommendations
        savings_recommendations = savings_recommender.recommend(spending_analysis)
        investment_recommendations = investment_recommender.recommend(
            spending_analysis, savings_recommendations
        )
        
        # Store analysis results in session
        session['analysis_data'] = {
            'transaction_count': len(transactions),
            'income': spending_analysis['income'],
            'expenses': spending_analysis['expenses'],
            'net_cash_flow': spending_analysis['net_cash_flow'],
            'savings_rate': spending_analysis['savings_rate'],
            'top_categories': spending_analysis['top_spending_categories'],
            'total_potential_savings': savings_recommendations['total_potential_savings']
        }
        
        # Prepare data for charts
        spending_by_category = spending_analysis['spending_by_category']
        monthly_spending = spending_analysis['monthly_spending']
        
        # Convert data for JSON serialization
        for month, data in monthly_spending.items():
            for category, amount in data.items():
                monthly_spending[month][category] = float(amount)
        
        for category, amount in spending_by_category.items():
            spending_by_category[category] = float(amount)
        
        # Store chart data in session
        session['chart_data'] = {
            'spending_by_category': spending_by_category,
            'monthly_spending': monthly_spending,
            'top_merchants': [
                {'merchant': item['merchant'], 'amount': float(item['amount'])}
                for item in spending_analysis['top_merchants']
            ]
        }
        
        # Store recommendations in session
        session['recommendations'] = {
            'savings': savings_recommendations['recommendations'],
            'investment': investment_recommendations['recommendations']
        }
        
        # Store transaction data
        session['transactions'] = [
            {
                'date': t['date'].isoformat(),
                'description': t['description'],
                'amount': float(t['amount']),
                'category': t.get('category', 'Uncategorized')
            }
            for t in transactions
        ]
        
        return render_template('dashboard.html', 
                              analysis=session['analysis_data'],
                              chart_data=session['chart_data'])
    
    except Exception as e:
        flash(f'Error analyzing data: {str(e)}')
        return redirect(url_for('index'))

@app.route('/transactions')
def transactions():
    """Display transaction details"""
    if 'transactions' not in session:
        flash('No transaction data available')
        return redirect(url_for('index'))
    
    return render_template('transactions.html', 
                          transactions=session['transactions'],
                          analysis=session['analysis_data'])

@app.route('/recommendations')
def recommendations():
    """Display recommendations"""
    if 'recommendations' not in session:
        flash('No recommendation data available')
        return redirect(url_for('index'))
    
    return render_template('recommendations.html', 
                          recommendations=session['recommendations'],
                          analysis=session['analysis_data'])

@app.route('/category/<category>')
def category_details(category):
    """Display details for a specific spending category"""
    if 'transactions' not in session:
        flash('No transaction data available')
        return redirect(url_for('index'))
    
    # Filter transactions by category
    category_transactions = [
        t for t in session['transactions'] 
        if t.get('category', '').lower() == category.lower()
    ]
    
    # Get category total
    category_total = sum(t['amount'] for t in category_transactions if t['amount'] < 0)
    
    return render_template('category_details.html',
                          category=category,
                          transactions=category_transactions,
                          total=abs(category_total),
                          analysis=session['analysis_data'])

@app.route('/api/transactions')
def api_transactions():
    """API endpoint for transaction data"""
    if 'transactions' not in session:
        return jsonify({'error': 'No transaction data available'}), 404
    
    return jsonify(session['transactions'])

@app.route('/api/chart-data')
def api_chart_data():
    """API endpoint for chart data"""
    if 'chart_data' not in session:
        return jsonify({'error': 'No chart data available'}), 404
    
    return jsonify(session['chart_data'])

@app.route('/api/recommendations')
def api_recommendations():
    """API endpoint for recommendations"""
    if 'recommendations' not in session:
        return jsonify({'error': 'No recommendation data available'}), 404
    
    return jsonify(session['recommendations'])

@app.route('/sample')
def use_sample_data():
    """Use sample data for demonstration"""
    sample_path = 'data/sample_statement.csv'
    
    if not os.path.exists(sample_path):
        flash('Sample data not found')
        return redirect(url_for('index'))
    
    session['file_path'] = sample_path
    return redirect(url_for('analyze'))

@app.route('/clear')
def clear_session():
    """Clear session data"""
    session.clear()
    flash('Session data cleared')
    return redirect(url_for('index'))

@app.route('/settings')
def settings():
    """Display and manage user settings"""
    return render_template('settings.html')

@app.route('/reports')
def reports():
    """Generate and display financial reports"""
    if 'transactions' not in session:
        flash('No transaction data available')
        return redirect(url_for('index'))
    
    return render_template('reports.html')

@app.route('/generate_report', methods=['POST'])
def generate_report():
    """Generate a financial report based on user selections"""
    if 'transactions' not in session:
        return jsonify({'error': 'No transaction data available'}), 400
    
    # Get report parameters from request
    report_type = request.form.get('report_type', 'monthly')
    report_format = request.form.get('report_format', 'pdf')
    sections = request.form.getlist('sections')
    
    # In a real implementation, this would generate the actual report
    # For now, we'll just return a success message
    return jsonify({
        'success': True,
        'message': f'{report_type.capitalize()} report generated in {report_format.upper()} format'
    })

# Import sample data modules
try:
    from data.sample_data import get_sample_data
    from data.sample_profiles import get_profile_names, get_profile_descriptions, get_sample_profile
    SAMPLE_PROFILES_AVAILABLE = True
except ImportError:
    def get_sample_data():
        return None
    def get_profile_names():
        return []
    def get_profile_descriptions():
        return {}
    def get_sample_profile(profile_name):
        return None
    SAMPLE_PROFILES_AVAILABLE = False

@app.route('/load_sample_data')
def load_sample_data_route():
    """Load generic sample transaction data"""
    try:
        sample_data = get_sample_data()
        if sample_data:
            # Store sample data in session
            session['transactions'] = [
                {
                    'date': t['date'].isoformat(),
                    'description': t['description'],
                    'amount': float(t['amount']),
                    'category': t.get('category', 'Uncategorized')
                }
                for t in sample_data['transactions']
            ]
            session['analysis_data'] = sample_data['analysis']
            session['chart_data'] = {
                'spending_by_category': sample_data['analysis']['spending_by_category'],
                'monthly_spending': sample_data['analysis']['monthly_spending'],
                'top_merchants': sample_data['analysis']['top_merchants']
            }
            session['recommendations'] = sample_data['recommendations']
            
            flash('Sample data loaded successfully!')
            return redirect(url_for('analyze'))
        else:
            flash('Sample data module not found')
            return redirect(url_for('index'))
    except Exception as e:
        flash(f'Error loading sample data: {str(e)}')
        return redirect(url_for('index'))

@app.route('/use_sample_profile/<profile_name>')
def use_sample_profile(profile_name):
    """Load sample transaction data for a specific financial profile"""
    if not SAMPLE_PROFILES_AVAILABLE:
        flash('Sample profiles are not available', 'warning')
        return redirect(url_for('index'))
        
    profile_data = get_sample_profile(profile_name)
    if not profile_data:
        flash(f'Profile {profile_name} not found', 'warning')
        return redirect(url_for('index'))
        
    # Store profile data in session
    session['transactions'] = [
        {
            'date': t['date'].isoformat(),
            'description': t['description'],
            'amount': float(t['amount']),
            'category': t.get('category', 'Uncategorized')
        }
        for t in profile_data['transactions']
    ]
    session['analysis_data'] = profile_data['analysis']
    session['chart_data'] = {
        'spending_by_category': profile_data['analysis']['spending_by_category'],
        'monthly_spending': profile_data['analysis']['monthly_spending'],
        'top_merchants': profile_data['analysis']['top_merchants']
    }
    session['recommendations'] = profile_data['recommendations']
    session['active_profile'] = profile_name
    
    # Flash a message about the selected profile
    profile_descriptions = get_profile_descriptions()
    if profile_name in profile_descriptions:
        flash(f'Loaded "{profile_name.replace("_", " ").title()}" profile: {profile_descriptions[profile_name]}', 'info')
    
    return redirect(url_for('analyze'))

def load_profile_from_file(profile_name):
    """Load profile data from CSV and JSON files"""
    profile_dir = os.path.join('data', 'sample_profiles')
    csv_path = os.path.join(profile_dir, f"{profile_name}.csv")
    json_path = os.path.join(profile_dir, f"{profile_name}_analysis.json")
    
    if not os.path.exists(csv_path) or not os.path.exists(json_path):
        return None
    
    # Load transactions from CSV
    transactions = []
    with open(csv_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Convert string amount to float
            row['amount'] = float(row['amount'])
            transactions.append(row)
    
    # Load analysis and recommendations from JSON
    with open(json_path, 'r') as jsonfile:
        data = json.load(jsonfile)
    
    # Combine data
    return {
        'transactions': transactions,
        'analysis': data['analysis'],
        'recommendations': data['recommendations']
    }

if __name__ == '__main__':
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Finance Analyzer Web Application')
    parser.add_argument('--sample', action='store_true', help='Load sample data on startup')
    parser.add_argument('--profile', type=str, help='Load specific financial profile on startup')
    args = parser.parse_args()
    
    # Start the Flask application
    if args.profile:
        print(f"Starting with {args.profile} profile. Access the application at http://localhost:8082")
        
        # Load profile data directly
        @app.before_request
        def load_profile_data_before_request():
            # Only load profile data once and only for the root route
            if request.endpoint != 'index' or 'sample_data_loaded' in session:
                return None
            
            try:
                # First try to load from file
                profile_data = load_profile_from_file(args.profile)
                
                # If file not found, try to generate dynamically
                if not profile_data and SAMPLE_PROFILES_AVAILABLE:
                    profile_data = get_sample_profile(args.profile)
                
                if profile_data:
                    # Store profile data in session
                    session['transactions'] = [
                        {
                            'date': t['date'] if isinstance(t['date'], str) else t['date'].isoformat(),
                            'description': t['description'],
                            'amount': float(t['amount']),
                            'category': t.get('category', 'Uncategorized')
                        }
                        for t in profile_data['transactions']
                    ]
                    session['analysis_data'] = profile_data['analysis']
                    session['chart_data'] = {
                        'spending_by_category': profile_data['analysis']['spending_by_category'],
                        'monthly_spending': profile_data['analysis']['monthly_spending'],
                        'top_merchants': profile_data['analysis']['top_merchants']
                    }
                    session['recommendations'] = profile_data['recommendations']
                    session['active_profile'] = args.profile
                    session['sample_data_loaded'] = True
                    
                    flash(f'{args.profile.replace("_", " ").title()} profile loaded automatically')
            except Exception as e:
                print(f"Error loading profile data: {str(e)}")
    elif args.sample:
        print("Starting with sample data. Access the application at http://localhost:8082")
        
        # Load sample data directly
        @app.before_request
        def load_sample_data_before_request():
            # Only load sample data once and only for the root route
            if request.endpoint != 'index' or 'sample_data_loaded' in session:
                return None
            
            try:
                sample_data = get_sample_data()
                if sample_data:
                    # Store sample data in session
                    session['transactions'] = [
                        {
                            'date': t['date'].isoformat(),
                            'description': t['description'],
                            'amount': float(t['amount']),
                            'category': t.get('category', 'Uncategorized')
                        }
                        for t in sample_data['transactions']
                    ]
                    session['analysis_data'] = sample_data['analysis']
                    session['chart_data'] = {
                        'spending_by_category': sample_data['analysis']['spending_by_category'],
                        'monthly_spending': sample_data['analysis']['monthly_spending'],
                        'top_merchants': sample_data['analysis']['top_merchants']
                    }
                    session['recommendations'] = sample_data['recommendations']
                    session['sample_data_loaded'] = True
                    
                    flash('Sample data loaded automatically')
            except Exception as e:
                print(f"Error loading sample data: {str(e)}")
    else:
        print("Starting Finance Analyzer. Access the application at http://localhost:8082")
    
    app.run(debug=True, host='0.0.0.0', port=8082)
