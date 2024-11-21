import os
import shutil
import pandas as pd
import streamlit as st

# Helper function to process seating allocation
def allocate_seating(input_file):
    ip_1 = pd.read_excel(input_file, sheet_name="ip_1")
    ip_2 = pd.read_excel(input_file, sheet_name="ip_2")
    ip_3 = pd.read_excel(input_file, sheet_name="ip_3")
    
    buffer = 0  # Buffer space per room
    dense_mode = False  # Control seating density
    max_fill = 1.0 if dense_mode else 0.5  # Max seat fill percentage

    # Prepare data mappings
    course_roll_mapping = ip_1.groupby("course_code")["rollno"].apply(list).to_dict()
    exam_schedule = ip_2.set_index("Date").to_dict(orient="index")
    rooms = ip_3.sort_values(by=["Block", "Exam Capacity"], ascending=[True, False])
    room_capacity = rooms.set_index("Room No.")["Exam Capacity"].to_dict()
    room_block = rooms.set_index("Room No.")["Block"].to_dict()

    initial_room_capacity = room_capacity.copy()
    seating_plan = []
    vacancy_details = []

    # Process each exam session
    for date, schedule in exam_schedule.items():
        for session in ["Morning", "Evening"]:
            if pd.isna(schedule[session]) or schedule[session] == "NO EXAM":
                continue

            vacant_rooms_block9 = {room: capacity - buffer for room, capacity in room_capacity.items() if room_block[room] == 9}
            vacant_rooms_lt = {room: capacity - buffer for room, capacity in room_capacity.items() if room_block[room] != 9}
            courses = schedule[session].split("; ")
            courses.sort(key=lambda c: len(course_roll_mapping.get(c, [])), reverse=True)

            for course in courses:
                rolls = course_roll_mapping.get(course, [])
                total_students = len(rolls)
                if total_students == 0:
                    continue

                allocated_rolls = []
                # Allocate seats in Block 9 rooms first
                for room, capacity in list(vacant_rooms_block9.items()):
                    max_alloc = int(initial_room_capacity[room] * max_fill)
                    alloc = min(total_students, max_alloc)
                    allocated_rolls.extend(rolls[:alloc])
                    rolls = rolls[alloc:]
                    total_students -= alloc
                    seating_plan.append([date, schedule["Day"], session, course, room, alloc, ";".join(allocated_rolls)])
                    vacant_rooms_block9[room] -= alloc
                    if vacant_rooms_block9[room] <= 0:
                        del vacant_rooms_block9[room]
                    if total_students == 0:
                        break

                # Allocate remaining students in other rooms
                if total_students > 0:
                    allocated_rolls = []
                    for room, capacity in list(vacant_rooms_lt.items()):
                        max_alloc = int(initial_room_capacity[room] * max_fill)
                        alloc = min(total_students, max_alloc)
                        allocated_rolls.extend(rolls[:alloc])
                        rolls = rolls[alloc:]
                        total_students -= alloc
                        seating_plan.append([date, schedule["Day"], session, course, room, alloc, ";".join(allocated_rolls)])
                        vacant_rooms_lt[room] -= alloc
                        if vacant_rooms_lt[room] <= 0:
                            del vacant_rooms_lt[room]
                        if total_students == 0:
                            break

                if total_students > 0:
                    course_roll_mapping[course] = rolls
                else:
                    del course_roll_mapping[course]

            # Track room vacancies
            vacancy_details.extend([
                [date, schedule["Day"], session, room, initial_room_capacity[room], room_block[room], vacant_rooms_block9.get(room, vacant_rooms_lt.get(room, 0))]
                for room in room_capacity
            ])

    seating_df = pd.DataFrame(seating_plan, columns=["Date", "Day", "Session", "course_code", "Room", "Allocated_students_count", "Roll_list"])
    seating_df["Date"] = pd.to_datetime(seating_df["Date"]).dt.date

    vacancy_df = pd.DataFrame(vacancy_details, columns=["Date", "Day", "Session", "Room No.", "Exam Capacity", "Block", "Vacant"])
    vacancy_df["Date"] = pd.to_datetime(vacancy_df["Date"]).dt.date

    return seating_df, vacancy_df

# Helper function to create attendance sheets
def create_attendance_sheets(seating_df, roll_name_mapping):
    folder_name = "Attendance_Sheets"
    os.makedirs(folder_name, exist_ok=True)
    file_paths = []

    for _, row in seating_df.iterrows():
        date = row["Date"].strftime("%d_%m_%Y")
        sub_code = row["course_code"]
        room = row["Room"]
        session = row["Session"].lower()
        rolls = row["Roll_list"].split(";")
        
        attendance_data = [{"Roll": roll, "Name": roll_name_mapping.get(roll, ""), "Signature": ""} for roll in rolls]
        for _ in range(5):
            attendance_data.append({"Roll": "", "Name": "", "Signature": ""})

        df = pd.DataFrame(attendance_data)
        file_name = f"{date}_{sub_code}_{room}_{session}.xlsx"
        file_path = os.path.join(folder_name, file_name)
        file_paths.append(file_name)
        df.to_excel(file_path, index=False)
    
    return file_paths

# Streamlit app setup
def app():
    # Setting the page configuration to use a light theme (default Streamlit theme is light)
    st.set_page_config(page_title="Seating Allocation and Attendance", layout="wide", initial_sidebar_state="expanded")
    
    # Adding custom CSS for left-aligned components
    st.markdown("""
        <style>
            .streamlit-expanderHeader {
                text-align: left !important;
            }
            .css-18e3th9 {
                text-align: left !important;
            }
            .css-1d391kg {
                text-align: left !important;
            }
        </style>
    """, unsafe_allow_html=True)
    
    st.title("Seating Allocation and Attendance Management")
    
    uploaded_file = st.file_uploader("Upload Excel File for Processing", type="xlsx")
    
    if uploaded_file is not None:
        st.success("File uploaded successfully! Processing...")

        ip_4 = pd.read_excel(uploaded_file, sheet_name="ip_4")
        roll_name_mapping = ip_4.set_index("Roll")["Name"].to_dict()
        
        seating_df, vacancy_df = allocate_seating(uploaded_file)
        
        attendance_files = create_attendance_sheets(seating_df, roll_name_mapping)
        
        # Left-align the seating allocation plan header
        st.subheader("Seating Allocation Plan")
        st.dataframe(seating_df, use_container_width=True)
        
        # Left-align the room vacancy status header
        st.subheader("Room Vacancy Status")
        st.dataframe(vacancy_df, use_container_width=True)
        
        st.subheader("Download Attendance Sheets")
        selected_class = st.selectbox("Select Attendance Sheet", attendance_files)
        if selected_class:
            file_path = os.path.join("Attendance_Sheets", selected_class)
            if os.path.exists(file_path):
                st.write(f"Viewing: {selected_class}")
                df = pd.read_excel(file_path)
                st.dataframe(df)
            else:
                st.error("File not found.")
        
        zip_file_path = "Attendance_Sheets.zip"
        with st.spinner("Zipping attendance sheets..."):
            shutil.make_archive("Attendance_Sheets", 'zip', "Attendance_Sheets")
        
        st.download_button(
            label="Download All Attendance Sheets as ZIP",
            data=open(zip_file_path, "rb").read(),
            file_name="Attendance_Sheets.zip",
            mime="application/zip"
        )

if __name__ == "__main__":
    app()
