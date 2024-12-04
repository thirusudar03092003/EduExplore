from flask import Flask, request, jsonify
from flask_cors import CORS
from difflib import get_close_matches

app = Flask(__name__)
CORS(app)

# Sample course data (same as before)
courses = [
    {'id': 1, 'name': 'Introduction to Python Programming', 'instructor': 'Dr. Smith', 'description': 'Learn Python basics.', 'price': 49.99, 'category': 'Programming'},
    {'id': 2, 'name': 'Advanced Machine Learning', 'instructor': 'Prof. Johnson', 'description': 'Deep dive into machine learning algorithms.', 'price': 79.99, 'category': 'Data Science'},
    {'id': 3, 'name': 'Web Development Bootcamp', 'instructor': 'Sarah Wilson', 'description': 'Become a full-stack web developer.', 'price': 59.99, 'category': 'Web Development'},
    {'id': 4, 'name': 'Data Analysis with R', 'instructor': 'John Doe', 'description': 'Analyze data with R programming.', 'price': 39.99, 'category': 'Data Science'},
    {'id': 5, 'name': 'UX/UI Design Fundamentals', 'instructor': 'Jane Smith', 'description': 'Learn the basics of UX/UI design.', 'price': 49.99, 'category': 'Design'},
    {'id': 6, 'name': 'Digital Marketing 101', 'instructor': 'Emily Johnson', 'description': 'Learn digital marketing strategies.', 'price': 29.99, 'category': 'Business'},
    {'id': 7, 'name': 'Java Programming for Beginners', 'instructor': 'Mark Wilson', 'description': 'Master the basics of Java programming.', 'price': 44.99, 'category': 'Programming'},
    {'id': 8, 'name': 'React and Redux Crash Course', 'instructor': 'Angela Lee', 'description': 'Build modern web apps with React and Redux.', 'price': 59.99, 'category': 'Web Development'},
    {'id': 9, 'name': 'AI in Healthcare', 'instructor': 'Dr. Brown', 'description': 'Explore the role of AI in the healthcare industry.', 'price': 89.99, 'category': 'Data Science'},
    {'id': 10, 'name': 'Ethical Hacking Basics', 'instructor': 'Hacker Joe', 'description': 'Understand cybersecurity fundamentals.', 'price': 69.99, 'category': 'Cybersecurity'},
    {'id': 11, 'name': 'Cloud Computing Essentials', 'instructor': 'Mary Anne', 'description': 'An overview of cloud technologies.', 'price': 54.99, 'category': 'IT'},
    {'id': 12, 'name': 'Blockchain Technology', 'instructor': 'Satoshi Nakamoto', 'description': 'Learn blockchain basics.', 'price': 79.99, 'category': 'Technology'},
    {'id': 13, 'name': 'Basics of Graphic Design', 'instructor': 'Michael Angelo', 'description': 'Create stunning visuals.', 'price': 39.99, 'category': 'Design'},
    {'id': 14, 'name': 'SQL for Beginners', 'instructor': 'Data Guru', 'description': 'Master database querying.', 'price': 34.99, 'category': 'Data Science'},
    {'id': 15, 'name': 'AWS Certification Prep', 'instructor': 'Amazon Expert', 'description': 'Prepare for AWS certification exams.', 'price': 99.99, 'category': 'Cloud'},
    {'id': 16, 'name': 'Introduction to Robotics', 'instructor': 'Dr. Robo', 'description': 'Dive into robotics fundamentals.', 'price': 89.99, 'category': 'Technology'},
    {'id': 17, 'name': 'SEO Mastery', 'instructor': 'Emily Marketing', 'description': 'Boost your website traffic.', 'price': 45.99, 'category': 'Business'},
    {'id': 18, 'name': 'Cybersecurity for Beginners', 'instructor': 'Cyber Expert', 'description': 'Understand basic cybersecurity principles.', 'price': 49.99, 'category': 'Cybersecurity'},
    {'id': 19, 'name': 'Mobile App Development', 'instructor': 'App Maker', 'description': 'Create mobile apps from scratch.', 'price': 74.99, 'category': 'Programming'},
    {'id': 20, 'name': '3D Modeling Basics', 'instructor': '3D Pro', 'description': 'Learn 3D design principles.', 'price': 59.99, 'category': 'Design'}
]


categories = ['Programming', 'Data Science', 'Web Development', 'Business', 'Design', 'Cybersecurity', 'IT', 'Technology', 'Cloud']

# Function to find similar courses based on category and description
def find_similar_courses(course_id):
    target_course = next(course for course in courses if course['id'] == course_id)
    similar_courses = []

    # Match by category
    category_matches = [course for course in courses if course['category'] == target_course['category'] and course['id'] != course_id]
    similar_courses.extend(category_matches)

    # Match by description using difflib to find similar descriptions
    description_matches = get_close_matches(target_course['description'], [course['description'] for course in courses], n=5, cutoff=0.6)
    for description in description_matches:
        similar_courses.extend([course for course in courses if course['description'] == description and course['id'] != course_id])

    # Remove duplicates by converting to a set and back to a list
    return list({course['id']: course for course in similar_courses}.values())

@app.route('/api/courses', methods=['GET'])
def get_courses():
    query = request.args.get('query', '').lower()
    category = request.args.get('category', '').lower()
    filtered_courses = courses

    if query:
        filtered_courses = [
            course for course in filtered_courses
            if query in course['name'].lower() or query in course['description'].lower()
        ]
    if category:
        filtered_courses = [
            course for course in filtered_courses
            if course['category'].lower() == category
        ]

    return jsonify({
        'status': 'success',
        'total': len(filtered_courses),
        'data': filtered_courses,
        'categories': categories
    })

@app.route('/api/recommendations/<int:course_id>', methods=['GET'])
def get_recommendations(course_id):
    recommended_courses = find_similar_courses(course_id)
    return jsonify({
        'status': 'success',
        'data': recommended_courses
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
