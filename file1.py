import streamlit as st
import io

st.set_page_config(page_title="File Handling App", layout="centered")
st.title("📁 Streamlit File Handling")

# --- Initialize session state ---
if "files" not in st.session_state:
    st.session_state.files = {}
if "used_file_names" not in st.session_state:
    st.session_state.used_file_names = set()
if "current_file" not in st.session_state:
    st.session_state.current_file = None
if "data_saved" not in st.session_state:
    st.session_state.data_saved = False
if "show_data" not in st.session_state:
    st.session_state.show_data = False
if "reset_flag" not in st.session_state:
    st.session_state.reset_flag = 0
if "file_exists_error" not in st.session_state:
    st.session_state.file_exists_error = False


def clear_all():
    st.session_state.files = {}
    st.session_state.current_file = None
    st.session_state.data_saved = False
    st.session_state.show_data = False
    st.session_state.file_exists_error = False
    st.session_state.reset_flag += 1


def clear_inputs_only():
    st.session_state.show_data = False
    st.session_state.file_exists_error = False
    st.session_state.reset_flag += 1


# --- 📁 Sidebar Section: Show All Files ---
with st.sidebar:
    st.header("📂 Your Files")
    if st.session_state.files:
        file_list = list(st.session_state.files.keys())
        selected = st.selectbox("Select a file to open:", file_list, key="selected_file")

        if st.button("📖 Open Selected File"):
            st.session_state.current_file = selected
            st.session_state.data_saved = True
            st.session_state.show_data = True  # 👈 Immediately show its data
            st.success(f"✅ Opened '{selected}' successfully!")
    else:
        st.info("No files created yet.")


# --- Create File Section ---
st.header("📝 Create a File")
file_name = st.text_input(
    "Enter File Name:",
    key=f"file_name_{st.session_state.reset_flag}",
    placeholder="example.txt"
)

if st.button("✅ Create File"):
    if not file_name.strip():
        st.warning("⚠️ Please enter a valid file name.")
    elif file_name in st.session_state.files or file_name in st.session_state.used_file_names:
        st.warning(f"⚠️ The file '{file_name}' already exists! Please use a different name.")
    else:
        st.session_state.files[file_name] = ""
        st.session_state.used_file_names.add(file_name)
        st.session_state.current_file = file_name
        clear_inputs_only()
        st.success(f"✅ File '{file_name}' created successfully!")

st.divider()


# --- Add Data Section ---
st.header("✍️ Add / Overwrite Data")
data_input = st.text_area(
    "Enter Data:",
    key=f"add_data_{st.session_state.reset_flag}",
    placeholder="Write your content here..."
)

if st.button("💾 Save Data"):
    if st.session_state.current_file:
        if data_input.strip():
            st.session_state.files[st.session_state.current_file] = data_input.strip()
            st.session_state.data_saved = True
            clear_inputs_only()
            st.success("✅ Data saved successfully! You can now view or download it.")
        else:
            st.warning("⚠️ Please enter some text before saving.")
    else:
        st.warning("⚠️ Please create a file first.")

st.divider()


# --- Show File Section ---
st.header("Show File Content")

if st.session_state.current_file and st.session_state.data_saved:
    show_btn = st.button("📂 Show / Hide File")
    if show_btn:
        st.session_state.show_data = not st.session_state.show_data

    if st.session_state.show_data:
        st.text_area(
            "📜 File Content (Read Only):",
            st.session_state.files[st.session_state.current_file],
            height=200,
            key=f"display_{st.session_state.reset_flag}",
        )
        st.caption(f"🔒 Currently viewing: **{st.session_state.current_file}** (read-only)")
else:
    st.info("💡 Save data first to enable viewing and downloading.")

st.divider()


# --- Update Data Section ---
st.header("Update Data")
update_input = st.text_area(
    "Enter Data to Append:",
    key=f"update_input_{st.session_state.reset_flag}",
    placeholder="Write text to append..."
)

if st.button("✏️ Update File"):
    if st.session_state.current_file:
        if update_input.strip():
            st.session_state.files[st.session_state.current_file] += "\n" + update_input.strip()
            st.session_state.data_saved = True
            clear_inputs_only()
            st.success("✅ Data appended successfully! You can now view or download the updated file.")
        else:
            st.warning("⚠️ Please enter text to append.")
    else:
        st.warning("⚠️ Please create a file first.")

st.divider()


# --- Download / Delete Section ---
st.header("💾 Download or Delete File")

col1, col2 = st.columns(2)

with col1:
    if st.session_state.current_file and st.session_state.data_saved:
        data = st.session_state.files[st.session_state.current_file].encode("utf-8")
        st.download_button(
            label="⬇️ Download File",
            data=io.BytesIO(data),
            file_name=st.session_state.current_file,
            mime="text/plain",
            key=f"download_{st.session_state.reset_flag}"
        )
    else:
        st.info("💡 Save or update data to enable download.")

with col2:
    if st.button("🗑️ Delete File"):
        if st.session_state.current_file:
            name = st.session_state.current_file
            del st.session_state.files[name]
            st.session_state.current_file = None
            st.session_state.data_saved = False
            st.session_state.show_data = False
            clear_inputs_only()
            st.success(f"🗑️ File '{name}' deleted successfully!")
        else:
            st.warning("⚠️ Please create a file first.")
