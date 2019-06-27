Create Database capstone;
use capstone;
drop table if exists Contact_us;
Create table Contact_us(
First_name varchar(25),
Last_name varchar(25),
Email varchar(60),
Country varchar(25),
Sub varchar(100)
);
select * from Contact_us;

Create table Login_details(
First_name varchar(25),
Last_name varchar(25),
Email varchar(60),
Passwd varchar(20),
Company_name varchar(30),
Designation varchar(20),
Reason_of_use varchar(200)
);

Insert into Login_details Values("Bhakti","Mehta","bhaktimehta111@gmail.com","pass","scu","student","learn");

select * from Login_details;