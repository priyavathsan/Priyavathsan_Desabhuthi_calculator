import ephem
import math
from datetime import datetime, timedelta

# Constants for Vimshottari Dasa
DASA_PERIODS = {
    'Ketu': 7,
    'Venus': 20,
    'Sun': 6,
    'Moon': 10,
    'Mars': 7,
    'Rahu': 18,
    'Jupiter': 16,
    'Saturn': 19,
    'Mercury': 17
}

DASA_ORDER = ['Ketu', 'Venus', 'Sun', 'Moon', 'Mars', 'Rahu', 'Jupiter', 'Saturn', 'Mercury']

NAKSHATRAS = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashirsha", "Ardra",
    "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni",
    "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha",
    "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishta",
    "Shatabhisha", "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"
]

TAMIL_NAKSHATRAS = {
    "Ashwini": "அஸ்வினி", "Bharani": "பரணி", "Krittika": "கார்த்திகை", "Rohini": "ரோகிணி", 
    "Mrigashirsha": "மிருகசீரிடம்", "Ardra": "திருவாதிரை", "Punarvasu": "புனர்பூசம்", "Pushya": "பூசம்", 
    "Ashlesha": "ஆயில்யம்", "Magha": "மகம்", "Purva Phalguni": "பூரம்", "Uttara Phalguni": "உத்திரம்",
    "Hasta": "ஹஸ்தம்", "Chitra": "சித்திரை", "Swati": "சுவாதி", "Vishakha": "விசாகம்", 
    "Anuradha": "அனுஷம்", "Jyeshtha": "கேட்டை", "Mula": "மூலம்", "Purva Ashadha": "பூராடம்", 
    "Uttara Ashadha": "உத்திராடம்", "Shravana": "திருவோணம்", "Dhanishta": "அவிட்டம்",
    "Shatabhisha": "சதயம்", "Purva Bhadrapada": "பூரட்டாதி", "Uttara Bhadrapada": "உத்திரட்டாதி", "Revati": "ரேவதி"
}

TAMIL_PLANETS = {
    'Ketu': 'கேது', 'Venus': 'சுக்கிரன்', 'Sun': 'சூரியன்', 'Moon': 'சந்திரன்', 'Mars': 'செவ்வாய்', 
    'Rahu': 'ராகு', 'Jupiter': 'குரு', 'Saturn': 'சனி', 'Mercury': 'புதன்'
}

GENERAL_PREDICTIONS = {
    'Ketu': 'ஆன்மீக நாட்டம் அதிகரிக்கும். ஞான மார்க்கத்தில் ஈடுபாடு உண்டாகும்.',
    'Venus': 'சுக போகங்கள் தேடி வரும். கலை, இசை ஆகியவற்றில் ஆர்வம் கூடும்.',
    'Sun': 'அரசு வகை நன்மைகள் உண்டாகும். சமூகத்தில் அந்தஸ்து உயரும்.',
    'Moon': 'மன நிம்மதி கிடைக்கும். நீர் வழிப் பயணங்கள் அமையலாம்.',
    'Mars': 'பூமி யோகம் உண்டாகும். சகோதர வழியில் நன்மைகள் ஏற்படும்.',
    'Rahu': 'எதிர்பாராத பயணங்கள், இடமாற்றம் ஏற்படலாம். அந்நிய தேசத் தொடர்பு கிட்டும்.',
    'Jupiter': 'தன வரவு திருப்தி தரும். பெரியோர்களின் ஆசி கிட்டும்.',
    'Saturn': 'உழைப்புக்கேற்ற பலன் கிடைக்கும். பொறுமை அவசியம்.',
    'Mercury': 'கல்வி, வியாபாரத்தில் முன்னேற்றம் ஏற்படும். புதிய விஷயங்களைக் கற்பீர்கள்.'
}

def get_dasa_bhuktis(dasa_name, dasa_start_date):
    dasa_lord_idx = DASA_ORDER.index(dasa_name)
    bhukti_start_date = dasa_start_date
    bhuktis = []
    
    for i in range(9):
        bhukti_lord_idx = (dasa_lord_idx + i) % 9
        bhukti_lord = DASA_ORDER[bhukti_lord_idx]
        
        bhukti_years = (DASA_PERIODS[dasa_name] * DASA_PERIODS[bhukti_lord]) / 120.0
        bhukti_days = bhukti_years * 365.25
        
        bhukti_end_date = bhukti_start_date + timedelta(days=bhukti_days)
        
        bhuktis.append({
            "bhukti": TAMIL_PLANETS.get(bhukti_lord, bhukti_lord),
            "start": bhukti_start_date.strftime("%d-%m-%Y"),
            "end": bhukti_end_date.strftime("%d-%m-%Y")
        })
        
        bhukti_start_date = bhukti_end_date
    return bhuktis

def calculate_age(dob_date, current_date):
    import calendar
    years = current_date.year - dob_date.year
    months = current_date.month - dob_date.month
    days = current_date.day - dob_date.day
    
    if days < 0:
        prev_month = current_date.month - 1 if current_date.month > 1 else 12
        prev_year = current_date.year if current_date.month > 1 else current_date.year - 1
        _, days_in_prev = calendar.monthrange(prev_year, prev_month)
        days += days_in_prev
        months -= 1
        
    if months < 0:
        months += 12
        years -= 1
        
    return f"{years} ஆண்டுகள், {months} மாதங்கள், {days} நாட்கள்"

def calculate_dasa_bhukti(dob_str, time_str, lat, lon, manual_balance=None):
    # dob_str: YYYY/MM/DD
    # time_str: HH:MM
    
    # Parse date and time
    dt_local = datetime.strptime(f"{dob_str} {time_str}", "%Y/%m/%d %H:%M")
    
    # Convert to UTC (Assuming IST +05:30 as user context implies India)
    dt_utc = dt_local - timedelta(hours=5, minutes=30)
    
    # Calculate Moon Position using Ephem
    observer = ephem.Observer()
    observer.lat = str(lat)
    observer.lon = str(lon)
    observer.date = dt_utc
    
    moon = ephem.Moon()
    moon.compute(observer)
    
    # Calculate Lahiri Ayanamsa (Chitra Paksha)
    # Spica (Chitra) is defined as 180 degrees (0 Libra) in Sidereal Zodiac
    spica = ephem.star('Spica')
    spica.compute(observer)
    
    # variable 'a_lon' is the "apparent longitude" (Tropical) in radians
    spica_tropical_lon = spica.a_ra 
    spica_ecl = ephem.Ecliptic(spica)
    spica_lon_rad = spica_ecl.lon
    
    # Lahiri Ayanamsa = Spica Tropical Longitude - 180 degrees (in radians)
    ayanamsa_rad = spica_lon_rad - math.radians(180)
    
    # Moon Tropical Longitude
    ecl = ephem.Ecliptic(moon)
    moon_tropical_lon = ecl.lon
    
    # Moon Sidereal Longitude = Tropical - Ayanamsa
    moon_sidereal_lon = moon_tropical_lon - ayanamsa_rad
    
    # Normalize to 0-360
    if moon_sidereal_lon < 0:
        moon_sidereal_lon += 2 * math.pi
        
    lon_deg = math.degrees(moon_sidereal_lon)
    
    # Calculate Nakshatra (Default)
    # 360 degrees / 27 nakshatras = 13.3333... degrees per nakshatra
    nak_duration = 360.0 / 27.0
    nakshatra_idx = int(lon_deg / nak_duration)
    nakshatra_name = NAKSHATRAS[nakshatra_idx]
    
    # MANUAL OVERRIDE
    if manual_balance and manual_balance.get('star'):
        manual_star_input = manual_balance.get('star')
        if manual_star_input in NAKSHATRAS:
            nakshatra_name = manual_star_input
            nakshatra_idx = NAKSHATRAS.index(nakshatra_name)
    
    # Determine Starting Dasa
    dasa_start_idx = nakshatra_idx % 9
    start_dasa_name = DASA_ORDER[dasa_start_idx]
    
    # Calculate Balance
    if manual_balance:
        # User provided manual balance
        m_y = manual_balance.get('years', 0)
        m_m = manual_balance.get('months', 0)
        m_d = manual_balance.get('days', 0)
        
        # Approximate days
        balance_days = (m_y * 365.25) + (m_m * 30.44) + m_d
        balance_years = balance_days / 365.25
    else:
        # Calculated Balance
        deg_in_nak = lon_deg % nak_duration
        percent_passed = deg_in_nak / nak_duration
        balance_percent = 1.0 - percent_passed
        
        dasa_len = DASA_PERIODS[start_dasa_name]
        balance_years = dasa_len * balance_percent
        balance_days = balance_years * 365.25
    
    # Calculate Balance End Date
    first_dasa_end_dt = dt_local + timedelta(days=balance_days)
    
    # Find Current Dasa/Bhukti
    current_dt = datetime.now()
    
    running_date = first_dasa_end_dt
    current_dasa = start_dasa_name
    current_dasa_end = first_dasa_end_dt
    
    # If currently calculating for a past date or very early date (unlikely but safe to handle)
    # Check if we are still in first dasa
    detected_dasa = start_dasa_name
    detected_dasa_end = first_dasa_end_dt
    previous_dasa_end = dt_local
    
    current_dasa_idx = dasa_start_idx

    # Find Dasa
    if current_dt < first_dasa_end_dt:
        detected_dasa = start_dasa_name
        detected_dasa_end = first_dasa_end_dt
        previous_dasa_end = dt_local
    else:
        # Loop forward from first dasa end
        while True:
            current_dasa_idx = (current_dasa_idx + 1) % 9
            dasa_name = DASA_ORDER[current_dasa_idx]
            dasa_duration_days = DASA_PERIODS[dasa_name] * 365.25
            dasa_end_date = running_date + timedelta(days=dasa_duration_days)
            
            if current_dt <= dasa_end_date:
                detected_dasa = dasa_name
                detected_dasa_end = dasa_end_date
                previous_dasa_end = running_date
                break
            
            running_date = dasa_end_date

    # Find Bhukti
    # Bhukti starts from the Dasa lord itself
    dasa_lord_idx = DASA_ORDER.index(detected_dasa)
    
    # Calculate exact start date of the current Dasa
    if detected_dasa == start_dasa_name and current_dt < first_dasa_end_dt:
        dasa_duration_days = DASA_PERIODS[detected_dasa] * 365.25
        dasa_start_date = first_dasa_end_dt - timedelta(days=dasa_duration_days)
    else:
        dasa_start_date = previous_dasa_end

    all_bhuktis = get_dasa_bhuktis(detected_dasa, dasa_start_date)
    
    # Extract current bhukti using exact dates
    for b in all_bhuktis:
        start_dt = datetime.strptime(b['start'], "%d-%m-%Y")
        end_dt = datetime.strptime(b['end'], "%d-%m-%Y")
        # Need accurate full datetime comparison, 
        # But we format them out as dates. Let's just do a rough check or use original logic.
    
    # Retaining exact current bhukti calculation using original logic
    bhukti_start_temp = dasa_start_date
    detected_bhukti = None
    detected_bhukti_end = None
    for i in range(9):
        bhukti_lord_idx = (dasa_lord_idx + i) % 9
        bhukti_lord = DASA_ORDER[bhukti_lord_idx]
        bhukti_years = (DASA_PERIODS[detected_dasa] * DASA_PERIODS[bhukti_lord]) / 120.0
        bhukti_days = bhukti_years * 365.25
        bhukti_end_temp = bhukti_start_temp + timedelta(days=bhukti_days)
        
        if detected_bhukti is None and current_dt <= bhukti_end_temp:
            detected_bhukti = bhukti_lord
            detected_bhukti_end = bhukti_end_temp
        bhukti_start_temp = bhukti_end_temp

    if detected_bhukti is None:
        detected_bhukti = bhukti_lord
        detected_bhukti_end = bhukti_end_temp

    # Calculate Previous Dasa and Next Dasa
    prev_dasa_name = DASA_ORDER[(dasa_lord_idx - 1) % 9]
    prev_dasa_duration = DASA_PERIODS[prev_dasa_name] * 365.25
    prev_dasa_start = dasa_start_date - timedelta(days=prev_dasa_duration)
    prev_bhuktis = get_dasa_bhuktis(prev_dasa_name, prev_dasa_start)
    
    next_dasa_name = DASA_ORDER[(dasa_lord_idx + 1) % 9]
    # next dasa start uses detected_dasa_end precisely for floating point accuracy avoiding gaps
    next_bhuktis = get_dasa_bhuktis(next_dasa_name, detected_dasa_end)

    # Formatting Balance
    bal_y = int(balance_years) # Simple year extraction
    # More precise balance display:
    remaining_days = balance_days
    b_y = int(remaining_days / 365.25)
    remaining_days %= 365.25
    b_m = int(remaining_days / 30.44)
    remaining_days %= 30.44
    b_d = int(remaining_days)

    # Calculate age
    dob_date = dt_local.date()
    current_date = current_dt.date()
    current_age_str = calculate_age(dob_date, current_date)

    return {
        "nakshatra": TAMIL_NAKSHATRAS.get(nakshatra_name, nakshatra_name),
        "start_dasa": TAMIL_PLANETS.get(start_dasa_name, start_dasa_name),
        "balance": f"{b_y} ஆண்டுகள், {b_m} மாதங்கள், {b_d} நாட்கள்",
        "current_dasa": TAMIL_PLANETS.get(detected_dasa, detected_dasa),
        "current_dasa_end": detected_dasa_end.strftime("%d-%m-%Y"),
        "current_bhukti": TAMIL_PLANETS.get(detected_bhukti, detected_bhukti),
        "current_bhukti_end": detected_bhukti_end.strftime("%d-%m-%Y"),
        "all_bhuktis": all_bhuktis,
        "prev_dasa": TAMIL_PLANETS.get(prev_dasa_name, prev_dasa_name),
        "prev_all_bhuktis": prev_bhuktis,
        "next_dasa": TAMIL_PLANETS.get(next_dasa_name, next_dasa_name),
        "next_all_bhuktis": next_bhuktis,
        "date": current_dt.strftime("%d-%m-%Y"),
        "current_age": current_age_str,
        "prediction": GENERAL_PREDICTIONS.get(detected_dasa, "பொதுவான பலன்கள் கிடைக்கும்.")
    }
