import streamlit as st
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, User, Task
from matching import TaskMatcher
import asyncio
import sys

# Fix for Windows event loop
if sys.platform == "win32" and hasattr(asyncio, "WindowsSelectorEventLoopPolicy"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# Database setup
engine = create_engine('sqlite:///tasks.db')
Session = sessionmaker(bind=engine)
session = Session()

# Initialize AI matcher
@st.cache_resource
def load_matcher():
    return TaskMatcher()

matcher = load_matcher()

def assign_task(task_id):
    try:
        task = session.query(Task).get(task_id)
        users = session.query(User).all()
        
        # Filter available users
        available_users = [
            u for u in users 
            if len(u.current_tasks) < u.capacity 
            and task.status == "open"
        ]
        
        # Calculate similarity scores
        matches = []
        for user in available_users:
            score = matcher.calculate_similarity(
                task.required_skills,
                user.skills
            )
            matches.append((user, score))
        
        # Sort and select top matches
        matches.sort(key=lambda x: x[1], reverse=True)
        selected = matches[:task.required_people]
        
        # Update database
        if len(selected) >= task.required_people:
            task.assigned_to = [u[0].id for u in selected]
            task.status = "in-progress"
            for user in selected:
                user.current_tasks.append(task.id)
            session.commit()
            return True, f"Assigned {task.required_people} people!"
        else:
            return False, "Not enough qualified users available"
            
    except Exception as e:
        return False, f"Error: {str(e)}"

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
                        capacity=user_cap,
                        current_tasks=[]
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
                    success, message = assign_task(task.id)
                    if success:
                        st.success(message)
                    else:
                        st.warning(message)
    
    with col2:
        st.header("👥 Team Overview")
        users = session.query(User).all()
        for user in users:
            st.write(f"**{user.name}**")
            st.progress(user.capacity/10)
            st.caption(f"Skills: {user.skills}")
            st.caption(f"Availability: {user.availability}")
            st.caption(f"Current tasks: {len(user.current_tasks)}/{user.capacity}")

if __name__ == "__main__":
    main()