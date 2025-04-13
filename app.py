#!/usr/bin/env python3
"""
Finance Analyzer - Web Application
A Flask web app that provides an interactive frontend for the Finance Analyzer.
"""

import os
import csv
import json
import argparse
import datetime
from pathlib import Path
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_session import Session
from werkzeug.utils import secure_filename
from flask_socketio import SocketIO, emit
import os
import json
import uuid
import tempfile
from datetime import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from flask_apscheduler import APScheduler
import logging
from parsers.parser_factory import ParserFactory
from analysis.spending_analyzer import SpendingAnalyzer
from recommendations.savings_recommender import SavingsRecommender
from recommendations.investment_recommender import InvestmentRecommender

# Create Flask app
app = Flask(__name__, 
            static_folder='./frontend/static',
            template_folder='./frontend/templates')

# Configure app
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key-for-testing')
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
app.config['ALLOWED_EXTENSIONS'] = {'csv', 'pdf', 'xlsx', 'xls'}
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload size
app.config['AI_CHAT_AVAILABLE'] = True  # Enable AI chat feature

# Configure Flask-Session to use server-side sessions
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = os.path.join(tempfile.gettempdir(), 'fintech_sessions')
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True
Session(app)

# Initialize Socket.IO
socketio = SocketIO(app, cors_allowed_origins="*", manage_session=False)

# Configure logging
logging.basicConfig(level=logging.INFO,
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('fintech')

# Custom Jinja2 filters
@app.template_filter('usd')
def format_usd(value):
    """Format a number as USD with commas for thousands"""
    if isinstance(value, (int, float)):
        return "${:,.2f}".format(value)
    return value

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
    print("Analyze route called")
    print(f"Session keys: {list(session.keys())}")
    
    # First, check if we have a sample profile loaded
    if 'active_profile' in session and 'transactions' in session:
        print(f"Using active profile: {session['active_profile']} with {len(session['transactions'])} transactions")
        
        # Make sure we have all the data we need
        if all(key in session for key in ['analysis_data', 'chart_data', 'recommendations']):
            print("Using pre-computed analysis data from session")
            
            # Render the dashboard template with the pre-computed data
            return render_template('dashboard.html',
                                   transactions=session['transactions'],
                                   analysis=session['analysis_data'],
                                   chart_data=session['chart_data'],
                                   recommendations=session['recommendations'],
                                   ai_chat_available=app.config.get('AI_CHAT_AVAILABLE', False))
    
    # Next, check if we have a file to analyze
    elif 'file_path' in session:
        print(f"Parsing file: {session['file_path']}")
        try:
            file_path = session['file_path']
            statement_parser = parser_factory.get_parser(file_path)
            transactions = statement_parser.parse(file_path)
        except Exception as e:
            print(f"Error parsing file: {str(e)}")
            flash(f'Error parsing file: {str(e)}')
            return redirect(url_for('index'))
    
    # If we don't have a profile or a file, redirect to the index
    else:
        print("No profile or file found in session")
        flash('Please upload a file or select a sample profile first')
        return redirect(url_for('index'))
    
    try:
        # Analyze spending
        print(f"Analyzing {len(transactions)} transactions")
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
                              chart_data=session['chart_data'],
                              recommendations=session['recommendations'],
                              transactions=session['transactions'],
                              ai_chat_available=app.config.get('AI_CHAT_AVAILABLE', False))
    
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
                          analysis=session['analysis_data'],
                          ai_chat_available=app.config.get('AI_CHAT_AVAILABLE', False))

@app.route('/recommendations')
def recommendations():
    """Display recommendations"""
    print("Recommendation route accessed. Session keys:", list(session.keys()))
    
    # NOTE: We need to display the regular recommendations page directly without redirecting
    # to avoid redirection loops. The user can choose to go to AI recommendations from here.
    
    # CASE 1: Check if we have the recommendations data directly available
    if all(key in session for key in ['analysis_data', 'recommendations', 'transactions']):
        print("All required data found in session - rendering recommendations directly")
        return render_template('recommendations.html',
                            recommendations=session['recommendations'],
                            analysis=session['analysis_data'],
                            ai_chat_available=app.config.get('AI_CHAT_AVAILABLE', False))
    
    # CASE 2: We have an active sample profile
    if 'active_profile' in session:
        profile_name = session['active_profile']
        print(f"Active profile found: {profile_name}")
        
        # Check if we already have transactions loaded for this profile
        if 'transactions' in session:
            # Regenerate all data for this profile to ensure consistency
            try:
                print(f"Regenerating data for profile: {profile_name}")
                profile_data = get_sample_profile(profile_name)
                
                # Store transactions and other data in session
                session['transactions'] = profile_data['transactions']
                session['analysis_data'] = profile_data['analysis']
                session['chart_data'] = profile_data['chart_data']
                session['recommendations'] = profile_data['recommendations']
                
                return render_template('recommendations.html',
                                    recommendations=session['recommendations'],
                                    analysis=session['analysis_data'],
                                    ai_chat_available=app.config.get('AI_CHAT_AVAILABLE', False))
            except Exception as e:
                print(f"Error loading sample profile: {e}")
                flash(f'Error loading sample profile: {str(e)}')
                return redirect(url_for('index'))
        else:
            # If we have a profile name but no data, need to reload the profile
            print(f"Redirecting to use_sample_profile with profile: {profile_name}")
            return redirect(url_for('use_sample_profile', profile_name=profile_name))
    
    # CASE 3: We have transactions but not the other data needed
    if 'transactions' in session and not all(key in session for key in ['analysis_data', 'recommendations']):
        print("Transactions found but missing analysis or recommendations - regenerating")
        try:
            # Process the transactions to generate recommendations
            transactions = session['transactions']
            
            # Analyze spending
            spending_analysis = analyzer.analyze(transactions)
            
            # Generate recommendations
            savings_recommendations = savings_recommender.recommend(spending_analysis)
            investment_recommendations = investment_recommender.recommend(
                spending_analysis, savings_recommendations
            )
            
            # Store analysis data in session
            session['analysis_data'] = {
                'transaction_count': len(transactions),
                'income': spending_analysis['income'],
                'expenses': spending_analysis['expenses'],
                'net_cash_flow': spending_analysis['net_cash_flow'],
                'savings_rate': spending_analysis['savings_rate'],
                'top_categories': spending_analysis['top_spending_categories'],
                'total_potential_savings': savings_recommendations['total_potential_savings']
            }
            
            # Store recommendations in session
            session['recommendations'] = {
                'savings': savings_recommendations['recommendations'],
                'investment': investment_recommendations['recommendations']
            }
            
            # Prepare chart data
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
            
            return render_template('recommendations.html',
                                recommendations=session['recommendations'],
                                analysis=session['analysis_data'],
                                ai_chat_available=app.config.get('AI_CHAT_AVAILABLE', False))
        except Exception as e:
            print(f"Error regenerating recommendations: {e}")
            flash('Error generating recommendations. Please try again.')
            return redirect(url_for('index'))
    
    # CASE 4: We have a file path but no processed data yet
    if 'file_path' in session:
        print("File path found but no processed data - processing file")
        try:
            # Process the file
            file_path = session['file_path']
            
            # Parse the statement
            statement_parser = parser_factory.get_parser(file_path)
            transactions = statement_parser.parse(file_path)
            
            # Store transactions in session
            session['transactions'] = transactions
            
            # Instead of redirecting, we'll process the transactions right here
            # to avoid a redirect loop
            print("Processing transactions immediately to avoid redirect")
            
            # Process the transactions to generate recommendations
            # Analyze spending
            spending_analysis = analyzer.analyze(transactions)
            
            # Generate recommendations
            savings_recommendations = savings_recommender.recommend(spending_analysis)
            investment_recommendations = investment_recommender.recommend(
                spending_analysis, savings_recommendations
            )
            
            # Store analysis data in session
            session['analysis_data'] = {
                'transaction_count': len(transactions),
                'income': spending_analysis['income'],
                'expenses': spending_analysis['expenses'],
                'net_cash_flow': spending_analysis['net_cash_flow'],
                'savings_rate': spending_analysis['savings_rate'],
                'top_categories': spending_analysis['top_spending_categories'],
                'total_potential_savings': savings_recommendations['total_potential_savings']
            }
            
            # Store recommendations in session
            session['recommendations'] = {
                'savings': savings_recommendations['recommendations'],
                'investment': investment_recommendations['recommendations']
            }
            
            # Prepare chart data
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
            
            # Mark the session as modified
            session.modified = True
            
            # Now render the template directly instead of redirecting
            return render_template('recommendations.html',
                                recommendations=session['recommendations'],
                                analysis=session['analysis_data'],
                                ai_chat_available=app.config.get('AI_CHAT_AVAILABLE', False))
        except Exception as e:
            print(f"Error processing file: {e}")
            flash(f'Error processing file: {str(e)}')
            return redirect(url_for('index'))
    
    # CASE 5: No data available at all
    print("No data available - redirecting to index")
    flash('No recommendation data available. Please upload a statement or use a sample profile.')
    return redirect(url_for('index'))
    
    
@app.route('/ai-recommendations')
def ai_recommendations():
    """Display AI-powered recommendations"""
    print("========== AI RECOMMENDATIONS ROUTE ==========")
    print("AI Recommendations route accessed. Session keys:", list(session.keys()))
    
    # Debug session contents
    for key in session.keys():
        if key in ['transactions', 'analysis_data', 'recommendations', 'active_profile']:
            if key == 'transactions':
                print(f"Session contains {len(session[key])} transactions")
            else:
                print(f"Session contains {key} with data: {session[key]}")
    
    if not app.config.get('AI_CHAT_AVAILABLE', False):
        flash('AI recommendations are not available.')
        return redirect(url_for('recommendations'))
    
    # CASE 1: Check if we have the required data available
    if all(key in session for key in ['analysis_data', 'transactions']):
        print("All required data found in session - rendering AI recommendations directly")
        return render_template('ai_recommendations.html',
                             analysis=session['analysis_data'],
                             transactions=session['transactions'])
    
    # CASE 2: We have an active sample profile but missing data
    if 'active_profile' in session:
        profile_name = session['active_profile']
        print(f"Active profile found: {profile_name}, but missing required data")
        
        try:
            print(f"Regenerating data for profile: {profile_name}")
            profile_data = get_sample_profile(profile_name)
            
            if not profile_data or not isinstance(profile_data, dict):
                print(f"Error: Invalid profile data for {profile_name}")
                flash(f'Error loading profile: Invalid profile data format', 'danger')
                return redirect(url_for('index'))
                
            # Important: Make sure we have all the required data
            if not all(key in profile_data for key in ['transactions', 'analysis', 'recommendations']):
                print(f"Error: Missing required data in profile: {[key for key in ['transactions', 'analysis', 'recommendations'] if key not in profile_data]}")
                flash('Error loading profile: Missing required data', 'danger')
                return redirect(url_for('index'))
            
            # Fresh clean of session data
            for key in ['transactions', 'analysis_data', 'chart_data', 'recommendations']:
                if key in session:
                    session.pop(key, None)
            
            # Store transactions with clean copy
            session['transactions'] = []
            for t in profile_data['transactions']:
                trans = {
                    'description': t.get('description', 'Unknown transaction'),
                    'amount': float(t.get('amount', 0)),
                    'category': t.get('category', 'Uncategorized'),
                    'date': str(t.get('date', ''))
                }
                session['transactions'].append(trans)
            
            # Store analysis data with clean fields
            analysis = profile_data['analysis']
            session['analysis_data'] = {
                'transaction_count': len(session['transactions']),
                'income': float(analysis.get('income', 0)),
                'expenses': float(analysis.get('expenses', 0)),
                'net_cash_flow': float(analysis.get('net_cash_flow', 0)),
                'savings_rate': float(analysis.get('savings_rate', 0)),
                'top_categories': analysis.get('top_spending_categories', []) 
                                 if 'top_spending_categories' in analysis 
                                 else analysis.get('top_categories', []),
                'total_potential_savings': float(analysis.get('total_potential_savings', 0))
            }
            
            # Build proper chart data structure
            session['chart_data'] = {
                'spending_by_category': analysis.get('spending_by_category', {}),
                'monthly_spending': analysis.get('monthly_spending', {}),
                'top_merchants': analysis.get('top_merchants', [])
            }
            
            # Store recommendations
            if isinstance(profile_data['recommendations'], dict):
                session['recommendations'] = profile_data['recommendations']
            else:
                session['recommendations'] = {'savings': [], 'investment': []}
                
            # Explicitly mark the session as modified
            session.modified = True
            
            print("Successfully regenerated profile data. Session now contains:", list(session.keys()))
            return render_template('ai_recommendations.html',
                                 analysis=session['analysis_data'],
                                 transactions=session['transactions'])
        except Exception as e:
            print(f"Error loading sample profile for AI recommendations: {e}")
            import traceback
            traceback.print_exc()
            flash(f'Error loading sample profile: {str(e)}', 'danger')
            return redirect(url_for('index'))
    
    # CASE 3: We have transactions but no analysis
    if 'transactions' in session and 'analysis_data' not in session:
        print("Transactions found but missing analysis - regenerating for AI recommendations")
        try:
            # Process the transactions
            transactions = session['transactions']
            
            # Analyze spending
            spending_analysis = analyzer.analyze(transactions)
            
            # Generate recommendations
            savings_recommendations = savings_recommender.recommend(spending_analysis)
            
            # Store analysis data in session
            session['analysis_data'] = {
                'transaction_count': len(transactions),
                'income': spending_analysis['income'],
                'expenses': spending_analysis['expenses'],
                'net_cash_flow': spending_analysis['net_cash_flow'],
                'savings_rate': spending_analysis['savings_rate'],
                'top_categories': spending_analysis['top_spending_categories'],
                'total_potential_savings': savings_recommendations['total_potential_savings']
            }
            
            return render_template('ai_recommendations.html',
                                 analysis=session['analysis_data'],
                                 transactions=session['transactions'])
        except Exception as e:
            print(f"Error regenerating analysis for AI recommendations: {e}")
            flash('Error generating recommendations. Please try again.')
            return redirect(url_for('index'))
    
    # CASE 4: We have a file path but no processed data yet
    if 'file_path' in session:
        print("File path found but no processed data - processing file for AI recommendations")
        try:
            # Process the file
            file_path = session['file_path']
            
            # Parse the statement
            statement_parser = parser_factory.get_parser(file_path)
            transactions = statement_parser.parse(file_path)
            
            # Store transactions in session
            session['transactions'] = transactions
            
            # Now that we have transactions, redirect back to recommendations
            return redirect(url_for('ai_recommendations'))
        except Exception as e:
            print(f"Error processing file for AI recommendations: {e}")
            flash(f'Error processing file: {str(e)}')
            return redirect(url_for('index'))
    
    # CASE 5: No data available at all
    print("No data available for AI recommendations - redirecting to index")
    flash('No financial data available. Please upload a statement or use a sample profile.')
    return redirect(url_for('index'))

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

# Force sample profiles to be available if the directory exists
import os
if os.path.exists(os.path.join(os.path.dirname(__file__), 'data', 'sample_profiles')):
    SAMPLE_PROFILES_AVAILABLE = True

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
    print(f"Loading sample profile: {profile_name}")
    
    # Clean up the profile name to ensure it's valid
    profile_name = profile_name.strip().lower()
    
    # Get the list of valid profiles from the sample_profiles module
    from data.sample_profiles import get_profile_names
    valid_profiles = get_profile_names()
    
    if profile_name not in valid_profiles:
        flash(f'Invalid profile name: {profile_name}', 'warning')
        return redirect(url_for('index'))
    
    # Force SAMPLE_PROFILES_AVAILABLE to be true if the directory exists
    global SAMPLE_PROFILES_AVAILABLE
    sample_dir = os.path.join(os.path.dirname(__file__), 'data', 'sample_profiles')
    if os.path.exists(sample_dir):
        SAMPLE_PROFILES_AVAILABLE = True
        print(f"Sample profiles directory found: {sample_dir}")
    
    if not SAMPLE_PROFILES_AVAILABLE:
        flash('Sample profiles are not available', 'warning')
        return redirect(url_for('index'))
    
    # Try to load from files first
    profile_data = load_profile_from_file(profile_name)
    print(f"Profile data loaded for {profile_name}: {profile_data is not None}")
    
    # If file loading fails, try to generate profile data
    if not profile_data:
        print(f"Attempting to generate {profile_name} profile data dynamically")
        profile_data = get_sample_profile(profile_name)
        
    if not profile_data:
        flash(f'Profile {profile_name} not found', 'warning')
        return redirect(url_for('index'))
    
    # Check if we have all the required data in the profile
    required_keys = ['transactions', 'analysis', 'recommendations']
    missing_keys = [key for key in required_keys if key not in profile_data]
    if missing_keys:
        print(f"Error: Missing required data in profile: {missing_keys}")
        flash('Error processing profile data: Missing required data', 'danger')
        return redirect(url_for('index'))
        
    # Note: chart_data is derived from analysis, not required directly
        
    try:
        # Clear any existing session data
        for key in ['transactions', 'analysis_data', 'chart_data', 'recommendations', 
                    'file_path', 'active_profile']:
            session.pop(key, None)
                
        # Ensure we have a proper list of transactions
        if not isinstance(profile_data.get('transactions', []), list):
            print("Error: transactions is not a list")
            flash('Error processing profile data', 'danger')
            return redirect(url_for('index'))
            
        # Deep copy the transactions to ensure they are all valid
        session['transactions'] = []
        for t in profile_data['transactions']:
            trans = {
                'description': t.get('description', 'Unknown transaction'),
                'amount': float(t.get('amount', 0)),
                'category': t.get('category', 'Uncategorized')
            }
            
            # Handle date carefully
            if 'date' in t:
                if hasattr(t['date'], 'isoformat'):
                    trans['date'] = t['date'].isoformat()
                else:
                    trans['date'] = str(t['date'])
            else:
                trans['date'] = datetime.datetime.now().strftime('%Y-%m-%d')
                
            session['transactions'].append(trans)
        
        print(f"Stored {len(session['transactions'])} transactions in session")
            
        # Store analysis data (ensure all required fields are present)
        analysis = profile_data['analysis']
        required_analysis_fields = ['income', 'expenses', 'net_cash_flow', 'savings_rate', 
                                  'top_categories', 'top_spending_categories', 
                                  'spending_by_category', 'monthly_spending', 'top_merchants']
        
        for field in required_analysis_fields:
            if field not in analysis:
                print(f"Warning: Missing analysis field: {field}. Adding default value.")
                if field in ['income', 'expenses', 'net_cash_flow', 'savings_rate']:
                    analysis[field] = 0.0
                elif field in ['top_categories', 'top_spending_categories', 'top_merchants']:
                    analysis[field] = []
                elif field in ['spending_by_category', 'monthly_spending']:
                    analysis[field] = {}
        
        # Convert numeric values to ensure they're serializable
        for field in ['income', 'expenses', 'net_cash_flow', 'savings_rate']:
            if field in analysis:
                analysis[field] = float(analysis[field])
        
        # Calculate total potential savings properly from the savings recommendations
        total_potential_savings = 0.0
        if isinstance(profile_data['recommendations'], dict) and 'savings' in profile_data['recommendations']:
            savings_recs = profile_data['recommendations']['savings']
            if isinstance(savings_recs, list) and savings_recs:
                # Sum up all potential savings from each recommendation
                total_potential_savings = sum(
                    float(rec.get('potential_savings', 0.0)) 
                    for rec in savings_recs
                )
        
        # Check if we already have a total_potential_savings directly in the recommendations
        if isinstance(profile_data['recommendations'], dict) and 'total_potential_savings' in profile_data['recommendations']:
            # Use the directly provided value if it exists
            direct_total = float(profile_data['recommendations']['total_potential_savings'])
            if direct_total > 0 and total_potential_savings == 0:
                total_potential_savings = direct_total
        
        session['analysis_data'] = {
            'transaction_count': len(session['transactions']),
            'income': float(analysis['income']),
            'expenses': float(analysis['expenses']),
            'net_cash_flow': float(analysis['net_cash_flow']),
            'savings_rate': float(analysis['savings_rate']),
            'top_categories': analysis['top_spending_categories'] if 'top_spending_categories' in analysis else analysis['top_categories'],
            'total_potential_savings': float(total_potential_savings)
        }
        
        print(f"Stored analysis data in session: {list(session['analysis_data'].keys())}")
        
        # Prepare chart data (ensure all values are Python native types)
        spending_by_category = analysis['spending_by_category']
        monthly_spending = analysis['monthly_spending']
        
        # Convert data for JSON serialization
        for month, data in monthly_spending.items():
            for category, amount in data.items():
                monthly_spending[month][category] = float(amount)
        
        for category, amount in spending_by_category.items():
            spending_by_category[category] = float(amount)
        
        # Build the chart data correctly
        session['chart_data'] = {
            'spending_by_category': spending_by_category,
            'monthly_spending': monthly_spending,
            'top_merchants': [
                {'merchant': item['merchant'], 'amount': float(item['amount'])}
                for item in analysis['top_merchants']
            ]
        }
        print("Stored chart data in session")
        
        # Store recommendations (ensuring proper format)
        if isinstance(profile_data['recommendations'], dict):
            recs = profile_data['recommendations']
            savings_list = recs.get('savings', []) if isinstance(recs.get('savings'), list) else []
            
            # Ensure all potential_savings values are properly formatted as floats
            for rec in savings_list:
                if 'potential_savings' in rec:
                    rec['potential_savings'] = float(rec['potential_savings'])
            
            investment_list = recs.get('investment', []) if isinstance(recs.get('investment'), list) else []
            
            session['recommendations'] = {
                'savings': savings_list,
                'investment': investment_list,
                'total_potential_savings': float(total_potential_savings)  # Add this to recommendations too
            }
        else:
            # If the recommendations aren't in the right format, create an empty structure
            session['recommendations'] = {
                'savings': [], 
                'investment': [],
                'total_potential_savings': 0.0
            }
            
        print("Stored recommendations in session")
        
        # Set active profile
        session['active_profile'] = profile_name
        print(f"Set active profile to {profile_name}")
        
        # Mark the session as modified
        session.modified = True
        
        # Flash a message about the selected profile
        profile_descriptions = get_profile_descriptions()
        if profile_name in profile_descriptions:
            flash(f'Loaded "{profile_name.replace("_", " ").title()}" profile: {profile_descriptions[profile_name]}', 'info')
            # Also add a flash message to simulate upload success
            flash(f'Successfully processed your financial data. Showing analysis for {profile_name.replace("_", " ").title()}', 'success')
        
        # Add a simulated file_path to make it feel like the user uploaded a file
        sample_file_name = f"{profile_name}_statement.csv"
        session['file_path'] = os.path.join(app.config['UPLOAD_FOLDER'], sample_file_name)
        
        # Redirect to analyze route to simulate the normal user flow after upload
        return redirect(url_for('analyze'))
    except Exception as e:
        print(f"Error storing profile data in session: {e}")
        flash(f'Error loading profile: {str(e)}', 'danger')
        return redirect(url_for('index'))

def load_profile_from_file(profile_name):
    """Load profile data from CSV and JSON files"""
    # Ensure we're using the correct profile name without any unexpected parameters
    profile_name = profile_name.strip().lower()
    print(f"Loading profile: {profile_name}")
    
    # Get the list of valid profiles from the sample_profiles module
    from data.sample_profiles import get_profile_names
    valid_profiles = get_profile_names()
    
    # Make sure we have a valid profile name
    if profile_name not in valid_profiles:
        print(f"Error: Invalid profile name: {profile_name}")
        return None
    
    profile_dir = os.path.join('data', 'sample_profiles')
    csv_path = os.path.join(profile_dir, f"{profile_name}.csv")
    json_path = os.path.join(profile_dir, f"{profile_name}_analysis.json")
    
    print(f"Loading profile from {csv_path} and {json_path}")
    
    # Check that the files exist
    if not os.path.exists(csv_path) or not os.path.exists(json_path):
        print(f"Error: One or both profile files do not exist:\n  CSV: {csv_path}\n  JSON: {json_path}")
        return None
    
    # Load transactions from CSV
    transactions = []
    try:
        with open(csv_path, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Convert string amount to float
                try:
                    row['amount'] = float(row['amount'])
                except (ValueError, KeyError):
                    # Handle missing or invalid amount
                    row['amount'] = 0.0
                    
                # Ensure date is properly handled
                if 'date' not in row:
                    row['date'] = datetime.datetime.now().strftime("%Y-%m-%d")
                elif isinstance(row['date'], str):
                    try:
                        # Try to parse the date, but keep as string
                        parsed_date = datetime.datetime.strptime(row['date'], "%Y-%m-%d")
                        row['date'] = parsed_date.strftime("%Y-%m-%d")
                    except ValueError:
                        # If parsing fails, use current date
                        row['date'] = datetime.datetime.now().strftime("%Y-%m-%d")
                        
                # Ensure category exists
                if 'category' not in row:
                    row['category'] = "Uncategorized"
                    
                transactions.append(row)
                
    except Exception as e:
        print(f"Error loading CSV: {str(e)}")
        return None
    
    # Load analysis and recommendations from JSON
    try:
        with open(json_path, 'r') as jsonfile:
            data = json.load(jsonfile)
    except Exception as e:
        print(f"Error loading JSON: {str(e)}")
        return None
    
    # Combine data
    return {
        'transactions': transactions,
        'analysis': data['analysis'],
        'recommendations': data['recommendations']
    }

# Socket.IO chat handlers
@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@socketio.on('send_message')
def handle_message(data):
    logger.info("========== SOCKET.IO MESSAGE HANDLER ==========")
    logger.info(f"Received message from client")
    
    # Safe access to session data
    session_keys = list(session.keys()) if hasattr(session, 'keys') else []
    logger.info(f"Session contains keys: {session_keys}")
    
    try:
        user_message = data.get('message', '')
        initial_analysis = data.get('initial_analysis', False)
        logger.info(f"Message: '{user_message[:50]}...' (Initial analysis: {initial_analysis})")
        
        # Simplified approach: Just access the required data directly
        # Don't try to reload missing data here - that should be handled at the route level
        
        # Create financial data dictionary with safe defaults
        financial_data = {
            'income': 0.0,
            'expenses': 0.0,
            'net_cash_flow': 0.0,
            'savings_rate': 0.0,
            'top_categories': [],
            'transactions': []
        }
        
        # Add analysis data if available
        if 'analysis_data' in session:
            analysis = session['analysis_data']
            financial_data.update({
                'income': float(analysis.get('income', 0.0)),
                'expenses': float(analysis.get('expenses', 0.0)),
                'net_cash_flow': float(analysis.get('net_cash_flow', 0.0)),
                'savings_rate': float(analysis.get('savings_rate', 0.0)),
                'top_categories': analysis.get('top_categories', [])
            })
        
        # Add transactions if available
        if 'transactions' in session:
            # Take only essential transaction data to reduce size
            financial_data['transactions'] = [
                {
                    'date': t.get('date', ''),
                    'description': t.get('description', ''),
                    'amount': float(t.get('amount', 0.0)),
                    'category': t.get('category', 'Uncategorized')
                } for t in session.get('transactions', [])[:100]  # Limit to 100 transactions
            ]
        
        # Add chart data if available
        if 'chart_data' in session:
            chart_data = session['chart_data']
            financial_data['spending_by_category'] = chart_data.get('spending_by_category', {})
            financial_data['top_merchants'] = chart_data.get('top_merchants', [])
        
        # Add recommendations if available
        if 'recommendations' in session:
            recs = session['recommendations']
            financial_data['savings_recommendations'] = recs.get('savings', [])
            financial_data['investment_recommendations'] = recs.get('investment', [])
        
        logger.info(f"Prepared financial data with {len(financial_data.get('transactions', []))} transactions")
        
        # Get conversation history (as a smaller list to avoid cookie size issues)
        conversation_history = session.get('conversation_history', [])
        # Keep only the last 6 messages to avoid excessive context size
        if len(conversation_history) > 6:
            conversation_history = conversation_history[-6:]
        
        # Get response from AI
        try:
            ai_response = chat_service.get_chat_response(
                user_message=user_message,
                financial_data=financial_data,
                conversation_history=conversation_history,
                initial_analysis=initial_analysis
            )
            logger.info("Successfully received AI response")
            
            # Store conversation (with size limits)
            if 'conversation_history' not in session:
                session['conversation_history'] = []
                
            # Add new messages
            session['conversation_history'].append({'role': 'user', 'content': user_message})
            session['conversation_history'].append({'role': 'assistant', 'content': ai_response})
            
            # Prune conversation history if too long
            if len(session['conversation_history']) > 10:  
                # Keep only the most recent 10 messages
                session['conversation_history'] = session['conversation_history'][-10:]
                
            # Save session
            session.modified = True
            
            # Send response to client
            emit('receive_message', {'message': ai_response})
            
        except Exception as ai_error:
            logger.error(f"Error getting AI response: {str(ai_error)}")
            import traceback
            logger.error(traceback.format_exc())
            emit('error_message', {'error': "I couldn't generate a response. There might be an issue with the AI service."})
            
    except Exception as e:
        logger.error(f"Error in chat handling: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        emit('error_message', {'error': "Sorry, I encountered an error processing your message. Please try again."})

@app.route('/api/clear_chat', methods=['POST'])
def clear_chat():
    """Clear the chat conversation history"""
    if 'conversation_history' in session:
        session.pop('conversation_history')
    return jsonify({'success': True})

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
        print("Starting with sample data. Access the application at http://localhost:8080")
        
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
        print("Starting Finance Analyzer. Access the application at http://localhost:8080")
    
    # Import AI chat service
    try:
        from ai_chat.chat_factory import ChatServiceFactory
        # Create a global chat service instance
        chat_service = ChatServiceFactory.get_chat_service()
        app.config['AI_CHAT_AVAILABLE'] = True
        print("AI Chat service successfully initialized")
    except Exception as e:
        app.config['AI_CHAT_AVAILABLE'] = False
        print(f"AI Chat service not available: {str(e)}")
    
    # Add chat route
    @app.route('/chat')
    def chat():
        """Display the chat interface"""
        return render_template('chat.html', ai_chat_available=app.config['AI_CHAT_AVAILABLE'])
    
    # Add chat API endpoint
    @app.route('/api/chat', methods=['POST'])
    def api_chat():
        """API endpoint for chat"""
        if not app.config['AI_CHAT_AVAILABLE']:
            return jsonify({'error': 'AI Chat service not available'}), 503
        
        # Get user message and context from request
        data = request.json
        user_message = data.get('message', '')
        page_context = data.get('context', {})
        
        if not user_message:
            return jsonify({'error': 'No message provided'}), 400
        
        # Get financial data from session
        financial_data = {
            'analysis_data': session.get('analysis_data', {}),
            'chart_data': session.get('chart_data', {}),
            'recommendations': session.get('recommendations', {}),
            'transactions': session.get('transactions', [])
        }
        
        # Add page context to financial data
        financial_data['page_context'] = page_context
        
        # Get conversation history from session
        conversation_history = session.get('conversation_history', [])
        
        try:
            # Create context-aware prompt based on current page
            context_prefix = ""
            if page_context.get('page'):
                page_path = page_context.get('page')
                if 'transactions' in page_path:
                    context_prefix = "The user is currently viewing their transactions. "
                elif 'recommendations' in page_path:
                    context_prefix = "The user is currently viewing savings recommendations. "
                elif 'category' in page_path and page_context.get('data', {}).get('category'):
                    category = page_context.get('data', {}).get('category')
                    context_prefix = f"The user is currently viewing details for the '{category}' spending category. "
            
            # Enhance user message with context
            enhanced_message = f"{context_prefix}{user_message}" if context_prefix else user_message
            
            # Get response from AI chat service
            response = ChatServiceFactory.get_chat_response(
                enhanced_message, financial_data, conversation_history
            )
            
            # Update conversation history (store original message, not enhanced)
            conversation_history.append({'role': 'user', 'content': user_message})
            conversation_history.append({'role': 'assistant', 'content': response})
            
            # Limit conversation history to last 20 messages
            if len(conversation_history) > 20:
                conversation_history = conversation_history[-20:]
            
            # Store conversation history in session
            session['conversation_history'] = conversation_history
            
            return jsonify({'response': response})
        
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    # Add endpoint to clear chat history
    @app.route('/api/clear_chat', methods=['POST'])
    def clear_chat_history():
        """Clear the chat conversation history"""
        if 'conversation_history' in session:
            session.pop('conversation_history')
        return jsonify({'status': 'success', 'message': 'Chat history cleared'})
    
    # SocketIO event handlers
    @socketio.on('connect')
    def handle_connect():
        print('Client connected')
    
    @socketio.on('disconnect')
    def handle_disconnect():
        print('Client disconnected')
    
    @socketio.on('chat_message')
    def handle_chat_message(data):
        """Handle chat messages via SocketIO"""
        if not app.config['AI_CHAT_AVAILABLE']:
            socketio.emit('chat_response', {'error': 'AI Chat service not available'})
            return
        
        user_message = data.get('message', '')
        
        if not user_message:
            socketio.emit('chat_response', {'error': 'No message provided'})
            return
        
        # Get financial data from session
        financial_data = {
            'analysis_data': session.get('analysis_data', {}),
            'chart_data': session.get('chart_data', {}),
            'recommendations': session.get('recommendations', {}),
            'transactions': session.get('transactions', [])
        }
        
        # Get conversation history from session
        conversation_history = session.get('conversation_history', [])
        
        try:
            # Get response from AI chat service
            response = ChatServiceFactory.get_chat_response(
                user_message, financial_data, conversation_history
            )
            
            # Update conversation history
            conversation_history.append({'role': 'user', 'content': user_message})
            conversation_history.append({'role': 'assistant', 'content': response})
            
            # Limit conversation history to last 10 messages
            if len(conversation_history) > 20:
                conversation_history = conversation_history[-20:]
            
            # Store conversation history in session
            session['conversation_history'] = conversation_history
            
            socketio.emit('chat_response', {'response': response})
        
        except Exception as e:
            socketio.emit('chat_response', {'error': str(e)})
    
    # Run the app with SocketIO
    socketio.run(app, debug=True, host='0.0.0.0', port=8080)
