# Початок файлу app.py (без змін)
import math
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/direct', methods=['POST'])
def direct_task():
    # ... код для прямої задачі залишається без змін ...
    # --- Отримуємо дані з форми ---
    x1 = float(request.form.get('pgz_x1'))
    y1 = float(request.form.get('pgz_y1'))
    distance = float(request.form.get('distance'))

    # Отримуємо азимут і конвертуємо в десяткові градуси
    deg = float(request.form.get('azimuth_deg'))
    min = float(request.form.get('azimuth_min'))
    sec = float(request.form.get('azimuth_sec'))
    decimal_azimuth = deg + min / 60 + sec / 3600

    # --- Виконуємо розрахунки (поки що спрощені) ---
    # Переводимо азимут в радіани для використання в математичних функціях
    azimuth_rad = math.radians(decimal_azimuth)

    # Розраховуємо приріст координат
    delta_x = distance * math.cos(azimuth_rad)
    delta_y = distance * math.sin(azimuth_rad)

    # Розраховуємо координати кінцевої точки
    x2 = x1 + delta_x
    y2 = y1 + delta_y

    # Формуємо рядок з результатом
    result_text = f"Координати кінцевої точки (P2): X = {x2:.2f}, Y = {y2:.2f}"

    # Показуємо результат на тій же сторінці
    return render_template('index.html', pgz_result=result_text)


# ОНОВЛЕНА ФУНКЦІЯ ДЛЯ ОБЕРНЕНОЇ ЗАДАЧІ
@app.route('/inverse', methods=['POST'])
def inverse_task():
    # --- Отримуємо дані з форми ---
    x1 = float(request.form.get('ogz_x1'))
    y1 = float(request.form.get('ogz_y1'))
    x2 = float(request.form.get('ogz_x2'))
    y2 = float(request.form.get('ogz_y2'))

    # --- Виконуємо розрахунки ---
    delta_x = x2 - x1
    delta_y = y2 - y1

    distance = math.sqrt(delta_x ** 2 + delta_y ** 2)

    # --- Логіка для румба та азимута ---
    rhumb_deg_abs = abs(math.degrees(math.atan(delta_y / delta_x)))

    # Визначаємо чверть і розраховуємо румб та азимут
    if delta_x > 0 and delta_y > 0:
        quarter = "I чверть (Пн-Сх)"
        rhumb_str = f"r = {rhumb_deg_abs:.4f}°"
        azimuth_deg = rhumb_deg_abs
    elif delta_x < 0 and delta_y > 0:
        quarter = "II чверть (Пн-Зх)"
        rhumb_str = f"r = {180 - rhumb_deg_abs:.4f}°"
        azimuth_deg = 180 - rhumb_deg_abs
    elif delta_x < 0 and delta_y < 0:
        quarter = "III чверть (Пд-Зх)"
        rhumb_str = f"r = {rhumb_deg_abs:.4f}°"
        azimuth_deg = 180 + rhumb_deg_abs
    elif delta_x > 0 and delta_y < 0:
        quarter = "IV чверть (Пд-Сх)"
        rhumb_str = f"r = {360 - rhumb_deg_abs:.4f}°"
        azimuth_deg = 360 - rhumb_deg_abs
    else:  # Випадки на осях
        quarter = "На осі"
        rhumb_str = ""
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

    # Конвертуємо десятковий азимут в Г-М-С
    az_deg = int(azimuth_deg)
    az_min_decimal = (azimuth_deg - az_deg) * 60
    az_min = int(az_min_decimal)
    az_sec = (az_min_decimal - az_min) * 60

    azimuth_gms_str = f"{az_deg}° {az_min}' {az_sec:.2f}\""

    # Формуємо рядок з результатом
    result_text = f"Відстань = {distance:.2f} м<br>Азимут = {azimuth_gms_str}<br>Румб: {rhumb_str} ({quarter})"

    # Оновлюємо index.html, щоб результат виводився без екранування HTML
    # Ми додамо атрибут `| safe` в шаблоні
    return render_template('index.html', ogz_result=result_text)


if __name__ == '__main__':
    app.run(debug=True)