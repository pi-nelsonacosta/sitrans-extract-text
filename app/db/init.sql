USE tempdb;

CREATE TABLE sqlserver_table (
    id INT PRIMARY KEY IDENTITY(1,1),
    name NVARCHAR(255) NOT NULL,
    description NVARCHAR(MAX) NOT NULL
);
