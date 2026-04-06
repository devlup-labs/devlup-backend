import csv
import math
import asyncio
import urllib.request
from server.database import project_collection
from server.models.project_model import ProjectModel
from server.schemas.project_schema import MentorBase

# Google Sheets CSV URL
CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTIkQ1vLdYZ8zVaGZxh7YVMfIe017GVt6TEnuZoOIetKzLyXevlVm1gXhk0G6xS5ikAI2Ysp9skKAHv/pub?output=csv"

def is_nan(val):
    if isinstance(val, float) and math.isnan(val):
        return True
    return False

def clean_val(val):
    if is_nan(val):
        return None
    if isinstance(val, str):
        val = val.strip()
        if val == "":
            return None
    return val

async def main():
    try:
        print(f"Fetching CSV from Google Sheets...")
        response = urllib.request.urlopen(CSV_URL)
        lines = [l.decode('utf-8') for l in response.readlines()]
        reader = csv.DictReader(lines)
        data = list(reader)
        print(f"Fetched {len(data)} rows.")
    except Exception as e:
        print("Error fetching or parsing CSV:", e)
        return

    # Clear existing projects
    print("Clearing old projects from the database...")
    result = await project_collection.delete_many({})
    print(f"Deleted {result.deleted_count} projects.")

    for item in data:
        # Helper to get the first valid field from a list of possible column names
        def get_field(names):
            for n in names:
                if item.get(n):
                    return clean_val(item[n])
            return None

        project_title = get_field(["Project Name"])
        project_description = get_field(["description", "Description"])
        
        if not project_title or not project_description:
            print("Skipping entry due to missing title or description:", project_title or "Unknown")
            continue

        raw_tech_stack = get_field(["Tech Stack (Comma separated)", "Tech Stack (Comma rated)"])
        tech_stack = [t.strip() for t in raw_tech_stack.split(",")] if raw_tech_stack else []

        # Extract mentors
        mentors = []
        for i in range(1, 4):
            m_name = get_field([f"Mentor {i} Name"])
            if m_name:
                m_email = get_field([f"Mentor {i} Email", f"Mentor {i} Mail"])
                m_linkedin = get_field([f"Mentor {i} LinkedIn Url", f"Mentor {i} LinkedIn"])
                m_github = get_field([f"Mentor {i} Github Url", f"Mentor {i} Github"])
                mentors.append(MentorBase(
                    name=m_name,
                    role="Project Mentor",
                    email=m_email,
                    linkedin=m_linkedin,
                    github=m_github
                ))

        # Industry Mentor
        ind_mentor = None
        ind_name = get_field(["Industry Mentor", "Industry mentor"])
        if ind_name:
            ind_email = get_field(["Industry Mentor Mail", "Industry Mentor Email"])
            ind_linkedin = get_field(["Industry Mentor LinkedIn", "Industry Mentor LinkedIn Url"])
            ind_mentor = MentorBase(
                name=ind_name,
                role="Industry Mentor",
                email=ind_email,
                linkedin=ind_linkedin
            )

        category = get_field(["Category"]) or ""
        project_type = "woc" if "woc" in category.lower() else "soc"
        
        status = get_field(["Status"]) or "ongoing"
        if status:
            status = status.lower()

        timestamp_str = get_field(["Timestamp"])
        year = 2025 # Default
        if timestamp_str:
            try:
                # "5/13/2025 0:05:44"
                parts = timestamp_str.split("/")
                if len(parts) >= 3:
                     year_str = parts[2].split(" ")[0]
                     year = int(year_str)
            except Exception:
                pass
                
        raw_live_links = get_field(["Live links", "Live Links", "Live Links (comma separated)"])
        live_links = [l.strip() for l in raw_live_links.split(",")] if raw_live_links else []
        preview_link = live_links[0] if live_links else None

        current_desc = get_field(["Current Desc", "Current Description"])
        github_repo = get_field(["Project Github", "Project GitHub", "Project Git Repo"])
        docs = get_field(["Project Doc"])
        recommended = get_field(["Recommended", "Difficulty"])

        project = {
            "project_title": project_title,
            "project_description": project_description,
            "status": status,
            "type": project_type,
            "year": year,
            "preview_link": preview_link,
            "github_repo_link": github_repo,
            "docs": docs,
            "has_issues": False,
            "tech_stack": tech_stack,
            "mentors": mentors,
            "industry_mentor": ind_mentor,
            "category": category,
            "current_desc": current_desc,
            "live_links": live_links,
            "recommended": recommended
        }
        
        try:
            model = ProjectModel(**project)
            doc = {}
            if hasattr(model, 'model_dump'):
                doc = model.model_dump(by_alias=True)
            else:
                doc = model.dict(by_alias=True)
            doc.pop('_id', None)
            
            await project_collection.insert_one(doc)
            print(f"Inserted project: {model.project_title}")
        except Exception as e:
            print(f"Failed to insert '{project_title}': {e}")

if __name__ == "__main__":
    asyncio.run(main())
