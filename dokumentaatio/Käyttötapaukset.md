# Käyttötapaukset

### Käyttäjän ja adminin käyttötapaukset

* Käyttäjä voi tarkastella kaikkia tietokannassa olevia kasveja

  ```sql
  SELECT * FROM Plant;
  ```
  
* Käyttäjä voi hakea kasvia sen suomenkielisen nimen perusteella

  ```sql
  SELECT * FROM Plant
  WHERE LOWER(Plant.name_fin) = name_fin;
  ```
  
* Käyttäjä voi hakea kaikki tietyn kategorian kasvit

  ```sql
  SELECT * FROM Plant
  WHERE Plant.id = plant_id;
  ```
  ```sql
  SELECT * FROM PlantCategory;
  ```
  
* Käyttäjä voi lisätä kasvin omalle listalleen

  ```sql
  SELECT * FROM Plant
  WHERE Plant.id = plant_id;
  ```
  ```sql
  SELECT * FROM User
  WHERE User.id = current_user.id;
  ```
  ```sql
  SELECT * FROM PlantUser
  WHERE PlantUser.plant_id = plant_id
  AND PlantUser.user_id = current_user.id;
  ```
  ```sql
  INSERT INTO PlantUser (plant_id, user_id, last_watered, last_fertilized)
  VALUES (plant_id, current_user.id, NULL, NULL);
  ```
  
* Käyttäjä voi poistaa kasvin omalta listaltaan

  ```sql
  DELETE FROM PlantUser
  WHERE PlantUser.plant_id = plant_id AND PlantUser.user_id = current_user.id;
  ```
  
* Käyttäjä voi päivittää tietoa siitä, milloin omalla listalla oleva kasvi on viimeksi kasteltu

  ```sql
  UPDATE PlantUser
  SET last_watered = new_value
  WHERE PlantUser.plant_id = plant_id
  AND PlantUser.user_id = current_user.id;
  ```
  
* Käyttäjä voi päivittää tietoa siitä, milloin omalla listalla oleva kasvi on viimeksi lannoitettu

  ```sql
  UPDATE PlantUser
  SET last_fertilized = new_value
  WHERE PlantUser.plant_id = plant_id
  AND PlantUser.user_id = current_user.id;
  ```

### Adminin käyttötapaukset

* Admin voi lisätä tietokantaan uuden kasvin

  ```sql
  SELECT * FROM Plant
  WHERE Plant.name_fin = name_fin;
  ```
  ```sql
  INSERT INTO Plant (name_fin, name_lat, water_need, fertilizer_need, light_need)
  VALUES (name_fin, name_lat, water_need, fertilizer_need, light_need);
  ```

* Admin voi päivittää tietokannassa olevan kasvin tietoja

  ```sql
  UPDATE Plant SET
  name_fin = name_fin, name_lat = name_lat, water_need = water_need, 
  fertilizer_need = fertilizer_need, light_need = light_need
  WHERE Plant.id = plant_id;
  ```

* Admin voi poistaa tietokannasta kasvin

  ```sql
  DELETE FROM Plant
  WHERE Plant.id = plant_id;
  ```

* Admin voi lisätä tietokantaan uuden kategorian

  ```sql
  SELECT * FROM Category
  WHERE Category.id = category_id;
  ```
  ```sql
  INSERT INTO Category (name, description)
  VALUES (name, description);
  ```

* Admin voi muokata tietokannassa olevaa kategoriaa

  ```sql
  UPDATE Category 
  SET name = name, description = description
  WHERE Category.id = category_id;
  ```

* Admin voi poistaa tietokannasta kategorian

  ```sql
  DELETE FROM Category
  WHERE Category.id = category.id;
  ```

* Admin voi lisätä kasvin kategoriaan

  ```sql
  SELECT * FROM PlantCategory
  WHERE PlantCategory.plant_id = plant_id
  AND PlantCategory.category_id = category_id;
  ```
  ```sql
  INSERT INTO PlantCategory (plant_id, category_id)
  VALUES (plant_id, category_id);
  ```

* Admin voi poistaa kasvin kategoriasta

  ```sql
  DELETE FROM PlantCategory
  WHERE PlantCategory.plant_id = plant_id
  AND PlantCategory.category_id = category_id;
  ```
