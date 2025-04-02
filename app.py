import streamlit as st
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, User, Task
from matching import TaskMatcher

# Database setup
engine = create_engine('sqlite:///tasks.db')
Session = sessionmaker(bind=engine)
session = Session()

# Initialize AI matcher
@st.cache_resource
def load_matcher():
    return TaskMatcher()

matcher = load_matcher()

# Streamlit app
def main():
    st.title("🦾 AI Task Allocation Dashboard")
    
    # Sidebar for adding entities
    with st.sidebar:
        st.header("➕ Add New")
        tab1, tab2 = st.tabs(["Task", "User"])
        
        with tab1:
            with st.form("task_form"):
                task_title = st.text_input("Task Title")
                task_desc = st.text_area("Description")
                task_skills = st.text_input("Required Skills (comma-separated)")
                task_people = st.number_input("People Required", min_value=1)
                if st.form_submit_button("Create Task"):
                    new_task = Task(
                        title=task_title,
                        description=task_desc,
                        required_skills=task_skills,
                        required_people=task_people,
                        status="open"
                    )
                    session.add(new_task)
                    session.commit()
                    st.success("Task created!")
        
        with tab2:
            with st.form("user_form"):
                user_name = st.text_input("Name")
                user_skills = st.text_input("Skills (comma-separated)")
                user_avail = st.selectbox("Availability", ["full-time", "shift1", "shift2"])
                user_cap = st.number_input("Daily Capacity (hours)", min_value=1)
                if st.form_submit_button("Add User"):
                    new_user = User(
                        name=user_name,
                        skills=user_skills,
                        availability=user_avail,
                        capacity=user_cap
                    )
                    session.add(new_user)
                    session.commit()
                    st.success("User added!")

    # Main dashboard
    col1, col2 = st.columns(2)
    
    with col1:
        st.header("📋 Open Tasks")
        tasks = session.query(Task).filter_by(status="open").all()
        for task in tasks:
            with st.expander(f"{task.title} (Needs {task.required_people} people)"):
                st.write(task.description)
                st.caption(f"Required skills: {task.required_skills}")
                if st.button("Auto-Assign", key=f"assign_{task.id}"):
                    # Implement your assignment logic here
                    st.success(f"Assigned {task.required_people} people to task!")
    
    with col2:
        st.header("👥 Team Overview")
        users = session.query(User).all()
        for user in users:
            st.write(f"**{user.name}**")
            st.progress(user.capacity/10)
            st.caption(f"Skills: {user.skills} | Availability: {user.availability}")

if __name__ == "__main__":
    main()