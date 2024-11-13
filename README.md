----------Customer Support System-------------

It is used to analyse the database by asking questions to retrive data, etc,.

Home page: index.html (relative url: /)
        In this page you need to enter the details of the database you want to connect and make analysis.(Database details you need to provide are : host, database name, user, password, schema)
        
        Note: If you dont have any customer or other database, I have provided the code to create it. Just follow the steps I have provided in End of this file.
        
        Note:- You need to provide the DATABASE SCHEMA details with detailed description of every table and its atributes.
        Example Format:
        *Table 1: Customers*
        customer_id (INT):  Unique identifier for each customer (Primary Key)
        first_name (VARCHAR): Customer's first name
        last_name (VARCHAR): Customer's last name
        email (VARCHAR): Customer's email address
        phone_number (VARCHAR): Customer's phone number
        shipping_address (VARCHAR): Customer's shipping address
        .... etc.

        *Table 2: Orders*
        order_id (INT): Unique identifier for each order (Primary Key)
        customer_id (INT): Foreign key referencing the Customers table
        order_date (DATETIME): Date and time when the order was placed
        order_status (VARCHAR): Status of the order (e.g., pending, shipped, delivered, cancelled)
        shipping_address (VARCHAR): Shipping address for the order
        billing_address (VARCHAR): Billing address for the order
        total_amount (DECIMAL): Total amount of the order
        ...... etc.


Chat Bot Page: chat.html (relative url: /bot)
        In this page you can ask the required questions about the database.
        Note:- I have given only some finite no of context questions about the bot (e.g: hi, hii, hello, what can you do, etc.) so it will less interactive responses about itself.
        But you can ask any question about your database, it can give effective responses.


NOTE:- If you dont have any database, I have Provided the DATABASE AND DATABASE ENTRIES CREATION code. Just go throuth the following steps:-
- Open the database_data_generation.ipynb file.
- RUN the First Cell to create the Entries for the Database (which are randomly generated using faker module).
- COPY the SQL code in the Second Cell and Run it in your database Server. So that database and all the tables will be created.
- Now select table in Database and select import option and select the file which is created in our root folder and import the data.
- After importing all the tables entries, The database creation will be complete.
- I have provided the DESCRIPTIVE FORMAT of SCHEMA of Generated Database in Third Cell of this file.
- Now, You can ask the questions on this database.


EXAMPLE QUESTIONS CAN BE ASKED FOR THE ABOVE DATABASE:-
Give me the top 5 purchased customers details
customer details of David Diaz
Who spent the most money in purchasing the orders
Give me the no of orders puchased in category wise
Who purchased more in fashion category



