def mentor_serializer(mentor) -> dict:
    return{
        "id": str(mentor["_id"]),
        "name": mentor["name"],
        "github": mentor["github"],
        "email": mentor["email"],
        "description": mentor["description"],
        "linkedin": mentor["linkedin"],
        "image": mentor["image"],
        "role": mentor["role"],
        "year": mentor["year"]  
    }