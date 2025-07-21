#!/usr/bin/env python
import sys
import warnings

from datetime import datetime

from my_stock_picker.crew import MyStockPicker

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

def run():
    """
    Run the crew.
    """
    inputs = {
        'sector': 'Technology'
    }
    
    result = MyStockPicker().crew().kickoff(inputs=inputs)

    print("\n\n=== FINAL DECISION ===\n\n")
    print(result.raw)

if __name__ == "__main__":
    run()
