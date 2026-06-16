import os
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from git import Repo  # Βιβλιοθήκη για τον χειρισμό του Git

DATA_FILE = "microclimate_data.csv"
OUTPUT_IMAGE = "climate_report.png"

# Ρυθμίσεις για το GitHub σας (Αντικαταστήστε με τα δικά σας στοιχεία)
REPO_PATH = "/home/pi/your_project_folder"  # Ο φάκελος στον οποίο κάνατε git clone
COMMIT_MESSAGE = "Αυτόματη ενημέρωση γραφήματος μικροκλίματος"

def create_charts():
    if not os.path.exists(DATA_FILE):
        print(f"Σφάλμα: Το αρχείο {DATA_FILE} δεν βρέθηκε.")
        return False

    df = pd.read_csv(DATA_FILE)
    if len(df) < 2:
        print("Δεν υπάρχουν αρκετά δεδομένα για γράφημα.")
        return False

    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    fig, ax1 = plt.subplots(figsize=(10, 6))

    color_temp = '#e74c3c'
    color_hum = '#3498db'

    ax1.set_xlabel('Χρόνος (Timestamp)', fontsize=12, fontweight='bold', labelpad=10)
    ax1.set_ylabel('Θερμοκρασία (°C)', color=color_temp, fontsize=12, fontweight='bold')
    line1 = ax1.plot(df['Timestamp'], df['Temperature_C'], color=color_temp, linewidth=2.5, label='Θερμοκρασία (°C)')
    ax1.tick_params(axis='y', labelcolor=color_temp)
    ax1.grid(True, linestyle='--', alpha=0.5)

    ax2 = ax1.twinx()  
    ax2.set_ylabel('Υγρασία (%)', color=color_hum, fontsize=12, fontweight='bold')
    line2 = ax2.plot(df['Timestamp'], df['Humidity_Pct'], color=color_hum, linewidth=2.5, linestyle='-.', label='Υγρασία (%)')
    ax2.tick_params(axis='y', labelcolor=color_hum)

    lines = line1 + line2
    labels = [l.get_label() for l in lines]
    ax1.legend(lines, labels, loc='upper left', frameon=True, facecolor='#f8f9fa')

    plt.title('Μελέτη Μικροκλίματος & Συνθηκών Περιβάλλοντος\n(Ανοιχτά Δεδομένα - ΕΛΛΑΚ 2026)', 
              fontsize=14, fontweight='bold', color='#2c3e50', pad=15)
    
    fig.autofmt_xdate()
    plt.tight_layout()
    plt.savefig(OUTPUT_IMAGE, dpi=300)
    plt.close()
    print("Το γράφημα δημιουργήθηκε τοπικά.")
    return True

def upload_to_github():
    """Συνάρτηση που κάνει add, commit και push την εικόνα στο GitHub"""
    try:
        # Άνοιγμα του τοπικού αποθετηρίου Git
        repo = Repo(REPO_PATH)
        
        # Έλεγχος αν υπάρχουν αλλαγές (αν δημιουργήθηκε νέο γράφημα)
        repo.git.add(OUTPUT_IMAGE)
        
        # Commit των αλλαγών
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        repo.index.commit(f"{COMMIT_MESSAGE} ({timestamp})")
        
        # Push στο GitHub (στο default branch, π.χ. main ή master)
        origin = repo.remote(name='origin')
        origin.push()
        
        print("[GitHub] Το γράφημα ανέβηκε επιτυχώς στο Open Repository σας!")
    except Exception as e:
        print(f"[GitHub Error] Αποτυχία ανεβάσματος: {e}")

if __name__ == "__main__":
    # Πρώτα φτιάχνουμε το γράφημα και αν πετύχει, το ανεβάζουμε
    if create_charts():
        upload_to_github()
