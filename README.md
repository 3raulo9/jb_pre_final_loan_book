
![T_2_Q_0498313961__D7_AA_D7_9E_D7_95_D7_A0_D7_944](https://github.com/3raulo9/jb_pre_final_loan_book/assets/123974722/0ebfba12-9d78-460d-b1ad-98c94c50d1c3)

# jb_pre_final_loan_book

Loan book john brice project

download the project = from my github page = [https://github.com/3raulo9/jb_pre_final_loan_book.git](https://github.com/3raulo9/jb_pre_final_loan_book/archive/refs/heads/main.zip)


in terminal open the project and create a virtual environment = 

virtualenv "the name you want to call your virtual environment"

we will call it "env" as a convention

cd inside \jb_pre_final_loan_book-main><env>        

          \jb_pre_final_loan_book-main\<env>cd Scripts

          \jb_pre_final_loan_book-main\<env>\Scripts>activate

if you will see in the beginning of your code line the (env) then you successfully activated the virtual environment


after do cd.. to go back one folder before the folder you in
do it two times and when you will be at the \jb_pre_final_loan_book-main\ folder

do the following (env) \jb_pre_final_loan_book-main>pip install -r requirements.txt

it will install all the requirements inside of your virtual environment 


now do cd bookloanjb 

and then do python manage.py createsuperuser
you will be creating a super user
do as you wish but don't forget the information you will be needing it later

then do python manage.py makemigrations

you will be needing it in case there was some unforseen change

and to confirm that command do python manage.py migrate


and to start the server do - python manage.py runserver



Here are some of the models that i created for the project:

1: User, you can register the username and password
2: Author, name, birth_year, nationality
3: Ebook, name, author, year_published, loan_type, ebook_content
4: Loan, id, user, ebook, loan_date, loan_delete
5: Review, id, user, ebook, rating, text_field, date
