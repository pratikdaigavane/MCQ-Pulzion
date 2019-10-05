# MCQ-Pulzion '19

## Description
This is  an  MCQ Platform developed for Pulzion'19 , TechFest PICT, Pune

## Technologies Used  
**Backend :** Django, MySQL  
**Frontend :** Javascript, Ajax, Bootstrap  
**Desktop App :** Electron.js 

</br>


[![Get it from the Snap Store](https://snapcraft.io/static/images/badges/en/snap-store-black.svg)](https://snapcraft.io/mcq-pulzion)

## Installation and Setup

1. Clone this repository `git clone https://github.com/pratikdaigavane/MCQ-Pulzion`
2. Start the virtual environment and install all the dependencies. `pip install -r requirements.txt`
3. Then start the django server by `python manage.py runserver`

## Usage
* The persons listed in database can login and appear for test  
* The test can be configured by editing `config.py`  
   * *Following are the parameters which can be edited:*
        * eventName = 'event_name'  
        
          * ide = 'True/False'   
          * ideHost = 'http://10.10.11.218:8080/'  
            Note: The c++, java, python ide was used in one of the use case of this project  
                For more details refer: https://github.com/pnshiralkar/Online-IDE
          
          
         
          


          # Duration of test
          duration = 2000  # Format mmss

          # Time at which timer becomes red
          tred = '2000'  # Format "mmss"

          useElectron = False

          '''
          WARNING !
          Make Sure that 
          level1 + level2 + level3 = totalQuestions
          '''

          # Total Question to be displayed
          totalQuestions = 50
          # Level 1 Questions
          level1 = 50
          # Level 2 Questions
          level2 = 0
          # Level 3 Questions
          level3 = 0

          # Correct Marks
          marksCorrect = 2

          # Incorrect Marks(DO NOT ADD MINUS SIGN!!!)
          marksIncorrect = 1















