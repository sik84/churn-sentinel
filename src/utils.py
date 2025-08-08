def recommend(prob, threshold=0.5):
    if prob > threshold:
        return "Kündigung wahrscheinlich: Kundenbindung verstärken!"
    else:
        return "Kein akutes Risiko"
