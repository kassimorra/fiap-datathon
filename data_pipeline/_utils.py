def load_all(*ProcessClass) -> None:
    for ProcessCls in ProcessClass:
        process = ProcessCls()
        process.run()

def print_status(stats: str) -> None:
    print(f"\n--- {stats} ---")