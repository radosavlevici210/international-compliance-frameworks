from flask import Flask, jsonify, render_template_string
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
import os
from datetime import datetime

class Base(DeclarativeBase):
    pass

app = Flask(__name__)
app.secret_key = os.environ.get('SESSION_SECRET', 'compliance-key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///compliance.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app, model_class=Base)

class ComplianceRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    framework = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(50), default='ACTIVE')
    owner = db.Column(db.String(100), default='Ervin Remus Radosavlevici')
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())

with app.app_context():
    db.create_all()
    if not ComplianceRecord.query.first():
        frameworks = ['WIPO', 'ISO27001', 'GDPR', 'SOC2', 'NIST']
        for fw in frameworks:
            record = ComplianceRecord(framework=fw)
            db.session.add(record)
        db.session.commit()

@app.route('/')
def index():
    records = ComplianceRecord.query.all()
    html = '''
    <h1>International Compliance Frameworks</h1>
    <h2>© 2025 Ervin Remus Radosavlevici</h2>
    <p>Contact: radosavlevici210@icloud.com</p>
    <h3>Active Frameworks:</h3>
    {% for record in records %}
    <p>{{ record.framework }}: {{ record.status }}</p>
    {% endfor %}
    '''
    return render_template_string(html, records=records)

@app.route('/api/compliance')
def compliance_api():
    return jsonify({
        'owner': 'Ervin Remus Radosavlevici',
        'contact': 'radosavlevici210@icloud.com',
        'frameworks_active': ComplianceRecord.query.count(),
        'status': 'PRODUCTION_READY'
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
