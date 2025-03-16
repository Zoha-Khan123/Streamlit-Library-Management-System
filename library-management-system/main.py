import streamlit as st
from supabase import create_client, Client
from dotenv import load_dotenv
import os
import pandas as pd

# Load environment variables
load_dotenv()

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

# ============== Set up Streamlit page configuration =============
st.set_page_config(page_title="Library Management System",page_icon="📚",)

# Make tabs
tab1, tab2, tab3 , tab4 , tab5 , tab6 = st.tabs(["🏠 Home","📚 Add a Book", "🗑️ Remove a Book", "📖 Display all Books","🔍 Search for a Book","📊 Display Statistics"])


# ====================== Home ==================================
with tab1:
    st.title("🏠 :rainbow[_Library Management System_] ")
    st.markdown("""
    **📚 Manage your library efficiently with this easy-to-use system.**  
    Here, you can add new books, remove books, search for books, view all books, and analyze library statistics.
    """)

  
    st.divider()

    # Quick Links or Instructions
    st.subheader("🚀 :rainbow[Get Started]")
    st.markdown("""
    - **Add a Book**: Go to the **📚 Add a Book** tab to add a new book to the library.
    - **Remove a Book**: Use the **🗑️ Remove a Book** tab to delete a book from the library.
    - **Search for a Book**: Visit the **🔍 Search for a Book** tab to find a specific book.
    - **View All Books**: Check out the **📖 Display all Books** tab to see the complete list of books.
    - **Library Statistics**: Explore the **📊 Display Statistics** tab for insights into your library.
    """)

    st.divider()

    # Footer or Additional Information
    st.markdown("""
    **💡 Tip**: Use the tabs above to navigate through the system and manage your library effectively.
    """)



# =================== Add a book ===================================
with tab2:
    st.title("📚  :rainbow[Add a New Book]")
    with st.form(key='book_form'):
        col1, col2 = st.columns(2)
        with col1:
            title = st.text_input("Book Title")
            genre = st.text_input("Genre")
            published = st.number_input("Published Year")
        with col2:
            author = st.text_input("Author")
            read_status = st.selectbox("Read Status", ("Yes", "No"))
        submit_button = st.form_submit_button(label="➕ Add Book")

    if submit_button:
        if all([title, genre, published, author, read_status]):
            existing_book = supabase.table("library-management").select("*").eq("Title", title).eq("Author", author).execute()
            if existing_book.data:  
                st.warning("⚠️ This book already exists in the library.")
            else:
                book_dict = {"Title": title, "Author": author, "Publication Year": published, "Genre": genre, "Read Status": read_status}
                supabase.table("library-management").insert([book_dict]).execute()
                st.success("✅ Book added successfully!")
        else:
            st.warning("⚠️ Please fill all fields before adding the book.")


# =================== Remove a book ===================================
with tab3:
    st.title("🗑️ :rainbow[Remove a Book]")
    remove = st.text_input("Enter the title of the book to remove")
    if st.button("🗑️ Remove Book"):
        book_exists = supabase.table("library-management").select("*").eq("Title", remove).execute()
        if book_exists.data:
            supabase.table("library-management").delete().eq("Title", remove).execute()
            st.success(f"✅ Book '{remove}' removed successfully!")
        else:
            st.warning(f"⚠️ No book found with the title '{remove}'.")


# =================== See all books ===================================
with tab4:
    st.title("📖 :rainbow[Library Collection]")
    response = supabase.table("library-management").select("*").execute()
    book_store = response.data
    if book_store:
        df = pd.DataFrame(book_store)
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No books found in the library.")


# =================== Search books ===================================
with tab5:
    st.title("🔍 :rainbow[Search for a Book]")
    search = st.text_input("Enter the book title to search")
    search_button = st.button("🔍 Search")  # Ensure search runs only when button is clicked

    if search_button:  
        if search:  # Check if the search input is not empty
            data = supabase.table("library-management").select("*").eq("Title", search).execute()

            if data.data:
                search_results_df = pd.DataFrame(data.data)  # Convert search result to DataFrame
                st.write("📚 **Search Results:**")
                st.dataframe(search_results_df)  # Display the search results
            else:
                st.warning("⚠️ No book found with this title.")
        else:
            st.warning("⚠️ Please enter a book title to search.")


# =================== Library Statistics ===================================
with tab6:
    st.title("📊 :rainbow[Library Statistics]")
    response = supabase.table("library-management").select("*").execute()
    book_store = response.data
    if book_store:
        total_books = len(book_store)
        read_books = sum(1 for book in book_store if book["Read Status"] == "Yes")
        unread_books = total_books - read_books

        col1, col2, col3 = st.columns(3)
        col1.metric("📚 Total Books", total_books)
        col2.metric("✔️ Read Books", read_books)
        col3.metric("📖 Unread Books", unread_books)
    else:
        st.info("No books available to display statistics.")