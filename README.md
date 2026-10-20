<br>
<br>

# <p align="center"> ICT Library </p>
<br>

#### Video Demo:  <https://youtu.be/cYVsAX6xL_c>

#### Description:

<p align="center">
    This Python Application Software is an ICT Library System Which Lend Books from Online Database to Registered Users Only.
    <br>
</p>

## 📝 Table of Contents

- [About](#about)
- [Usage](#usage)
- [Start](#start)

## 🧐 About<a name = "about"></a>
  The ICT Library System Will Help People To Borrow and Return 3 Books Maximum at a time from Online Library Called Gutenberg General e-Books there for this Library will provide about 69,300 books at all for any registered members to borrow and return within a 3 days per book otherwise users must pay $1 per day if they miss the return date.


## 🎈 Usage<a name="usage"></a>

  [Register]
  This part will let the user sign in to the system and then save as a unique record in the existing Json file .

  [Login]
  This part let users to Login and then it remembers which user has login until it logout then it will let the user save all activity to the existing Json file with a unique record related to the current user.

  [Main_Menu]
  This part will list three options to the user after they login so 1st is to borrow a book, 2nd is to return the book and 3rd is to exit from the loop means they can logout of the system.

  [Borrow_Book]
  This part will let users borrow max of 3 books at a time and 3 days duration for each book as long as they login from all available libraries means a user can borrow the book from online general library. To do that the user must first featch all books title and type the book name or know the title of the book then the system uses a search function to list the book title from the selected library including similar books if available or it returns to the main menu.

  [Return_Book]
  This part will let users return one book at a time from their own borrowed book list as long as they login first and also it checks that if the user misses the return date or not so if they miss that date then it will ask the user to pay $1 per day then the user has the option to pay whatever money they have at the time and the system will manage the difference for them.


## 🏁 Start<a name = "start"></a>

These instructions will let you copy the project from github and running on your local machine for development and testing purposes.

### Prerequisites to Test

  This Python Application Project Needs The Following:-

- 1st - Intsallation of Python in the Local Machine.
  Use this website link if you don't know how to install it.

  https://www.tutorialspoint.com/how-to-install-python-in-windows

- 2nd - Under the project folder there will be a file called "requirements.txt" so you need to install it later and for now you can see them below the additional [requirements] (#requirements)

### Requirements<a name = "requirements"></a>
- pyfiglet
- requests
- validator_collection

#### Getting Started

- $

- $ wget https://github.com/Ethiomesi2020/Project_CS50P/archive/refs/heads/main.zip

- unzip main.zip

- rm main.zip

- ren Project_CS50P-main project

- cd project

- project $ ls

  README.md requirements.txt project.py files/......

- pip install -r requirements.txt

#### Running

- $ python project.py runserver

- http://127.0.0.1:5000/ 

