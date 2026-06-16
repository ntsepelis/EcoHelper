import pandas as pd
import matplotlib.pyplot as plt
import os

# Όνομα του αρχείου δεδομένων
DATA_FILE = "microclimate_data.csv"
OUTPUT_IMAGE = "climate_report.png"

def create_charts():
    # 1. Έλεγχος αν υπάρχει το αρχείο με τα Ανοιχτά Δεδομένα
    if not os.path.exists(DATA_FILE):
        print(f"Σφάλμα: Το αρχείο {DATA_FILE} δεν βρέθηκε ακόμα. Λειτουργεί το ρομπότ;")
        return

    print("Ανάγνωση δεδομένων και δημιουργία γραφήματος...")

    # 2. Φόρτωση των δεδομένων με το Pandas
    df = pd.read_csv(DATA_FILE)

    # Έλεγχος αν το αρχείο έχει αρκετές εγγραφές
    if len(df) < 2:
        print("Δεν υπάρχουν αρκετά δεδομένα στο CSV για τη δημιουργία γραφήματος.")
        return

    # Μετατροπή της στήλης Timestamp σε μορφή ημερομηνίας/ώρας
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])

    # 3. Ρύθμιση του σχήματος του γραφήματος (10x6 ίντσες)
    fig, ax1 = plt.subplots(figsize=(10, 6))

    # Χρώματα για το γράφημα (Eco-friendly παλέτα)
    color_temp = '#e74c3c'  # Κόκκινο για τη Θερμοκρασία
    color_hum = '#3498db'   # Μπλε για την Υγρασία

    # 4. Σχεδίαση της γραμμής Θερμοκρασίας (Αριστερός Άξονας Υ)
    ax1.set_xlabel('Χρόνος (Timestamp)', fontsize=12, fontweight='bold', labelpad=10)
    ax1.set_ylabel('Θερμοκρασία (°C)', color=color_temp, fontsize=12, fontweight='bold')
    line1 = ax1.plot(df['Timestamp'], df['Temperature_C'], color=color_temp, linewidth=2.5, label='Θερμοκρασία (°C)')
    ax1.tick_params(axis='y', labelcolor=color_temp)
    ax1.grid(True, linestyle='--', alpha=0.5)

    # 5. Δημιουργία δεύτερου άξονα Υ για την Υγρασία (Δεξιός Άξονας Υ)
    ax2 = ax1.twinx()  
    ax2.set_ylabel('Υγρασία (%)', color=color_hum, fontsize=12, fontweight='bold')
    line2 = ax2.plot(df['Timestamp'], df['Humidity_Pct'], color=color_hum, linewidth=2.5, linestyle='-.', label='Υγρασία (%)')
    ax2.tick_params(axis='y', labelcolor=color_hum)

    # 6. Προσθήκη Υπομνήματος (Legend) που ενώνει και τις δύο γραμμές
    lines = line1 + line2
    labels = [l.get_label() for l in lines]
    ax1.legend(lines, labels, loc='upper left', frameon=True, facecolor='#f8f9fa')

    # 7. Τίτλος και μορφοποίηση
    plt.title('Μελέτη Μικροκλίματος & Συνθηκών Περιβάλλοντος\n(Ανοιχτά Δεδομένα - ΕΛΛΑΚ 2026)', 
              fontsize=14, fontweight='bold', color='#2c3e50', pad=15)
    
    # Αυτόματη περιστροφή των ημερομηνιών στον άξονα Χ για να μην κρύβει η μία την άλλη
    fig.autofmt_xdate()
    plt.tight_layout()

    # 8. Αποθήκευση του γραφήματος σε εικόνα υψηλής ανάλυσης
    plt.savefig(OUTPUT_IMAGE, dpi=300)
    plt.close()
    
    print(f"Το γράφημα δημιουργήθηκε επιτυχώς και αποθηκεύτηκε ως '{OUTPUT_IMAGE}'!")

if __name__ == "__main__":
    create_charts()
