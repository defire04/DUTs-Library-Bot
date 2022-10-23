CREATE TABLE books
(
    id                              INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    title                           VARCHAR,
    author                          VARCHAR,
    lang                            VARCHAR(100),
    document_size                   VARCHAR(200),
    year_of_publication             INTEGER,
    publishing_house                VARCHAR(200),
    country                         VARCHAR(200),
    number_of_pages                 INTEGER,
    availability_in_the_library     VARCHAR(50),
    availability_in_electronic_form VARCHAR(50),
    added                           VARCHAR(200),
    classification                  VARCHAR(200),
    document_type                   VARCHAR(200),
    link_to_book                    VARCHAR(200)
);


drop table books;
INSERT INTO books (title, author, lang, document_size, year_of_publication, publishing_house, country,
                   number_of_pages, availability_in_the_library, availability_in_electronic_form, added, classification,
                   document_type, link_to_book)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?), ('2', 'a', 'a',  'a', 0,  'a',  'a', 9,  'a',  'a',  'a',  'a', 'a', 'a');

select * from books
