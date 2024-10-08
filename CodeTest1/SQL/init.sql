-- Create the 'parts' table
CREATE TABLE parts (
    ID SERIAL PRIMARY KEY,
    PART_NO TEXT
);

-- Create the 'times' table
CREATE TABLE times (
    ID SERIAL PRIMARY KEY,
    START_PART_ID INTEGER NOT NULL,
    END_PART_ID INTEGER NOT NULL,
    TIME NUMERIC DEFAULT 0,
    ACTIVE INTEGER DEFAULT 0,
    UPDATE_TIME TEXT NOT NULL,
    FOREIGN KEY (START_PART_ID) REFERENCES parts(ID),
    FOREIGN KEY (END_PART_ID) REFERENCES parts(ID)
);
