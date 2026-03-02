import asyncio
from api import clean_files

def main():
    asyncio.run(clean_files())

if __name__ == "__main__":
    main()
