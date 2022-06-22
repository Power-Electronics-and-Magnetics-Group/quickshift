:: This is the batch script to run the current-sharing Flask instance. The development mode below is to left alone unless
:: a production instance will be configured (instructions on this specifically coming later.) 

set FLASK_APP=front
set FLASK_ENV=development

python3 -m flask run
