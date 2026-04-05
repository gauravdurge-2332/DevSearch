import os
import django
import requests
import random
from django.core.files.base import ContentFile

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'devsearch.settings')
django.setup()

from django.contrib.auth.models import User
from users.models import Userprofile
from project.models import Project, Tags

def generate_dummy_projects(projects_per_user=2):
    project_archetypes = [
        ("E-commerce Platform", "A fully functional e-commerce system with cart and payment integration.", ["React", "Django", "PostgreSQL"]),
        ("Weather Dashboard", "Real-time weather tracking application using OpenWeather API.", ["JavaScript", "Python", "API"]),
        ("Crypto Portfolio", "A dashboard to track cryptocurrency holdings and market trends.", ["Next.js", "Node.js", "Blockchain"]),
        ("Personal Blog", "A modern blog engine with Markdown support and SEO optimization.", ["Python", "Django", "Bootstrap"]),
        ("Social Media App", "A platform for connecting developers and sharing code snippets.", ["React", "PostgreSQL", "TailwindCSS"]),
        ("Task Manager", "A productivity tool for managing team tasks and deadlines.", ["Django", "JavaScript", "Docker"]),
        ("Fitness Tracker", "An app to track workouts, calorie intake, and health metrics.", ["Mobile", "Python", "React"]),
        ("Expense Tracker", "A budgeting tool to visualize spending habits and savings goals.", ["Node.js", "Next.js", "PostgreSQL"]),
        ("Recipe Finder", "Search and discover new recipes based on available ingredients.", ["React", "API", "Bootstrap"]),
        ("Chat Application", "Real-time chat system with room management and file sharing.", ["Node.js", "JavaScript", "PostgreSQL"]),
        ("Job Board", "A platform for developers to find and apply for remote tech jobs.", ["Django", "Python", "AWS"]),
        ("Event Management", "Plan and organize virtual or in-person events seamlessly.", ["React", "Django", "TailwindCSS"]),
        ("Quiz Platform", "Interactive quiz system for testing technical knowledge.", ["JavaScript", "Python", "Docker"]),
        ("URL Shortener", "A tool to create and manage short, trackable links.", ["Node.js", "PostgreSQL", "API"]),
        ("AI Content Generator", "Generate high-quality content using advanced AI models.", ["Python", "Django", "API"]),
    ]

    profiles = Userprofile.objects.all()
    count = 0

    print(f"Starting generation of {len(profiles) * projects_per_user} dummy projects...")

    for profile in profiles:
        for i in range(projects_per_user):
            title_base, desc_base, tags_base = random.choice(project_archetypes)
            title = f"{title_base} - {random.randint(100, 999)}"
            description = f"{desc_base}. This project was built to demonstrate proficiency in modern web architecture and scalable design patterns."
            
            # 1. Create Project
            project = Project.objects.create(
                owner=profile,
                title=title,
                description=description,
                demo_link=f"https://demo.devsearch.com/{title.lower().replace(' ', '-')}",
                source_link=f"https://github.com/{profile.username}/{title.lower().replace(' ', '-')}",
            )

            # 2. Add Tags
            for t_name in tags_base:
                tag, created = Tags.objects.get_or_create(name=t_name)
                project.tags.add(tag)

            # 3. Download Thumbnail
            try:
                # Use a random picsum photo (800x600)
                img_id = random.randint(1, 1000)
                img_url = f"https://picsum.photos/id/{img_id}/800/600"
                response = requests.get(img_url, timeout=15)
                if response.status_code == 200:
                    project.featured_image.save(f"project_{project.id}.jpg", ContentFile(response.content), save=False)
            except Exception as e:
                print(f"Failed to download thumbnail for {title}: {e}")

            project.save()
            count += 1
            print(f"Generated project {count}/{len(profiles) * projects_per_user}: {title} for {profile.username}")

    print(f"Successfully generated {count} dummy projects!")

if __name__ == "__main__":
    generate_dummy_projects(2)
