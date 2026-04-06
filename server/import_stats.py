import csv
import asyncio
import urllib.request
from server.database import stats_collection
from server.models.stats_model import StatModel

# Assuming they use the same base CSV URL but with the analytics GID '778618438' as defined in their .env
CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTIkQ1vLdYZ8zVaGZxh7YVMfIe017GVt6TEnuZoOIetKzLyXevlVm1gXhk0G6xS5ikAI2Ysp9skKAHv/pub?output=csv&gid=778618438"

async def main():
    try:
        print("Fetching Analytics CSV from Google Sheets...")
        response = urllib.request.urlopen(CSV_URL)
        lines = [l.decode('utf-8').strip() for l in response.readlines() if l.strip()]
        
        reader = csv.reader(lines)
        rows = list(reader)
        print(f"Fetched {len(rows)} rows.")
    except Exception as e:
        print("Error fetching CSV:", e)
        return

    print("Clearing old stats from the database...")
    await stats_collection.delete_many({})
    
    count = 0
    docs_to_insert = []
    # Skip header
    for row in rows[1:]:
        if len(row) == 0: continue
        page = row[0] if len(row) > 0 and row[0] else '/'
        timestamp = row[1] if len(row) > 1 and row[1] else ''
        session_id = row[2] if len(row) > 2 and row[2] else ''
        
        if not session_id or not timestamp:
            continue
            
        doc = {
            "page": page.strip(),
            "timestamp": timestamp.strip(),
            "sessionId": session_id.strip(),
            "referrer": None
        }
            
        try:
            model = StatModel(**doc)
            if hasattr(model, 'model_dump'):
                db_doc = model.model_dump(by_alias=True)
            else:
                db_doc = model.dict(by_alias=True)
            db_doc.pop('_id', None)
            docs_to_insert.append(db_doc)
        except Exception as e:
            pass
            
        if len(docs_to_insert) >= 5000:
            await stats_collection.insert_many(docs_to_insert)
            count += len(docs_to_insert)
            print(f"Inserted {count} records...")
            docs_to_insert = []
            
    if docs_to_insert:
        await stats_collection.insert_many(docs_to_insert)
        count += len(docs_to_insert)
    print(f"Successfully inserted {count} analytics records.")

if __name__ == "__main__":
    asyncio.run(main())
