from ml_predictor import ml_predictor

print("=" * 50)
print("TEST ML PREDICTOR")
print("=" * 50)
print(f"ML Disponible: {ml_predictor.ml_available}")

if ml_predictor.ml_available:
    pred = ml_predictor.predict_daily_generation(
        latitude=-38.7183,
        avg_irradiance=850,
        avg_wind_speed=6.5,
        mes=1
    )
    print("\nPredicción diaria:")
    print(f"  Solar: {pred['solar_kwh_day']:.2f} kWh/día")
    print(f"  Eólica: {pred['wind_kwh_day']:.2f} kWh/día")
    print(f"  Total: {pred['total_kwh_day']:.2f} kWh/día")
    print(f"  ML usado: {pred['ml_used']}")
else:
    print("❌ ML no disponible")
print("=" * 50)
