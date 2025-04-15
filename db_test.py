from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/bookmanager'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

try:
    with app.app_context():
        # Use the `db.session.execute()` with a `text()` query
        db.session.execute(text("SELECT 1"))
    print("✅ MySQL connection successful.")
except Exception as e:
    print("❌ MySQL connection failed:")
    print(e)
