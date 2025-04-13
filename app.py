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
from flask import Flask, render_template, request, redirect, url_for, jsonify, flash, session
from werkzeug.utils import secure_filename
from flask_socketio import SocketIO

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

# Custom Jinja2 filters
@app.template_filter('usd')
def format_usd(value):
    """Format a number as USD with commas for thousands"""
    if isinstance(value, (int, float)):
        return "${:,.2f}".format(value)
    return value

# Initialize SocketIO
socketio = SocketIO(app, cors_allowed_origins="*")

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
            
            # Render the analysis template with the pre-computed data
            return render_template('analysis.html',
                                   transactions=session['transactions'],
                                   analysis=session['analysis_data'],
                                   chart_data=session['chart_data'],
                                   recommendations=session['recommendations'])
    
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
    
    # Define the valid profiles
    valid_profiles = [
        "young_professional", "family_budget", "student_finances", 
        "retirement_planning", "high_income", "debt_reduction"
    ]
    
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
    
    # Clear any existing session data
    session.pop('file_path', None)
    
    # Store profile data in session
    try:
        # Ensure we have a proper list of transactions
        if not isinstance(profile_data.get('transactions', []), list):
            print("Error: transactions is not a list")
            flash('Error processing profile data', 'danger')
            return redirect(url_for('index'))
            
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
            
        # Store analysis data
        session['analysis_data'] = profile_data['analysis']
        
        # Prepare chart data
        session['chart_data'] = {
            'spending_by_category': profile_data['analysis']['spending_by_category'],
            'monthly_spending': profile_data['analysis']['monthly_spending'],
            'top_merchants': profile_data['analysis']['top_merchants']
        }
        
        # Store recommendations
        session['recommendations'] = profile_data['recommendations']
        
        # Mark this as an active profile
        session['active_profile'] = profile_name
        
        print(f"Successfully stored profile data in session. Transactions: {len(session['transactions'])}")
    except Exception as e:
        print(f"Error storing profile data in session: {str(e)}")
        flash(f'Error processing profile: {str(e)}', 'danger')
        return redirect(url_for('index'))
    
    # Flash a message about the selected profile
    profile_descriptions = get_profile_descriptions()
    if profile_name in profile_descriptions:
        flash(f'Loaded "{profile_name.replace("_", " ").title()}" profile: {profile_descriptions[profile_name]}', 'info')
    
    return redirect(url_for('analyze'))

def load_profile_from_file(profile_name):
    """Load profile data from CSV and JSON files"""
    # Ensure we're using the correct profile name without any unexpected parameters
    profile_name = profile_name.strip().lower()
    print(f"Loading profile: {profile_name}")
    
    # Define the specific profiles we support
    valid_profiles = [
        "young_professional", "family_budget", "student_finances", 
        "retirement_planning", "high_income", "debt_reduction"
    ]
    
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
        app.config['AI_CHAT_AVAILABLE'] = True
    except ImportError:
        app.config['AI_CHAT_AVAILABLE'] = False
        print("AI Chat service not available. Please install required packages.")
    
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
