# Початок файлу app.py (без змін)
import math
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/direct', methods=['POST'])
def direct_task():
    # --- Збираємо дані в словник ---
    pgz_inputs = {
        'x1': request.form.get('pgz_x1'),
        'y1': request.form.get('pgz_y1'),
        'azimuth_deg': request.form.get('azimuth_deg'),
        'azimuth_min': request.form.get('azimuth_min'),
        'azimuth_sec': request.form.get('azimuth_sec'),
        'distance': request.form.get('distance')
    }

    # --- Конвертуємо дані для розрахунків ---
    x1 = float(pgz_inputs['x1'])
    y1 = float(pgz_inputs['y1'])
    distance = float(pgz_inputs['distance'])
    decimal_azimuth = float(pgz_inputs['azimuth_deg']) + float(pgz_inputs['azimuth_min']) / 60 + float(
        pgz_inputs['azimuth_sec']) / 3600

    # --- Розрахунки ---
    azimuth_rad = math.radians(decimal_azimuth)
    delta_x = distance * math.cos(azimuth_rad)
    delta_y = distance * math.sin(azimuth_rad)
    x2 = x1 + delta_x
    y2 = y1 + delta_y

    result_text = f"Координати кінцевої точки (P2): X = {x2:.2f}, Y = {y2:.2f}"

    # --- Передаємо в шаблон і результат, і початкові дані ---
    return render_template('index.html', pgz_result=result_text, pgz_inputs=pgz_inputs)


@app.route('/inverse', methods=['POST'])
def inverse_task():
    # --- Збираємо дані в словник ---
    ogz_inputs = {
        'x1': request.form.get('ogz_x1'),
        'y1': request.form.get('ogz_y1'),
        'x2': request.form.get('ogz_x2'),
        'y2': request.form.get('ogz_y2')
    }

    # --- Конвертуємо дані для розрахунків ---
    x1 = float(ogz_inputs['x1'])
    y1 = float(ogz_inputs['y1'])
    x2 = float(ogz_inputs['x2'])
    y2 = float(ogz_inputs['y2'])

    # ... (вся логіка розрахунків залишається без змін) ...
    delta_x = x2 - x1
    delta_y = y2 - y1
    distance = math.sqrt(delta_x ** 2 + delta_y ** 2)
    if delta_x == 0:
        rhumb_deg_abs = 90.0 if delta_y != 0 else 0.0
    else:
        rhumb_deg_abs = abs(math.degrees(math.atan(delta_y / delta_x)))
    # ... і так далі ...
    if delta_x > 0 and delta_y > 0:
        quarter = "I чверть (Пн-Сх)"
        azimuth_deg = rhumb_deg_abs
    elif delta_x < 0 and delta_y > 0:
        quarter = "II чверть (Пд-Сх)"
        azimuth_deg = 180 - rhumb_deg_abs
    elif delta_x < 0 and delta_y < 0:
        quarter = "III чверть (Пд-Зх)"
        azimuth_deg = 180 + rhumb_deg_abs
    elif delta_x > 0 and delta_y < 0:
        quarter = "IV чверть (Пн-Зх)"
        azimuth_deg = 360 - rhumb_deg_abs
    else:
        quarter = "На осі"
        if delta_x == 0 and delta_y > 0:
            azimuth_deg = 90
        elif delta_x == 0 and delta_y < 0:
            azimuth_deg = 270
        elif delta_y == 0 and delta_x > 0:
            azimuth_deg = 0
        elif delta_y == 0 and delta_x < 0:
            azimuth_deg = 180
        else:
            azimuth_deg = 0

    az_deg = int(azimuth_deg)
    az_min_decimal = (azimuth_deg - az_deg) * 60
    az_min = int(az_min_decimal)
    az_sec = (az_min_decimal - az_min) * 60
    azimuth_gms_str = f"{az_deg}°{az_min}'{az_sec:.2f}\""

    rm_deg = int(rhumb_deg_abs)
    rm_min_decimal = (rhumb_deg_abs - rm_deg) * 60
    rm_min = int(rm_min_decimal)
    rm_sec = (rm_min_decimal - rm_min) * 60
    rhumb_gms_str = f"{rm_deg}°{rm_min}'{rm_sec:.2f}\""

    final_rhumb_str = f"Румб = {rhumb_gms_str} ({quarter})" if quarter != "На осі" else "Румб: (На осі)"
    result_text = f"Відстань = {distance:.2f} м<br>Азимут = {azimuth_gms_str}<br>{final_rhumb_str}"

    # --- Передаємо в шаблон і результат, і початкові дані ---
    return render_template('index.html', ogz_result=result_text, ogz_inputs=ogz_inputs)

if __name__ == '__main__':
    app.run(debug=True)