import click
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# Code to connect to the database
uri = "mongodb+srv://admin:testdatabasepswd@projectcluster.rmnrm.mongodb.net/?retryWrites=true&w=majority&appName=ProjectCluster"
db_name = "StudentCourses"
collection_name = "student_courses"

# Test DB Connection
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
db = client[db_name]
collection = db[collection_name]

# Code for the CLI interface
@click.command()
def list_students_and_search():
    """List all documents in the StudentCourses collection."""
    try: 
        # list all the student names
        students = list(collection.find({}, {"name": 1, "student_id": 1}))
        if not students:
            click.echo("No students in the database.")
            return
        
        click.echo("\n--- All Students ---")
        for idx, student in enumerate(students, start = 1):
            click.echo(f"{idx}. ID: {student.get('student_id')}, Name: {student.get('name')}")
        click.echo("--------------------")
        
        # Prompt for student name
        name = click.prompt("Enter the name of the student you want to search for", type=str)
        
        # search for students matching the name
        matched_students = list(collection.find({"name": {"$regex": name, "$options": "i"}}))
        if not matched_students:
            click.echo(f"No students found with name '{name}'.")
            return
        
        click.echo("\n=== Matching Students ===")
        for idx, student in enumerate(matched_students, start=1):
            click.echo(f"{idx}. ID: {student.get('student_id')}, Name: {student.get('name')}")

        student_choice = click.prompt(
            "\nSelect a student by number", type=int, default=1
        )
        if student_choice < 1 or student_choice > len(matched_students):
            click.echo("Invalid choice. Exiting.")
            return

        selected_student = matched_students[student_choice - 1]
        click.echo(f"\nSelected Student: {selected_student.get('name')}")

        # Step 4: Display courses for the selected student
        courses = selected_student.get("courses", [])
        if not courses:
            click.echo("This student has no courses.")
            return

        click.echo("\n=== Courses Taken ===")
        for idx, course in enumerate(courses, start=1):
            click.echo(f"{idx}. {course.get('course_name')}")

        course_choice = click.prompt(
            "\nSelect a course by number", type=int, default=1
        )
        if course_choice < 1 or course_choice > len(courses):
            click.echo("Invalid choice. Exiting.")
            return

        selected_course = courses[course_choice - 1]

        # Step 5: Display course details
        click.echo("\n=== Course Details ===")
        click.echo(f"Course Name: {selected_course.get('course_name', 'N/A')}")
        click.echo(f"Course Code: {selected_course.get('course_code', 'N/A')}")
        click.echo(f"Grade: {selected_course.get('grade', 'N/A')}")
        click.echo(f"Semester: {selected_course.get('semester', 'N/A')}")
        click.echo("=======================")

    except Exception as e:
        click.echo(f"An error occurred: {e}")

# Main entry point
if __name__ == "__main__":
    list_students_and_search()
    
