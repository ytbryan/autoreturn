from autoreturn import autoreturn

@autoreturn
def example():
    x = 10 + 20
    x * 2  # Last expression, will be returned automatically

if __name__ == "__main__":
    print(example())