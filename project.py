import streamlit as st 
import pandas as pd
import os

FILE_path="books.csv"
# load  csv file/create
def load_data():
    if os.path.exists(FILE_path):
        return pd.read_csv(FILE_path)
    else:
        df=pd.DataFrame(columns=["Book ID","Title","Author","Status"])
        df.to_csv(FILE_path,index=False)
        return df
    
# save data
def save_data(df):
    df.to_csv(FILE_path,index=False)
    
st.title("library managment system")

# session data
if "books" not in st.session_state:
    st.session_state.books=load_data()
    
menu = st.sidebar.selectbox("select option",["view books","add books", "issue books" ,"return books" ])


# view
if menu=="view books":
   st.header("Book List")
   st.dataframe(st.session_state.books)



# addbooks
elif menu=="add books":
    st.header("add books")
    title=st.text_input("book title")
    author=st.text_input("author name")
    
    if st.button("Add"):
        if title and author:
            new_id=len(st.session_state.books)+1
            new_book=pd.DataFrame({
                "Book ID":[new_id],
                "title":[title],
                "author":[author],
                "status":["available"]
            }) 
            st.session_state.books=pd.concat([st.session_state.books,new_book],
            ignore_index=True)
            save_data(st.session_state.books)
            st.text("book added successfully ")
        else:
            st.text("enter both entry")
# issue
elif menu=="issue books":
    st.header("issue book")
    available=st.session_state.books[st.session_state.books["Status"]=="available"]
    
    if available.empty:
        st.text("no books available to issue")
    else:
        book_id=st.selectbox("select book ID",available["book id"])
        if st.button("issue"):
            st.session_state.books.loc[st.session_state.books["book ID"]==book_id,
            "status"]="Issued"
            save_data(st.session_state.books)
            st.text("book issued successfuly")
            
# return
elif menu=="return books":
    st.header("return book")
    issued=st.session_state.books[st.session_state.books["Status"]=="issued"]
    if issued.empty:
      st.text("no issued book to return") 
    else:
        book_id=st.selectbox("select book id",issued["book id "])
        if st.button("return"):
            st.session_state.books.loc[st.session_state.books["book id "]==book_id,
            "Status"]="available"
            save_data(st.session_state.books)
            st.text("book return successfully")
