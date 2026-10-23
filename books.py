books = { 1 : {"title": "Harry potter", "author": "JK Rowling"},
          2: {"title": "Physics", "author": "H.C  Verma"},
          3: {"title": "Lookism", "author": "Gu jun pyong"}}

def list_books():
    for book_id, book in books.items():
        print(book_id, "-", book["title"], "by", book["author"])

def add_books():
        title = input("title: ")
        author = input("author: ")
        new_id = max(books) +1
        books[new_id] = {"title": title, "author": author}
        print("Added")

def book_search():
     x = input("Name of the book: ").lower()
     found = False
     for book_id, book in books.items():
        if x in book["title"].lower():
            print(book["title"], "by", book["author"])
            found= True
     if not found:
        print("Book not found")

def book_del():
    x = input("Name the book you want to delete: ").lower()
    for book_id, book in books.items():
        if x in book["title"].lower():
            del books[book_id]
            print("Book Deleted")
            break
    else:
        print("Book not found")

while True:
    print("\n1) Add 2) Search 3) Delete 4) List All 5) Exit")
    choice = input("choose: ")

    # to add
    if choice == "1":
        add_books()
    elif choice == "2":
        book_search()
    elif choice == "3":
        book_del()
    elif choice == "4":
        list_books()
    elif choice == "5":
        print("Bye")
        break
    else:
        print("Not built yet")


