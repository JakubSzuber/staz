<h1>Development setup</h1>

To dev work after cloning the repo use `docker compose -f docker-compose.dev.yml up -d --build` for the initial setup and after each change to 
configuration-related files, after executing this command you can just start coding (the changes to Python or HTML files will be applied after each save) 
and you will see the website on [localhost:8000](http://localhost:8000). 

***Furthermore: a pull request with the prefix "dev_" is highly recommended in order to contribute to the repo.***
