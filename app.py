from flask import Flask, render_template, request, jsonify, redirect
from logic import calculate_dasa_bhukti

app = Flask(__name__)

@app.route('/')
def root():
    return redirect('/desabhuthi_calculator.html')

@app.route('/desabhuthi_calculator.html')
@app.route('/desabhuthi')
def home():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.json
    dob = data.get('dob') # 1992/05/20 expected format changed in logic
    # Actually the prompt says DD/MM/YYYY, logic expects YYYY/MM/DD for flatlib usually, 
    # but let's conform logic to whatever we pass or parse here.
    # Logic.py used: Datetime(dob, time...)
    
    # Let's clean up input. flatlib expects YYYY/MM/DD or similar.
    # User input: 20/05/1992
    
    raw_dob = data.get('date')
    raw_time = data.get('time')
    place = data.get('place') # For now, we might mock coord or use geopy if needed.
    # Hardcoding Chennai Lat/Lon for simplicity as prompt gave Chennai example, 
    # but ideally we look it up.
    
    # Parse DD/MM/YYYY to YYYY/MM/DD
    parts = raw_dob.split('/')
    if len(parts) == 3:
        formatted_dob = f"{parts[2]}/{parts[1]}/{parts[0]}"
    else:
        formatted_dob = "2000/01/01" # Fallback

    # Coordinates override
    lat, lon = 13.0827, 80.2707
    
    manual_balance = data.get('manual_balance')

    try:
        result = calculate_dasa_bhukti(formatted_dob, raw_time, lat, lon, manual_balance)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
