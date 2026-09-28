from database import engine, Base, SessionLocal, ProjectModel

# Create all tables in the database
Base.metadata.create_all(bind=engine)

def seed_database():
    db = SessionLocal()
    
    if db.query(ProjectModel).first():
        print("Database already contains data!")
        db.close()
        return

    sample_projects = [
        ProjectModel(
            title="PortAce Idea Generator",
            tagline="An AI-powered project generator with customizable tech stack roadmaps.",
            difficulty="Intermediate",
            domain="Web Dev",
            tags=["Python", "FastAPI", "React", "Gemini API"],
            core_concepts=["REST API Design", "ORM Integration", "Prompt Engineering"]
        ),
        ProjectModel(
            title="Distributed Key-Value Store",
            tagline="In-memory cache with master-replica replication and persistent WAL logs.",
            difficulty="Advanced",
            domain="Systems",
            tags=["Python", "Sockets", "Concurrency"],
            core_concepts=["Network Protocols", "File I/O", "Concurrency"]
        ),
        ProjectModel(
            title="CLI Expense Tracker",
            tagline="Command-line tool to track spending and export monthly CSV reports.",
            difficulty="Beginner",
            domain="Web Dev",
            tags=["Python", "SQLite"],
            core_concepts=["CLI Interfaces", "Basic CRUD", "Data Processing"]
        )
    ]

    db.add_all(sample_projects)
    db.commit()
    print("Database seeded successfully with initial PortAce projects!")
    db.close()

if __name__ == "__main__":
    seed_database()