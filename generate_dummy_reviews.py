import os
import django
import random

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'devsearch.settings')
django.setup()

from django.contrib.auth.models import User
from users.models import Userprofile
from project.models import Project, Review

def generate_dummy_reviews():
    profiles = list(Userprofile.objects.all())
    projects = Project.objects.all()
    
    review_templates = [
        "Amazing work! The code is clean and well-structured.",
        "Really loved the UI/UX of this project. Keep it up!",
        "Great implementation of the backend logic. Very scalable.",
        "The documentation could be a bit better, but the overall project is solid.",
        "Excellent use of modern tech stack. Inspired by this!",
        "Functional and efficient. I'll definitely be checking out the source code.",
        "Simple yet effective. Solves a real problem.",
        "Not bad, but I think the mobile responsiveness could be improved.",
        "Impressive project! I'd love to collaborate on something similar.",
        "Standard implementation, but the design is quite nice."
    ]

    print(f"Generating random reviews for {projects.count()} projects...")

    for project in projects:
        # Generate 1-5 random reviews for each project
        num_reviews = random.randint(1, 5)
        
        # Pick random profiles to be the reviewers (excluding the project owner)
        potential_reviewers = [p for p in profiles if p != project.owner]
        reviewers = random.sample(potential_reviewers, min(num_reviews, len(potential_reviewers)))

        for reviewer in reviewers:
            # Avoid duplicate reviews for the same project/owner combo
            if not Review.objects.filter(owner=reviewer, project=project).exists():
                value = random.choices(["up", "down"], weights=[85, 15])[0]  # 85% chance of up-vote
                Review.objects.create(
                    owner=reviewer,
                    project=project,
                    value=value,
                    body=random.choice(review_templates)
                )
        
        # Trigger vote recount
        project.getcountvote
        project.save()

    print("Success! All projects now have dynamic ratings.")

if __name__ == "__main__":
    generate_dummy_reviews()
