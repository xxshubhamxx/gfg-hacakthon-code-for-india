function validateForm() {
    var step_count = document.forms["myForm"]["step_count"].value;
    var calories_burnt = document.forms["myForm"]["calories_burnt"].value;
    var hours_of_sleep = document.forms["myForm"]["hours_of_sleep"].value;
    var weight = document.forms["myForm"]["weight"].value;
    var height = document.forms["myForm"]["height"].value;
    var calories = document.forms["myForm"]["calories"].value;
    var bmi = document.forms["myForm"]["bmi"].value;
    var calorie_deficient_or_over = document.forms["myForm"]["calorie_deficient_or_over"].value;
  
    if (step_count == "" || calories_burnt == "" || hours_of_sleep == "" || weight == "" || height == "" || calories == "" || bmi == "" || calorie_deficient_or_over == "") {
      alert("All fields must be filled out");
      return false;
    }
  
    if (step_count < 0 || calories_burnt < 0 || hours_of_sleep < 0 || weight < 0 || height < 0 || calories < 0 || bmi < 0 || calorie_deficient_or_over < 0) {
      alert("All values must be positive");
      return false;
    }
    
    return true;
  }