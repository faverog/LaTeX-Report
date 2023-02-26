# Function to handle button click event
def submit_entries(entries, window):
    for i in range(len(entries)):
        print(f"Entry {i+1}: {entries[i].get()}")
    window