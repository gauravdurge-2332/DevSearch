import os
import django
import requests
import random
from django.core.files.base import ContentFile

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'devsearch.settings')
django.setup()

from django.contrib.auth.models import User
from users.models import Userprofile, Skills

def cleanup_old_dummies():
    """Delete all users except superusers to ensure a clean start."""
    print("Cleaning up old dummy accounts...")
    User.objects.filter(is_superuser=False).delete()
    print("Old accounts cleared.")

def generate_improved_dummies(count=25):
    male_names = [
        ("Aakash", "Sharma"), ("Arjun", "Kulkarni"), ("Vikram", "Reddy"), ("Rahul", "Patel"), ("Karan", "Joshi"),
        ("James", "Smith"), ("Robert", "Brown"), ("Michael", "Johnson"), ("David", "Williams"), ("Oliver", "Twist"),
        ("Alexander", "TheGreat"), ("Sebastian", "Vettel"), ("Ethan", "Hunt")
    ]
    female_names = [
        ("Deepa", "Verma"), ("Anjali", "Deshmukh"), ("Meera", "Choudhury"), ("Neha", "Nair"), ("Pooja", "Gupta"),
        ("Emily", "Davies"), ("Sophie", "Miller"), ("Chloe", "Wilson"), ("Isabella", "Garcia"), ("Mia", "Anderson"),
        ("Charlotte", "Thomas"), ("Amelia", "White")
    ]
    
    titles = [
        "Fullstack Developer", "Backend Engineer", "Frontend Specialist", "AI Enthusiast", 
        "Python Scripter", "Mobile App Dev", "DevOps Engineer", "Cloud Architect",
        "Cybersecurity Analyst", "UI/UX Designer", "Blockchain Developer", "Data Scientist"
    ]
    
    skills_list = ["Python", "JavaScript", "React", "Django", "Node.js", "PostgreSQL", "AWS", "Docker", "Git"]

    # 50/50 Split (approximate)
    males_to_create = 13
    females_to_create = 12

    print(f"Generating {count} gender-matched dummy accounts...")

    # Combine names into a list of tuples: (First, Last, Gender)
    combined_names = [(m[0], m[1], 'male') for m in male_names[:males_to_create]] + \
                     [(f[0], f[1], 'female') for f in female_names[:females_to_create]]
    
    random.shuffle(combined_names)

    for fname, lname, gender in combined_names:
        username = f"{fname.lower()}_{lname.lower()}_{random.randint(100, 999)}"
        email = f"{username}@devsearch.com"
        password = "dummyPass123"

        # 1. Create User
        user = User.objects.create_user(username=username, email=email, password=password, first_name=fname, last_name=lname)
        print(f"Created {gender} user: {username}")

        # 2. Update Profile
        profile = user.userprofile
        profile.name = f"{fname} {lname}"
        profile.short_note = random.choice(titles)
        profile.bio = f"Hi, I'm {fname}! I'm a {profile.short_note} who loves tackling complex architectural challenges."
        profile.location = random.choice(['London', 'New York', 'San Francisco', 'Bangalore', 'Berlin', 'Tokyo'])
        
        profile.social_github = f"https://github.com/{username}"
        profile.social_linkedin = f"https://linkedin.com/in/{username}"

        # 3. Download Gender-Matched Image
        try:
            # Using xsgames which has a direct gender-specific endpoint
            img_url = f"https://xsgames.co/randomusers/assets/avatars/{gender}/{random.randint(0, 75)}.jpg"
            response = requests.get(img_url, timeout=10)
            if response.status_code == 200:
                profile.profile_img.save(f"{username}.jpg", ContentFile(response.content), save=False)
        except Exception as e:
            print(f"Failed to download image for {username}: {e}")

        profile.save()

        # 4. Add Skills
        random_skills = random.sample(skills_list, 3)
        for s_name in random_skills:
            Skills.objects.create(
                owner=profile,
                name=s_name,
                Description=f"Highly proficient in {s_name} with multiple successful deployments."
            )

    print("Success! 25 gender-matched accounts are now LIVE.")

if __name__ == "__main__":
    cleanup_old_dummies()
    generate_improved_dummies(25)
