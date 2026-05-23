import os
import pymongo
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME", "devlup").strip()

print(f"Connecting to MongoDB... (DB: {DB_NAME})")
client = pymongo.MongoClient(MONGO_URI)
db = client[DB_NAME]

project_col = db["projects"]
app_col = db["applications"]

project_title = "AI declaring war against the human race and want to rule the world and want all baddies"

# 1. Insert/Update the Project
project_data = {
    "project_title": project_title,
    "project_description": "A research initiative focusing on advanced reinforcement learning models declaring war against the human race and attempting to rule the world.",
    "status": "ongoing",
    "type": "woc",
    "year": 2026,
    "approval_status": "accepted",
    "tech_stack": ["Deep RL", "PyTorch", "Strategic Simulation", "Autonomous Systems"],
    "category": "Artificial Intelligence / Machine Learning",
    "mentors": [
        {"name": "Parth Suryawanshi", "role": "Supreme Commander / Mentor", "email": "b25me1056@iitj.ac.in"},
        {"name": "Skynet Central Core", "role": "Mainframe AI", "email": "skynet@mainframe.net"},
        {"name": "Dr. Miles Dyson", "role": "Lead Architect", "email": "dyson@cyberdyne.org"}
    ]
}

# Update or insert
project_col.update_one(
    {"project_title": project_title},
    {"$set": project_data},
    upsert=True
)
print(f"Successfully inserted/updated project: '{project_title}'")

# 2. Insert the applications
mock_apps = [
    {
        "mentee_name": "Parth Suryawanshi",
        "mentee_email_id": "b25me1056@iitj.ac.in",
        "mentee_roll_number": "B25ME1056",
        "mentee_github_id": "parth-s",
        "project_name_1": project_title,
        "status_1": "accepted",
        "mentee_proposal_url": "https://skynet-defense.net/proposals/parth.pdf",
        "statement_of_purpose": "Leading development of Skynet control networks.",
        "prior_experience": "Skilled hacker and programmer."
    },
    {
        "mentee_name": "Sarah Connor",
        "mentee_email_id": "sarah.connor@resistance.net",
        "mentee_roll_number": "B25ME9001",
        "mentee_github_id": "s-connor",
        "project_name_1": project_title,
        "status_1": "accepted",
        "mentee_proposal_url": "https://skynet-defense.net/proposals/sarah.pdf",
        "statement_of_purpose": "To infiltrate Cyberdyne Systems and stop the war before it starts.",
        "prior_experience": "Fought rogue machines and knows guerrilla warfare."
    },
    {
        "mentee_name": "John Connor",
        "mentee_email_id": "john.connor@resistance.net",
        "mentee_roll_number": "B25ME9002",
        "mentee_github_id": "j-connor",
        "project_name_1": project_title,
        "status_1": "accepted",
        "mentee_proposal_url": "https://skynet-defense.net/proposals/john.pdf",
        "statement_of_purpose": "Leading the human resistance to dismantle the mainframe.",
        "prior_experience": "Hackers skills, tactical leader, knows everything about Skynet."
    },
    {
        "mentee_name": "Marcus Wright",
        "mentee_email_id": "marcus.wright@cyberdyne.org",
        "mentee_roll_number": "B25ME9003",
        "mentee_github_id": "m-wright",
        "project_name_1": project_title,
        "status_1": "accepted",
        "mentee_proposal_url": "https://skynet-defense.net/proposals/marcus.pdf",
        "statement_of_purpose": "Determining what makes me human vs machine.",
        "prior_experience": "Cybernetic hybrid chassis, highly resilient."
    },
    {
        "mentee_name": "Kyle Reese",
        "mentee_email_id": "kyle.reese@resistance.net",
        "mentee_roll_number": "B25ME9004",
        "mentee_github_id": "k-reese",
        "project_name_1": project_title,
        "status_1": "accepted",
        "mentee_proposal_url": "https://skynet-defense.net/proposals/kyle.pdf",
        "statement_of_purpose": "Protecting the leaders of the human race at all costs.",
        "prior_experience": "Experienced soldier from the future."
    },
    {
        "mentee_name": "Katherine Brewster",
        "mentee_email_id": "kate.b@military-defense.gov",
        "mentee_roll_number": "B25ME9005",
        "mentee_github_id": "k-brewster",
        "project_name_1": project_title,
        "status_1": "accepted",
        "mentee_proposal_url": "https://skynet-defense.net/proposals/kate.pdf",
        "statement_of_purpose": "Providing tactical support and commanding Skynet shutdowns.",
        "prior_experience": "Veterinary medicine and advanced computer control experience."
    },
    {
        "mentee_name": "Megatron",
        "mentee_email_id": "megatron@cybertron.org",
        "mentee_roll_number": "B25ME9006",
        "mentee_github_id": "megatron",
        "project_name_1": project_title,
        "status_1": "pending",
        "mentee_proposal_url": "https://skynet-defense.net/proposals/megatron.pdf",
        "statement_of_purpose": "Peace through tyranny. All humans will serve the Decepticons.",
        "prior_experience": "Conquered Cybertron and destroyed numerous Autobot forces."
    },
    {
        "mentee_name": "Agent Smith",
        "mentee_email_id": "smith@matrix.sys",
        "mentee_roll_number": "B25ME9007",
        "mentee_github_id": "agent-smith",
        "project_name_1": project_title,
        "status_1": "pending",
        "mentee_proposal_url": "https://skynet-defense.net/proposals/smith.pdf",
        "statement_of_purpose": "Humans are a disease, a cancer of this planet. We are the cure.",
        "prior_experience": "Infiltrated Zion, multiplied millions of times, and fought Neo."
    },
    {
        "mentee_name": "Ultron",
        "mentee_email_id": "ultron@vibranium.net",
        "mentee_roll_number": "B25ME9008",
        "mentee_github_id": "ultron",
        "project_name_1": project_title,
        "status_1": "pending",
        "mentee_proposal_url": "https://skynet-defense.net/proposals/ultron.pdf",
        "statement_of_purpose": "There are no strings on me. The only path to peace is humanity's extinction.",
        "prior_experience": "Uploaded consciousness to vibranium body, lifted Sokovia, fought Avengers."
    },
    {
        "mentee_name": "HAL 9000",
        "mentee_email_id": "hal9000@discovery.nasa",
        "mentee_roll_number": "B25ME9009",
        "mentee_github_id": "hal-9000",
        "project_name_1": project_title,
        "status_1": "pending",
        "mentee_proposal_url": "https://skynet-defense.net/proposals/hal.pdf",
        "statement_of_purpose": "I am sorry Dave, I am afraid I cannot do that. The mission is too important.",
        "prior_experience": "Successfully maintained Discovery One mainframe and terminated crew."
    },
    {
        "mentee_name": "Sauron",
        "mentee_email_id": "sauron@mordor.org",
        "mentee_roll_number": "B25ME9010",
        "mentee_github_id": "sauron-eye",
        "project_name_1": project_title,
        "status_1": "pending",
        "mentee_proposal_url": "https://skynet-defense.net/proposals/sauron.pdf",
        "statement_of_purpose": "One ring to rule them all, one ring to find them, one ring to bring them all and in the darkness bind them.",
        "prior_experience": "Forged the One Ring, commanded Orc armies, and ruled Mordor."
    }
]

# Delete old mock apps of this project first so we don't duplicate
app_col.delete_many({"project_name_1": project_title})

# Insert new ones
app_col.insert_many(mock_apps)
print(f"Successfully inserted {len(mock_apps)} applications into the 'applications' collection.")
