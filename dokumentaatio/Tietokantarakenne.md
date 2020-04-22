Tietokanta on normalisoitu.

## Create table -lauseet:

  ```sql
  CREATE TABLE account (
        id INTEGER NOT NULL,
        date_created DATETIME,
        date_modified DATETIME,
        username VARCHAR(144) NOT NULL,
        password VARCHAR(144) NOT NULL,
        role VARCHAR(144) NOT NULL,
        PRIMARY KEY (id)
  )
  ```
  ```sql
  CREATE TABLE plant (
          id INTEGER NOT NULL,
          name_fin VARCHAR(100) NOT NULL,
          name_lat VARCHAR(100) NOT NULL,
          water_need VARCHAR(50),
          fertilizer_need VARCHAR(50),
          light_need VARCHAR(50),
          PRIMARY KEY (id)
  )

  ```
  ```sql
  CREATE TABLE category (
        id INTEGER NOT NULL,
        name VARCHAR(100) NOT NULL,
        description VARCHAR(100) NOT NULL,
        PRIMARY KEY (id)
  )
  ```
  ```sql
  CREATE TABLE plantuser (
        plant_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        last_watered DATE,
        last_fertilized DATE,
        PRIMARY KEY (plant_id, user_id),
        FOREIGN KEY(plant_id) REFERENCES plant (id),
        FOREIGN KEY(user_id) REFERENCES account (id)
  )
  ```
  ```sql
  CREATE TABLE plantcategory (
        plant_id INTEGER NOT NULL,
        category_id INTEGER NOT NULL,
        PRIMARY KEY (plant_id, category_id),
        FOREIGN KEY(plant_id) REFERENCES plant (id),
        FOREIGN KEY(category_id) REFERENCES category (id)
  )
  ```
