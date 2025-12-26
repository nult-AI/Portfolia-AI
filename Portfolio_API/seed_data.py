"""
Seed initial data for Portfolio API
Run this script once to populate the database with sample data
"""
from app.core.database import SessionLocal
from app.models.models import (
    Profile, SkillCategory, Skill, OtherSkill,
    Experience, ExperienceDuty, ExperienceDomain, Education
)

def seed_data():
    db = SessionLocal()
    
    try:
        # Check if data already exists
        existing_profile = db.query(Profile).first()
        if existing_profile:
            print("⚠️  Data already exists. Skipping seed.")
            return
        
        print("🌱 Seeding initial data...")
        
        # Create Profile
        profile = Profile(
            name="MINH NHAT, LE",
            role="Senior Full Stack .NET, React | Lead / Senior Software Engineer",
            bio="Chuyên gia phát triển hệ thống .NET Full Stack với hơn 14 năm kinh nghiệm. Có khả năng dẫn dắt đội ngũ lớn (hơn 11 người), thiết kế kiến trúc hệ thống từ Monolith đến Microservices, và triển khai trên các nền tảng Cloud hiện đại như AWS, Azure.",
            email="nult2003@gmail.com",
            phone="0982 880 258",
            location="33/47 Street 4, Binh Hung Hoa Ward, Ho Chi Minh City, Viet Nam",
            skype="nult2003@gmail.com",
            linkedin_url="https://www.linkedin.com/in/minh-nhat-le-a9638919/",
        )
        db.add(profile)
        
        # Create Skill Categories and Skills
        categories_data = {
            "Programming Languages": ["C#", "HTML", "CSS", "SASS", "JavaScript", "TypeScript", "SQL"],
            "Frameworks": ["MVC", "Entity Framework", "KnockoutJS", "VueJS", "React", ".NET Core Web API", "WCF", "WPF", "NUnit"],
            "Architect/Pattern": ["Repository pattern", "Microservices (RabbitMQ)", "Web Single Page", "MVC Architecture"],
            "ORM/Tools": ["Automapper", "Dapper", "Slapper", "Git", "Jira", "BitBucket", "Azure", "Visual Studio"],
            "Cloud/Infra": ["Docker", "Kubernetes (EKS)", "Terraform", "SAM", "EC2", "S3", "Minikube", "LENS"]
        }
        
        for idx, (category_name, skills) in enumerate(categories_data.items()):
            category = SkillCategory(name=category_name, display_order=idx)
            db.add(category)
            db.flush()  # Get the ID
            
            for skill_name in skills:
                skill = Skill(name=skill_name, category_id=category.id)
                db.add(skill)
        
        # Create Other Skills
        other_skills_data = [
            "Training interns",
            "Analyze requirements from tickets/customers",
            "Leadership (Lead team over 11 members)",
            "Problem solving & Analytical thinking",
            "Excellent framework building skills (BE/FE)"
        ]
        
        for skill_name in other_skills_data:
            other_skill = OtherSkill(name=skill_name)
            db.add(other_skill)
        
        # Create Experiences
        exp1 = Experience(
            company_name="TMA Company",
            role="Senior/Lead .NET Full Stack",
            period_display="2020 - Hiện tại",
            tech_stack="C#, Oracle, .NET Core Web API, Automapper, Entity Framework, Repository pattern, React, Redux, AWS S3, TypeScript"
        )
        db.add(exp1)
        db.flush()
        
        # Add duties for exp1
        duties1 = [
            "Làm việc với các dự án từ Canada và Ấn Độ theo quy trình Agile.",
            "Phát triển ứng dụng dựa trên React và .NET Core API.",
            "Review code, Unit Test và quản lý mã nguồn qua Bitbucket.",
            "Quản lý team hơn 11 người, phân chia công việc và theo dõi tiến độ.",
            "Thảo luận trực tiếp với khách hàng về yêu cầu nghiệp vụ."
        ]
        for duty in duties1:
            db.add(ExperienceDuty(description=duty, experience_id=exp1.id))
        
        # Add domains for exp1
        domains1 = ["Network design management", "Clinical management"]
        for domain in domains1:
            db.add(ExperienceDomain(name=domain, experience_id=exp1.id))
        
        # Experience 2
        exp2 = Experience(
            company_name="XSPERA Company",
            role="Senior .NET Full Stack",
            period_display="09/2018 - 2020",
            tech_stack="C#, SQL Server, .NET Core Web API, Automapper, Dapper, Entity Framework, React, Redux, Vue, TypeScript, Rabbit MQ"
        )
        db.add(exp2)
        db.flush()
        
        duties2 = [
            "Phân tích yêu cầu từ bộ phận kinh doanh để xây dựng ứng dụng với công nghệ phù hợp.",
            "Phát triển ứng dụng trên nền tảng SharePoint (On-premise & Online) kết hợp React và .NET Core.",
            "Tổ chức các buổi họp brainstorm để tìm kiếm giải pháp kỹ thuật tối ưu."
        ]
        for duty in duties2:
            db.add(ExperienceDuty(description=duty, experience_id=exp2.id))
        
        domains2 = ["Web portal (Sharepoint)", "Logistic management"]
        for domain in domains2:
            db.add(ExperienceDomain(name=domain, experience_id=exp2.id))
        
        # Create Education
        education = Education(
            school="Post and Telecommunication Institute of Technology",
            degree="Engineer's Degree",
            major="Software Engineer"
        )
        db.add(education)
        
        db.commit()
        print("✅ Seed data created successfully!")
        print("\nCreated:")
        print("  - 1 Profile")
        print(f"  - {len(categories_data)} Skill Categories")
        print(f"  - {sum(len(skills) for skills in categories_data.values())} Skills")
        print(f"  - {len(other_skills_data)} Other Skills")
        print("  - 2 Experiences")
        print("  - 1 Education")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error seeding data: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()
