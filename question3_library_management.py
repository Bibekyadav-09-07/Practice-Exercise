def read_integer(prompt, minimum=None):
    while True:
        try:
            value = int(input(prompt))
            if minimum is not None and value < minimum:
                print("Value must be at least {}.".format(minimum))
            else:
                return value
        except ValueError:
            print("Please enter a whole number.")


def add_book(books):
    book_id = input("Book ID: ").strip()
    if not book_id:
        print("Book ID cannot be empty.")
        return
    if book_id in books:
        print("That book ID already exists.")
        return
    title = input("Title: ").strip()
    author = input("Author: ").strip()
    if not title or not author:
        print("Title and author cannot be empty.")
        return
    copies = read_integer("Number of copies: ", 0)
    books[book_id] = {
        "title": title, "author": author, "copies": copies, "borrowed": 0
    }
    print("Book added successfully.")


def display_available_books(books):
    found = False
    for book_id, book in books.items():
        if book["copies"] > 0:
            found = True
            print("ID: {} | {} by {} | Available: {}".format(
                book_id, book["title"], book["author"], book["copies"]
            ))
    if not found:
        print("There are no books with available copies.")


def search_books(books):
    query = input("Enter a title or author to search: ").strip().lower()
    if not query:
        print("Search text cannot be empty.")
        return
    found = False
    for book_id, book in books.items():
        if query in book["title"].lower() or query in book["author"].lower():
            found = True
            print("ID: {} | {} by {} | Available: {}".format(
                book_id, book["title"], book["author"], book["copies"]
            ))
    if not found:
        print("No matching books were found.")


def borrow_book(books, borrowed_books):
    book_id = input("Book ID to borrow: ").strip()
    if book_id not in books:
        print("Book not found.")
        return
    if books[book_id]["copies"] == 0:
        print("No copies are currently available.")
        return
    books[book_id]["copies"] -= 1
    books[book_id]["borrowed"] += 1
    borrowed_books.append(book_id)
    print("Book borrowed successfully.")


def return_book(books, borrowed_books):
    book_id = input("Book ID to return: ").strip()
    if book_id not in books:
        print("Book not found.")
        return
    if book_id not in borrowed_books:
        print("This book was not borrowed, so it cannot be returned.")
        return
    borrowed_books.remove(book_id)
    books[book_id]["borrowed"] -= 1
    books[book_id]["copies"] += 1
    print("Book returned successfully.")


def display_unavailable_books(books):
    found = False
    for book_id, book in books.items():
        if book["copies"] == 0:
            found = True
            print("ID: {} | {} by {}".format(
                book_id, book["title"], book["author"]
            ))
    if not found:
        print("All books have at least one available copy.")


def display_totals(books):
    total_titles = 0
    total_copies = 0
    total_available = 0
    for book in books.values():
        total_titles += 1
        total_copies += book["copies"] + book["borrowed"]
        total_available += book["copies"]
    print("Different book titles: {}".format(total_titles))
    print("Total copies in inventory: {}".format(total_copies))
    print("Available copies: {}".format(total_available))


def main():
    books = {}
    borrowed_books = []
    while True:
        print("\nLIBRARY MANAGEMENT")
        print("1. Add book\n2. Display available books\n3. Search books")
        print("4. Borrow book\n5. Return book\n6. Show books with no copies")
        print("7. Show inventory totals\n0. Exit")
        choice = input("Choose an option: ").strip()
        if choice == "1":
            add_book(books)
        elif choice == "2":
            display_available_books(books)
        elif choice == "3":
            search_books(books)
        elif choice == "4":
            borrow_book(books, borrowed_books)
        elif choice == "5":
            return_book(books, borrowed_books)
        elif choice == "6":
            display_unavailable_books(books)
        elif choice == "7":
            display_totals(books)
        elif choice == "0":
            print("Goodbye.")
            break
        else:
            print("Invalid menu choice.")


if __name__ == "__main__":
    main()
